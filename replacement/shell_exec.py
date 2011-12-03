def call():    
    function = """
    echo "<SHELL_EXEC>$cmd";
    $ret = shell_sandbox($cmd);
    return $ret;
    """
    return function
