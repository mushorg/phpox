
def call():
    # TODO: Make uptime dynamic
    function = """
    echo "SYSTEM $cmd";
    $ret =  shell_sandbox($cmd);
    return $ret;
    """
    return function
