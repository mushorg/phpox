import docsimlarity
import sys, os
import getopt


if __name__ == '__main__':
    print "\nFile Classifier Starting based on document similarity "
    opts  = getopt.getopt(sys.argv[1], "v", [])
    #if len(opts)< 2:
    
    setpath = "/home/julia/projects/php_sandbox/classifier/"
    docpath = setpath + opts[1]
    trainpath = setpath + "trainset/"
    
    #Training Set for phpbot Classifier
    training_phpbot_list = []
    list_phpbot = os.listdir(trainpath + "/phpbot/")
    for sample in list_phpbot:
        gettext = docsimlarity.fileio(trainpath + "/phpbot/"+sample)
        gettext = docsimlarity.textread(gettext)
        training_phpbot_list.append(docsimlarity.tf_text(gettext))
        
    training_phpecho_list = []
    list_phpbot = os.listdir(trainpath + "/phpecho/")
    for sample in list_phpbot:
        gettext = docsimlarity.fileio(trainpath + "/phpecho/"+sample)
        gettext = docsimlarity.textread(gettext)
        training_phpecho_list.append(docsimlarity.tf_text(gettext))
        
    #training_phpdownloading_list = []
    #list_phpbot = os.listdir(trainpath + "/phpdownloading/")
    #for sample in list_phpbot:
    #    gettext = docsimlarity.fileio(trainpath + "/phpdownloading/"+sample)
    #    gettext = docsimlarity.textread(gettext)
    #    training_phpdownloading_list.append(docsimlarity.tf_text(gettext))
        
    training_phpshell_list = []
    list_phpbot = os.listdir(trainpath + "/phpshell/")
    for sample in list_phpbot:
        gettext = docsimlarity.fileio(trainpath + "/phpshell/"+sample)
        gettext = docsimlarity.textread(gettext)
        training_phpshell_list.append(docsimlarity.tf_text(gettext))
    
    # Process php scripts into a list
    gettext = docsimlarity.fileio(docpath)
    gettext = docsimlarity.textread(gettext)
    request_list = docsimlarity.tf_text(gettext)
    
    # Calculate similarity of documents
    eqularity_phpbot = []
    for document in training_phpbot_list:
        equality = docsimlarity.comp_descriptors (request_list, document)
        eqularity_phpbot.append(equality)
        
    eqularity_phpecho = []
    for document in training_phpecho_list:
        equality = docsimlarity.comp_descriptors (request_list, document)
        eqularity_phpecho.append(equality)
    
    #eqularity_phpdownloading = []
    #for document in training_phpdownloading_list:
    #    equality = docsimlarity.comp_descriptors (request_list, document)
    #    eqularity_phpdownloading.append(equality)
    
    eqularity_phpshell = []
    for document in training_phpshell_list:
        equality = docsimlarity.comp_descriptors (request_list, document)
        eqularity_phpshell.append(equality)
    
    print "phpbot="+str(docsimlarity.getMedian(eqularity_phpbot))
    print "phpecho="+str(docsimlarity.getMedian(eqularity_phpecho))
    #print docsimlarity.getMedian(eqularity_phpdownloading)
    print "phpshell="+str(docsimlarity.getMedian(eqularity_phpshell))
        
    
    
    #document_list = [document1]
    

