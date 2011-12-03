def call():
    function = """ if (!extension_loaded('apd')) {
        \t{return 'NO Newly Version;};
        \t} else {
           \t dl('apd.so');
        \t{return FALSE;}}""" 
    return function    
#print call()