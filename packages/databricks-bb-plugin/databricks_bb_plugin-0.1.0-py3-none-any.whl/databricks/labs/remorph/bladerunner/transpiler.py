import logging
import os
import platform
import subprocess
import sys
import traceback
from collections.abc import Sequence
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from lsprotocol.types import Diagnostic, TextEdit, DiagnosticSeverity

from .helpers import full_range
from .hasher import compute_hash

logger = logging.getLogger(__name__)

class Transpiler:

    def __init__(self, dialect: str):
        self._license_file = self._locate_license()
        self._config_file = self._locate_config(dialect)
        self._binary = self._locate_binary()

    def transpile(self, file_name: str, source_code: str) -> tuple[Sequence[TextEdit], Sequence[Diagnostic]]:
        with TemporaryDirectory(prefix="bladerunner_") as tempdir:
            return self._transpile(tempdir, file_name, source_code)

    def _transpile(self, tempdir: str, file_name: str, source_code: str) -> tuple[Sequence[TextEdit], Sequence[Diagnostic]]:
        # prepare fs
        workdir = Path(tempdir)
        originals_dir = workdir / "originals"
        originals_dir.mkdir(parents=True, exist_ok=True)
        original_file = originals_dir / file_name
        original_file.parent.mkdir(parents=True, exist_ok=True)
        transpiled_dir = workdir / "transpiled"
        transpiled_dir.mkdir(parents=True, exist_ok=True)
        transpiled_file = transpiled_dir / file_name
        transpiled_file.parent.mkdir(parents=True, exist_ok=True)
        self._store_source(original_file, source_code)
        error = self._run_binary(workdir, transpiled_dir, original_file)
        if error:
            diagnostic = Diagnostic(range=full_range(source_code), message=error, severity=DiagnosticSeverity.Error, code="PARSING-FAILURE")
            return [], [diagnostic]
        transpiled = transpiled_file.read_text(encoding="utf-8")
        edits = [TextEdit(range=full_range(source_code), new_text=transpiled)]
        return edits, []

    def _locate_binary(self) -> Path:
        if 'darwin' in sys.platform:
            tool = "MacOS/dbxconv"
        elif 'win' in sys.platform:
            tool = "Windows/dbxconv.exe"
        elif 'linux' in sys.platform:
            tool = "Linux/dbxconv"
        else:
            raise Exception(f"Unsupported platform: {sys.platform}")
        return Path(__file__).parent / "Converter" / "bin" / tool

    def _locate_license(self):
        return Path(__file__).parent / "Converter" / "bin" / "converter_key.txt"

    def _locate_config(self, dialect: str) -> Path:
        configs_folder = Path(__file__).parent / "Converter" / "Configs"
        all_configs = os.listdir(configs_folder)
        names = list(filter(lambda cfg: cfg.lower() == dialect, all_configs))
        if len(names) != 1:
            raise Exception(f"Could not locate main config file for dialect {dialect}")
        parent =  configs_folder / names[0]
        short = "ds" if dialect == "datastage" else "hana" if dialect == "saphana" else "bq" if dialect == "bigquery" else dialect
        for prefix in (short, f"{short}_procs", f"base_{short}", dialect):
            for extension in ("_main", ""):
                for suffix in ("databricks", "databricksql", "databricks_sql", "databricks_dbsql", "databricks_sql_python", "databricks_workflow", "dws", "dbks", "dbks_pyspark", "sparksql", "pyspark", "_sql"):
                    path = parent / f"{prefix}2{suffix}{extension}.json"
                    if path.exists():
                        return path
        raise Exception(f"Could not locate main config file for dialect {dialect}")

    def _store_source(self, file_path: Path, source_code: str) -> None:
        file_path.write_text(source_code, encoding="utf-8")

    def _run_binary(self, workdir: Path, transpiled_dir: Path, source: Path) -> str | None:
        cwd = os.getcwd()
        try:
            os.chdir(workdir)
            return self._run_binary_in_workdir(workdir, transpiled_dir, source)
        finally:
            os.chdir(cwd)

    def _run_binary_in_workdir(self, workdir: Path, transpiled_dir:Path, source: Path) -> str | None:
        try:
            args = [
                str(self._binary),
                "SQL",
                "-u",
                self._config_file.name,
                "-n",
                str(transpiled_dir.relative_to(workdir)),
                "-i",
                str(source.relative_to(workdir))
            ]
            hash = compute_hash(args)
            args.extend(["-H", hash])
            env = deepcopy(os.environ)
            # converter needs access to included configs
            env["BB_CONFIG_CONVERTER_DIR"] = str(self._config_file.parent.parent)
            env["UTF8_NOT_SUPPORTED"] = str(1)
            completed = subprocess.run(args, cwd=str(workdir), env=env, capture_output=True, text=True)
            # capture output before managing return code
            if completed.stdout:
                for line in completed.stdout.split("\n"):
                    logger.info(line)
            if completed.stderr:
                for line in completed.stderr.split("\n"):
                    logger.error(line)
            # manage return code
            completed.check_returncode()
            return None
        # it is good practice to catch broad exceptions raised by launching a child process
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Conversion failed", exc_info=e)
            return str(e)
