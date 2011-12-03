def call():
    function = """ if (!extension_loaded('apd')) {
        \t{return FALSE;};}""" 
    return function    
#print call()