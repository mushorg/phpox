# Copyright (C) 2012  Lukas Rist
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import re
import math
import os
import os.path
from stripogram import html2text


def fileio(filename):
    fh = open(filename)
    gettext = fh.readlines()
    fh.close()
    return gettext


def filewrite(filename, strlist):
    fh = open(filename, 'w')
    fh.write(strlist)
    fh.close()


def textread(content):
    strtext = html2text(str(content))
    strtext = strtext.replace('\n', " ")
    strtext = strtext.replace('\"', "")
    strtext = strtext.replace('\'', "")
    strtext = strtext.lower()
    return strtext


def tf_text(strtext):
    "calculates the term frequency for a given text"
    #split the line and return list of words
    tokens = re.compile(r"[\w']+")
    words = tokens.findall(strtext)
    wordlist = {}
    for i in words:
        frequency = 0
        if i in wordlist:
            frequency = wordlist[i]
        frequency = frequency + 1
        wordlist[i] = frequency
    return wordlist


def tf_text_key(tf_wordlist):
    return tf_wordlist.keys()


def getMedian(numericValues):
    theValues = sorted(numericValues)
    if len(theValues) % 2 == 1:
        return theValues[(len(theValues) + 1) / 2 - 1]
    else:
        lower = theValues[len(theValues) / 2 - 1]
        upper = theValues[len(theValues) / 2]
        return (float(lower + upper)) / 2


def convert_list_into_dictionary(original, init_value):
    "converts a list into a dictionary"
    result = {}
    list_size = len(original)
    for item in range(list_size):
        left_value = original[item]
        result[left_value] = init_value
    return result


def comp_descriptors(document1, document2):
    "returns the degree of equality between two documents (often a request and a document)"
    equality = 0
    items_document1 = len(document1)
    items_document2 = len(document2)
    #document1_dict = convert_list_into_dictionary(document1, 0)
    #document2_dict = convert_list_into_dictionary(document2, 0)
    similar_descriptors = 0

    for item in document1.keys():
        if item in document2:
            similar_descriptors += 1
    # calculate equality
    try:
        equality = float(similar_descriptors) / float((math.sqrt(items_document1) * math.sqrt(items_document2)))
        return equality
    except ZeroDivisionError as e:
        #print "float division by zero"
        return 0


def document_rank(request, document_list, order):
    "ranks the given documents according to the equality of their descriptors with the request"
    ranking_list = []
    list_no = 0
    for document in document_list:
        equality = comp_descriptors(request, document)
        ranking_entry = {
            "descriptors": document,
            "equality": equality,
            "list_no": list_no
        }
        list_no += 1

        # search for an appropiate place to insert new entry (binary search)
        list_length = len(ranking_list) - 1
        right = list_length
        left = 0

        if(right == -1):
            # still an empty ranking list
            ranking_list.append(ranking_entry)
        else:
            if (ranking_list[left]["equality"] <= equality):
                ranking_list = [ranking_entry] + ranking_list
                continue
            # end if
            if (ranking_list[right]["equality"] >= equality):
                ranking_list.append(ranking_entry)
                continue
            # end if

            while (right > left):
                middle = (right + left) / 2
                value = ranking_list[middle]["equality"]

                if (value <= equality):
                    right = middle
                else:
                    left = middle + 1
                # end if
            # end while
            ranking_list = ranking_list[:middle + 1] + [ranking_entry] + ranking_list[middle + 1:]
        # end if
    # end for

    if (order == 1):
        # not descending
        new_ranking_list = []
        for item in ranking_list:
            new_ranking_list = [item] + new_ranking_list
        ranking_list = new_ranking_list
    # end if
    return ranking_list
