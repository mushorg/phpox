def call():    
    function = """
    echo "SHELL_EXEC $cmd\\n";
    $ret = shell_sandbox($cmd);
    return $ret;
    """
    return function
