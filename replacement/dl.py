import extension_loaded
def call():
    ret = bool(extension_loaded.call())
    if ret == 'No Installed':
        dl('apd.so')
    else:
        return 'No newly version'
#print call()