"""brute.py
brute.py opens sample php file and get words inside double quotation marks, and used
as data of botnet password dictionary info.
"""

import re

def open_sample(sample):
    """open the sample,, strip it and return the context string"""
    with open(sample, "r") as sample_fp:
        sample_string = sample_fp.read()
    return sample_string

def find_strings(sample):
    """extract the string inside the double quotation marks in the context, and return them in the list"""
    string_list = re.findall(r'"(.*?)"', open_sample(sample))
    return set(string_list)