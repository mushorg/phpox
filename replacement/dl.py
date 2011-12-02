import extension_loaded
def call():
    if extension_loaded.call == True:
        function = """dl('apd.so');"""
        return 'False'
    else:
        return 'True'    
print call()