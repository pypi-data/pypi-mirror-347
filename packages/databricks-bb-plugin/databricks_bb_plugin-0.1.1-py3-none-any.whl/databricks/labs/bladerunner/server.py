import logging
from pathlib import Path

from lsprotocol.types import (
    InitializeParams,
    Registration,
    RegistrationParams,
    INITIALIZE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CLOSE,
    LanguageKind,
    DidOpenTextDocumentParams,
    DidCloseTextDocumentParams,
)

from pygls.lsp.server import LanguageServer

from databricks.labs.bladerunner.lsp_extension import (
    TRANSPILE_TO_DATABRICKS_CAPABILITY,
    TranspileDocumentParams,
    TranspileDocumentResult,
    TRANSPILE_TO_DATABRICKS_METHOD,
)
from databricks.labs.bladerunner.transpiler import Transpiler

logging.basicConfig(filename='lsp-server.log', filemode='w', level=logging.DEBUG)

logger = logging.getLogger(__name__)

class Server(LanguageServer):

    async def did_initialize(self, init_params: InitializeParams) -> None:
        registrations = [
            Registration(
                id=TRANSPILE_TO_DATABRICKS_CAPABILITY["id"], method=TRANSPILE_TO_DATABRICKS_CAPABILITY["method"]
            )
        ]
        options: dict[str, any] = init_params.initialization_options or {}
        remorph: dict[str, any] = options.get("remorph", {})
        dialect = remorph.get("source-dialect", "ansi")
        self._transpiler = Transpiler(dialect)
        register_params = RegistrationParams(registrations)
        await self.client_register_capability_async(register_params)

    def transpile_to_databricks(self, params: TranspileDocumentParams) -> TranspileDocumentResult:
        source_sql = self.workspace.get_text_document(params.uri).source
        changes, diagnostics = self._transpiler.transpile(Path(params.uri).name, source_sql)
        return TranspileDocumentResult(
            uri=params.uri, language_id=LanguageKind.Sql, changes=changes, diagnostics=diagnostics
        )


server = Server("remorph-sqlglot-transpiler", "v0.1")


@server.feature(INITIALIZE)
async def lsp_did_initialize(params: InitializeParams) -> None:
    await server.did_initialize(params)


@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def lsp_text_document_did_open(params: DidOpenTextDocumentParams) -> None:
    logger.debug(f"open-document-uri={params.text_document.uri}")


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
async def lsp_text_document_did_close(params: DidCloseTextDocumentParams) -> None:
    logger.debug(f"close-document-uri={params.text_document.uri}")


@server.feature(TRANSPILE_TO_DATABRICKS_METHOD)
def transpile_to_databricks(params: TranspileDocumentParams) -> TranspileDocumentResult:
    return server.transpile_to_databricks(params)


if __name__ == "__main__":
    server.start_io()
