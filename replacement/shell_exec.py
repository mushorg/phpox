def call():    
    function = """
    $ret = shell_sandbox($cmd);
    return $ret;
    """
    return function
