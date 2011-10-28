
def call():
    # TODO: Make uptime dynamic
    function = """
    $ret =  shell_sandbox($cmd);
    return $ret;
    """
    return function
