def call(): 
    function = """ \tif ($name == "apd") 
    \t{return FALSE;} 
    \telse {
    \treturn TRUE;}""" 
    return function 
print call()