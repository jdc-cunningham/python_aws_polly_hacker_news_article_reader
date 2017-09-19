# import re

def url_link_replacer(str):

    s = str

    # links = re.findall('*)', s)

    # link_found = 'true'

    # in order of likelihood to occurr
    def for_slash_only_case(str):
        # global link_found
        if (str.find('://') != -1):
            return 'true'

    def www_case(str):
        # global link_found
        if (str.find('www.') != -1):
            return 'true'

    # http case
    def http_case(str):
        global link_found
        if (str.find('http://') != -1):
            return link_found

    def https_case(str):
        # global link_found
        if (str.find('https://') != -1):
            return 'true'

    url_cases = {
        0 : for_slash_only_case,
        1 : www_case,
        2 : http_case,
        3 : https_case
    }

    # url matching function
    def url_match(str):
        for case in url_cases:
            # run through cases
            url_found = url_cases[case](str)
            if (url_found == 'true'):
                return 'true'
                break

    str_text = s.split(' ')

    for index, text in enumerate(str_text):
        url_found = url_match(text)
        if (url_found == 'true'):
            # replace with link
            str_text[index] = 'link'

    s = ' '.join(str_text)


    return s
