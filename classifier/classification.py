import docsimlarity
import matrix_training
import sys, os
import getopt
import json


    
def similarity_docrequest(classifier, request_list_dump, similarity_list):
    request_list_load = json.loads(request_list_dump)
    fh = open("classifier/trainset/"+classifier+"/"+classifier+"_matrix")
    for linestr in fh.readlines():
        dictall = json.loads(linestr)
        for documentlist in dictall.keys():
            equality = docsimlarity.comp_descriptors (request_list_load, dictall[documentlist])
            similarity_list.append(equality)
    return similarity_list

def ranking_similarity(setpath, similarity_phpbot, similarity_phpecho, similarity_phpdownloading, similarity_phpshell):
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
        if (max(getMedian_prob_list) > 0.6) or (max(max_prob_list) > 0.80) :
            strprint = "Clear Classification:"
            if max_prob_list.index(max(max_prob_list)) == 0:
                addtrainset("cp " + setpath+" classifier/trainsamples/phpbot/")
                strprint = strprint + "phpbot" +"\nSimilarity:" + str(max(max_prob_list))
                
                #print "mv " + docpath+"/"+sample + " trainset/phpbot/"
            elif max_prob_list.index(max(max_prob_list)) == 1:              
                addtrainset("cp " + setpath+" classifier/trainsamples/phpecho/")
                strprint = strprint + "phpecho" + "\nSimilarity:" + str(max(max_prob_list))
                
            elif max_prob_list.index(max(max_prob_list)) == 2:              
                addtrainset("cp " + setpath+" classifier/trainsamples/phpdownloading/")
                strprint = strprint + "phpdownaloding" + "\nSimilarity:" +  str(max(max_prob_list))
                
            else:
                addtrainset("cp " + setpath+" classifier/trainsamples/phpshell/")
                strprint = strprint + "phpshell" + "\nSimilarity:" +  str(max(max_prob_list))
            
            print strprint
            
        else:
            addtrainset("cp " + setpath + " classifier/trainsamples/checking/")
            print  "Possible Classification: " + str(max_prob_list.index(max(max_prob_list))) + "  Similarity:" + str(max(max_prob_list))
            
    else:
            print "Ambiguous classification:"+ str(getMedian_prob_list.index(max(getMedian_prob_list)))+" v.s " + str(max_prob_list.index(max(max_prob_list)))
            addtrainset("cp " + setpath+ " classifier/trainsamples/others/")
            
          
   
def addtrainset(command):
    os.system(command)
    #    print getMedian_prob_list.index(max(getMedian_prob_list)

def redo_trainset(classobj):
    """Generate Trainset for phpbot, phpshell, phpdownloading, phpshell. If you need to update training matrix, please remove comment!"""
    #matrix_training.getTrainset("phpbot")
    #matrix_training.getTrainset("phpshell")
    #matrix_training.getTrainset("phpdownloading")
    #matrix_training.getTrainset("phpecho")
    matrix_training.getTrainset(classobj)

def classifier_start(opts):                                        
    print "File Classifier Starting based on document similarity "
    #opts  = getopt.getopt(sys.argv[1], "v", [])
    request_list = {}
    request_list_dump = matrix_training.wordlist_docrequest(opts, request_list)
        
    similarity_phpbot = []
    similarity_phpdownloading = []
    similarity_phpecho = []
    similarity_phpshell = []
    similarity_others = []
    
    # Calculate similarity of documents
    similarity_phpbot = similarity_docrequest("phpbot", request_list_dump, similarity_phpbot)
    similarity_phpdownloading = similarity_docrequest("phpdownloading", request_list_dump, similarity_phpdownloading)
    similarity_phpecho = similarity_docrequest("phpecho", request_list_dump, similarity_phpecho)
    similarity_phpshell = similarity_docrequest("phpshell", request_list_dump, similarity_phpshell)
    
    numcase = ranking_similarity(opts, similarity_phpbot, similarity_phpecho, similarity_phpdownloading, similarity_phpshell)
    return numcase
    #document_list = [document1]


