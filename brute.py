import re
def open_sample(sample):
    with open(sample, "r") as sample_fp:
        sample_string = sample_fp.read()
    return sample_string

def find_strings(sample):
    string_list = re.findall(r'"(.*?)"', open_sample(sample))
    return set(string_list)