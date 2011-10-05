def call():
    function = """\t$function_name = "fgets" . "_" . $rand;
\t$ret = $function_name($handle,$length);
\techo $ret;
\treturn $ret;"""
    return function