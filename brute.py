def open_sample(sample):
    with open(sample, "r") as sample_fp:
        sample_string = sample_fp.read().split("\r")
    return sample_string

def find_strings(sample_string):
    string_list = []
    for line in sample_string:
        if '"' in line:
            line_list = line.split("\"")
            for item in line_list:
                string_list.append(item.strip())
    return set(string_list)
