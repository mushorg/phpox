def call():
    ret = """
    echo "FUNCTION_EXISTS $name\\n";
    $function_name = "function_exists" . "_" . $rand;
    return $function_name($name);
    """
    return ret
