import docsimlarity
import sys, os
import getopt

def wordlist_train(dirpath, listall):
    list_scripts = os.listdir(dirpath)
    for sample in list_scripts:
        gettext = docsimlarity.fileio(dirpath+sample)
        gettext = docsimlarity.textread(gettext)
        listall.append(docsimlarity.tf_text(gettext))
    return listall

def wordlist_docrequest(docpath, request_list):
    gettext = docsimlarity.fileio(docpath)
    gettext = docsimlarity.textread(gettext)
    request_list = docsimlarity.tf_text(gettext)
    return request_list
    
def similarity_docrequest(training_list, request_list, similarity_list):
    for document in training_list:
        equality = docsimlarity.comp_descriptors (request_list, document)
        similarity_list.append(equality)
    return similarity_list

def ranking_similarity(similarity_phpbot, similarity_phpecho, similarity_phpdownloading, similarity_phpshell):
    getMedian_prob_list = []
    max_prob_list = []
    
    getMedian_prob_list.append(docsimlarity.getMedian(similarity_phpbot))
    max_prob_list.append(max(similarity_phpbot))
    
    getMedian_prob_list.append(docsimlarity.getMedian(similarity_phpecho))
    max_prob_list.append(max(similarity_phpecho))
    
    getMedian_prob_list.append(docsimlarity.getMedian(similarity_phpdownloading))
    max_prob_list.append(max(similarity_phpdownloading))
    
    getMedian_prob_list.append(docsimlarity.getMedian(similarity_phpshell))
    max_prob_list.append(max(similarity_phpshell))
    
    print "Median_Similarity:"+ str(getMedian_prob_list)
    print "Maximum_Similarity:" + str(max_prob_list)
    
    if getMedian_prob_list.index(max(getMedian_prob_list)) == max_prob_list.index(max(max_prob_list)):
        if (max(getMedian_prob_list) > 0.6) or (max(max_prob_list) > 0.85) :
            strprint = "Clear Classification:"
            if max_prob_list.index(max(max_prob_list)) == 0:
                addtrainset("mv " + setpath+"/"+sample + " trainset/phpbot/")
                strprint = strprint + "phpbot" +"\nSimilarity:" + str(max(max_prob_list))
                #print "mv " + docpath+"/"+sample + " trainset/phpbot/"
            elif max_prob_list.index(max(max_prob_list)) == 1:              
                addtrainset("mv " + setpath+"/"+sample + " trainset/phpecho/")
                strprint = strprint + "phpecho" + "\nSimilarity:" + str(max(max_prob_list))
            elif max_prob_list.index(max(max_prob_list)) == 2:              
                addtrainset("mv " + setpath+"/"+sample + " trainset/phpdownloading/")
                strprint = strprint + "phpdownaloding" + "\nSimilarity:" +  str(max(max_prob_list))
            else:
                addtrainset("mv " + setpath+"/"+sample + " trainset/phpshell/")
                strprint = strprint + "phpshell" + "\nSimilarity:" +  str(max(max_prob_list))
            
            print strprint
            
        else:
            addtrainset("mv " + setpath+"/"+sample + " trainset/checking/")
            print  "Possible Classification" + str(max_prob_list.index(max(max_prob_list))) + "  Similarity:" + str(max(max_prob_list))
            #return 0
    else:
            print "Ambiguous classification:"+ str(getMedian_prob_list.index(max(getMedian_prob_list)))+" v.s " + str(max_prob_list.index(max(max_prob_list)))
            addtrainset("mv " + setpath+"/"+sample + " trainset/others/")
            print "We cannot classify properly. Need human inspection! "
            #return 2
   
def addtrainset(command):
    os.system(command)
    #    print getMedian_prob_list.index(max(getMedian_prob_list)
                                        
if __name__ == '__main__':
    print "File Classifier Starting based on document similarity "
    opts  = getopt.getopt(sys.argv[1], "v", [])
    
    setpath = "/home/julia/projects/php_sandbox/classifier/"
    docpath = setpath + opts[1]
    sample = opts[1]
    phpbot_trainpath = setpath + "trainset/phpbot/"
    phpdownloading_trainpath = setpath + "trainset/phpdownloading/"
    phpshell_trainpath = setpath + "trainset/phpshell/"
    phpecho_trainpath = setpath + "trainset/phpecho/"
    
    # Training Class List 
    training_phpbot_list = []
    training_phpdownloading_list = []
    training_phpecho_list = []
    training_phpshell_list = []
    
    training_phpbot_list = wordlist_train(phpbot_trainpath, training_phpbot_list)
    training_phpdownloading_list = wordlist_train(phpdownloading_trainpath, training_phpdownloading_list)
    training_phpecho_list = wordlist_train(phpecho_trainpath, training_phpecho_list)
    training_phpshell_list = wordlist_train(phpshell_trainpath, training_phpshell_list)
    
    #doc_all = os.listdir(docpath)
    #for sample in doc_all:
    #print docpath+"/"+sample
        
    similarity_phpbot = []
    similarity_phpdownloading = []
    similarity_phpecho = []
    similarity_phpshell = []
    similarity_others = []
    request_list = []
    request_list = wordlist_docrequest(setpath+"/"+opts[1], request_list)
        
    # Calculate similarity of documents
    similarity_phpbot = similarity_docrequest(training_phpbot_list, request_list, similarity_phpbot)
    similarity_phpdownloading = similarity_docrequest(training_phpdownloading_list, request_list, similarity_phpdownloading)
    similarity_phpecho = similarity_docrequest(training_phpecho_list, request_list, similarity_phpecho)
    similarity_phpshell = similarity_docrequest(training_phpshell_list, request_list, similarity_phpshell)
    
    numcase = ranking_similarity(similarity_phpbot, similarity_phpecho, similarity_phpdownloading, similarity_phpshell)
        
    print "#######################################################################"
    #document_list = [document1]
    

