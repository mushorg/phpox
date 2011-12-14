def call():
    function = """
    echo "PASSTHRU $cmd\\n";
    $ret = shell_sandbox($cmd);
"""
    return function
