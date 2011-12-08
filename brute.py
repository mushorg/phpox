"""brute.py
brute.py opens sample php file and get words inside“  ”, and used
as data of botnet password dictionary info.
"""

import re
# 將sample打開
def open_sample(sample):
    with open(sample, "r") as sample_fp:
        sample_string = sample_fp.read()
    return sample_string
# 比對open_sample(sample)中的字串，只要是 " " 內的字串，就會被抓出來
def find_strings(sample):
    string_list = re.findall(r'"(.*?)"', open_sample(sample))
    return set(string_list)