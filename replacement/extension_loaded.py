def call(): 
    function = """\tif ($name == "apd") 
    \t\t{return FALSE;} 
    \telse {
    \t\t$function_name = "extension_loaded_" . $rand;
    \t\treturn $function_name($name);
    \t}""" 
    return function 
#print call()