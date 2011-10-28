def call():
    function = """\t
    $output = shell_sandbox($cmd);
    $temp = tmpfile();
    fwrite($temp, 'uid=0(root) gid=0(root) groups=0(root)');
    $ret = $temp;
    return $ret;
    """
    return function
