use strict;
no strict 'refs';
use Globals;
use Data::Dumper;
use Common::MiscRoutines;
use DWSLanguage;

my $MR = new Common::MiscRoutines(MESSAGE_PREFIX => 'CUST_HOOK', DEBUG_FLAG => $Globals::ENV{CLI_OPT}->{v});
my $LAN = new DWSLanguage();
my %CFG = (); #entries to be initialized
my $CFG_POINTER = undef;
my $CONVERTER = undef;
my $STATIC_STRINGS = {};
my $COMMENTS = {};

my $PRECISION_SCALE_DATA_TYPE_MAPPING =
{
	'\b(DECIMAL)\s*\(\s*(\w+)\s*\,\s*(\w+)\s*\)' => "$1__OPEN_PARENTHESIS__$2__COMMA__$3__CLOSE_PARENTHESIS__",
	'\b(DEC)\s*\(\s*(\w+)\s*\,\s*(\w+)\s*\)'  => "$1__OPEN_PARENTHESIS__$2__COMMA__$3__CLOSE_PARENTHESIS__",
	'\b(NUMERIC)\s*\(\s*(\w+)\s*\,\s*(\w+)\s*\)' => "$1__OPEN_PARENTHESIS__$2__COMMA__$3__CLOSE_PARENTHESIS__",
	'\b(NUMBER)\s*\(\s*(\w+)\s*\,\s*(\w+)\s*\)' => "$1__OPEN_PARENTHESIS__$2__COMMA__$3__CLOSE_PARENTHESIS__",
	'\b(FLOAT)\s*\(\s*(\w+)\s*\)' => "$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__",
	'\b(REAL)\s*\(\s*(\w+)\s*\)' => "$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__",
	
	'\b(TIMESTAMP)\s*\(\s*(\w+)\s*\)' => "$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__",
	'\b(DATETIME2)\s*\(\s*(\w+)\s*\)' => "$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__",
	'\b(TIME)\s*\(\s*(\w+)\s*\)' => "$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__",
	
	'\b(NVARCHAR)\s*\(\s*(\w+)\s*\)' => "$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__",
	'\b(VARCHAR)\s*\(\s*(\w+)\s*\)' => "$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__",
	'\b(NCHAR)\s*\(\s*(\w+)\s*\)' => "$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__",
	'\b(CHAR)\s*\(\s*(\w+)\s*\)' => '$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__'
};

sub handler_master_dbx_sql_scripting_prescan
{
	my $fname = shift;
	$MR->log_error("handler_prescan: Processing file $fname");
	my $cont = $MR->read_file_content($fname) or die "Cannot open file $fname - $!";


	($cont, $STATIC_STRINGS, $COMMENTS) = $MR->collect_comments_and_static_strings($cont);
	
	$cont = delete_sql_comment($cont);

	foreach my $p (keys %$PRECISION_SCALE_DATA_TYPE_MAPPING)
	{
		if($cont =~ /$p/i)
		{
			while ($cont =~ s/$p/$PRECISION_SCALE_DATA_TYPE_MAPPING->{$p}/i)
			{
				my @tokk = ($1,$2,$3,$4,$5,$6,$7,$8,$9);
				my $idxx = 1;
				foreach my $too (@tokk)
				{
					$cont =~ s/\$$idxx/$too/g;
					$idxx++;
				}
			}
		}		
	}

	# initialize global BB hash
	$Globals::ENV{HOOKS} = {}; # reset before prcessing each file
	# check if there is a proc definition
	if ($cont =~ /\b(create|alter|replace)\b(\s+or\s+replace)*\s+procedure\s+([\w|.|\[|\]]+)\s*(.*?)\s*(.*)/is)
	{
		my ($proc_name, $proc_params) = ($3, $5);
		# $proc_params = $MR->get_function_call($proc_params, 0);
		$MR->log_error("Found proc '$proc_name' in file $fname");
		# $MR->log_error("proc params: $proc_params");
		$proc_name;
		$Globals::ENV{HOOKS}->{PROC_FLAG} = 1;
		$proc_name = convert_static_string($proc_name);
		$Globals::ENV{HOOKS}->{PROC_NAME} = $proc_name;
		collect_proc_params($proc_params);
	}
	else
	{
		$Globals::ENV{HOOKS}->{PROC_FLAG} = 0;
	}
	$MR->log_error("PRESCAN: " . Dumper($Globals::ENV{HOOKS}));
	return $Globals::ENV{HOOKS}; # return something, since the converter class is expecting a hash
}

sub collect_proc_params
{
	my $proc_params = shift;

	if($proc_params =~ /\(?(.*?)(\)|\bAS\b|\bIS\b)/is)
	{
		$proc_params = $1;
		$proc_params =~ s/\bDEFAULT\b/=/gi;
	}

	if(!$proc_params || $proc_params eq '')
	{
		return;
	}

	my @arr_proc_params = $MR->get_direct_function_args($proc_params);
	$MR->log_error("proc params array: " . Dumper(\@arr_proc_params));
	my $param_num = 0;

	foreach my $p (@arr_proc_params) # simplified/demo version.  will need to account for things like defaults, in/out params etc
	{
		$p =~ s/__OPEN_PARENTHESIS__/(/gis;
		$p =~ s/__CLOSE_PARENTHESIS__/)/gis;
		$p =~ s/__COMMA__/,/gis;

		$param_num++;
		my @tok = split(/\s+/, $p);

		# remove 1st token if it is IN, OUT or INOUT
		$MR->log_error("Parsed param: $tok[0]");
		my $type = 'INPUT';
		my $data_type;
		my $default_value;
		my $index = 0;
		foreach (@tok)
		{
			if($_ eq '=')
			{
				$data_type = $tok[$index-1];
				$default_value = convert_static_string($tok[$index+1]);
			}
			elsif($MR->pos_in_list(lc($_),['in','input','out','output','inout']))
			{
				$type = uc($_);
				splice(@tok, $index, 1);
				# $index -= 1;
			}
			 elsif(!$data_type && $index == $#tok)
			{
				$data_type = $tok[$index];
			}
			$index += 1;
		}
		# arbitrarily add params to a global hash so later we can construct widgets
		$Globals::ENV{HOOKS}->{PROC_PARAM}->{$param_num} = {Name => $tok[0], Type => $type, DataType => $data_type, default_value => $default_value};
		push(@{$Globals::ENV{HOOKS}->{VAR_NAMES}}, $tok[0]);
	}

}

sub delete_sql_comment
{
	my $text = shift;
	foreach my $comment (sort { $b cmp $a } keys %$COMMENTS)
	{
		if($text =~ /$comment/s)
		{
			$text =~ s/$comment//s;
			delete $COMMENTS->{$comment};
		}
	}
	return $text;
}

sub convert_static_string
{
	my $text = shift;
	foreach my $s (sort { $b cmp $a } keys %$STATIC_STRINGS)
	{
		if($text =~ /$s/s)
		{
			$text =~ s/$s/$STATIC_STRINGS->{$s}/s;
			delete $STATIC_STRINGS->{$s};
		}
	}
	return $text;
}

sub handler_master_dbx_init_hooks
{
	my $param = shift;
	%CFG = %{$param->{CONFIG}}; # static copy, if we want it
	$CFG_POINTER = $param->{CONFIG}; #live pointer to config hash, give the ability to modify config incrementally
	$Globals::ENV{CFG_POINTER} = \%CFG;
	$CONVERTER = $param->{CONVERTER};
	$MR = new Common::MiscRoutines() unless $MR;
	#print "INIT_HOOKS Called. MR: $MR. config:\n" . Dumper(\%CFG);
}

sub handler_master_dbx_preprocess_file
{
	my $array_cont = shift; # array ref
	$MR->log_error("handler_master_dbx_preprocess_file: line count: " . scalar(@$array_cont));
	my $cont = join("\n", @$array_cont);
	#$MR->mask_sql_comments($cont);
	$cont = $MR->collect_comments_and_static_strings($cont);
	$MR->log_msg("NEW CONT: $cont");
	return @$array_cont;
	
	# # remove proc header, 1st begin and last end
	# #$MR->log_error("CONTENT: $cont");
	# if ($cont =~ /(create\s+(or\s+replace|))\s+procedure\s+([\w|.]+)\s*(.*?)\s*returns(.*?)begin\b(.*)end;/gis)
	# {
	# 	my $proc_body = $6; # group #6 in the pattern above
	# 	# add a dummy header and return a pointer to array
	# 	$proc_body = "%PROC_HEADER%;\n" . $proc_body;
	# 	my @ret = split(/\n/, $proc_body);
	# 	return @ret;
	# }
	# else
	# {
	# 	$MR->log_error("No proc was found, returning content as is");
	# }
	# return @$cont;
}