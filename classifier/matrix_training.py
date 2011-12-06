import docsimlarity
import sys, os
import getopt
import json
import hashlib

def wordlist_train(dirpath, listall):
    list_scripts = os.listdir(dirpath)
    dictall_md5 = {}
    for sample in list_scripts:
        filemd5 = md5(dirpath+sample)
        gettext = docsimlarity.fileio(dirpath+sample)
        gettext = docsimlarity.textread(gettext)
        listall = docsimlarity.tf_text(gettext)
        dictall_md5[filemd5] = listall
    return json.dumps(dictall_md5)


def wordlist_docrequest(docpath, request_list):
    #filemd5 = md5(docpath)
    gettext = docsimlarity.fileio(docpath)
    gettext = docsimlarity.textread(gettext)
    request_list = docsimlarity.tf_text(gettext)
    #request_list["FileMD5"] = filemd5
    return json.dumps(request_list)

def md5(fileName):
    """Compute md5 hash of the specified file"""
    m = hashlib.md5()
    try:
        fd = open(fileName,"rb")
    except IOError:
        print "Reading file has problem:", fileName
        return
    
    x = fd.read()
    fd.close()
    m.update(x)
    return m.hexdigest()

def getTrainset(classifier):
    train_list = {}
    dirtrain = "trainsamples/"+classifier+"/"
    train_list = wordlist_train(dirtrain, train_list)
    docsimlarity.filewrite("trainset"+"/"+classifier+"/"+classifier+"_matrix", train_list)
    #print "getTrainset_train_list"+ train_list
    
