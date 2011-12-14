def call():
    function = """
    echo "EXECUTE $cmd\\n";
    $ret = shell_sandbox($cmd);
    """
    return function
