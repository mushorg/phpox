def call():
    extension_loaded = 'apd'
    ret = bool(extension_loaded)
    if ret == 'true':
         return 'No Installed'
    else:
         return 'No newly version'
print call()