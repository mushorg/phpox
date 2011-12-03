def call():
    function = """
    echo "PASSTHRU $cmd";
    $ret = shell_sandbox($cmd);
"""
    return function
