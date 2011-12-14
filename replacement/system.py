
def call():
    # TODO: Make uptime dynamic
    function = """
    echo "SYSTEM $cmd\\n";
    $ret =  shell_sandbox($cmd);
    return $ret;
    """
    return function
