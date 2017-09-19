import os

# do a check first if dekstop is online
hostname = '192.###.###.###'
response = os.system('ping -c 1 ' + hostname)
if response == 0:
    # desktop is up, continue

    import requests
    import json
    # import html
    import HTMLParser
    parser = HTMLParser.HTMLParser()
    import re
    import pygame
    from boto3 import Session
    # import os # directory creation
    import shutil # delete directory contents
    from findurls import url_link_replacer
    session = Session(profile_name="adminuser")
    polly = session.client("polly")
    text = ""
    text = text.encode('utf-8')
    voiceID = "Kendra"
    outputFormat = "mp3"
    CHUNK_SIZE = 1024

    # Get data from HN, limit to 10 articles

    # get top articles
    article_ids = [0] * 10 
    get_top_article_ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    python_list = [0] * 10
    python_list = (get_top_article_ids.content.decode('utf-8'))
    # remove [ and ]
    s_clean_left = python_list.replace('[','')
    s_clean_right = s_clean_left.replace(']', '')
    list_article_ids = s_clean_right.split(',')
    counter = 0

    # article_dictionary = {} works

    synthesize_text = "Here are the top articles from Hacker News \n\n"
    synthesize_text_2 = "" # this is for in case the next set added is greater than 1500 characters, I should trim comments
    synthesize_text_ph = "" # placeholder for sum check

    # delete directory contents
    if os.path.exists('sound-files2'):
        shutil.rmtree('sound-files2')
        os.makedirs('sound-files2')

    if not os.path.exists('sound-files2'):
        os.makedirs('sound-files2')

    # print (s_list)
    for article_id in list_article_ids:
        # break # skip this for now
        # loop counter
        counter = counter + 1
        if (counter > 10):
            break
        else:

            article_json_req = requests.get('https://hacker-news.firebaseio.com/v0/item/' + article_id + '.json')
            article_json_cont = article_json_req.content.decode('utf-8')
            article_json_loaded = json.loads(article_json_cont)
            article_title = article_json_loaded['title']
            if 'kids' in article_json_loaded:
                article_comments = article_json_loaded['kids']
                article_top_comment_id = article_comments[0]
                article_comment_json_req = requests.get('https://hacker-news.firebaseio.com/v0/item/' + str(article_top_comment_id) + '.json')
                article_comment_json_cont = article_comment_json_req.content.decode('utf-8')
                article_comment_json_loaded = json.loads(article_comment_json_cont)
                article_top_comment = parser.unescape(article_comment_json_loaded['text'])
                article_top_comment_html_stripped = re.sub('<[^<]+?>', '', article_top_comment)
                synthesize_text += "Number " + str(counter) + "\n\n" + " title " + "\n\n" + article_title + "\n\n top comment \n\n"

                # check current length
                syn_text_len = len(synthesize_text)
                comment_len = 1476 - int(syn_text_len)
                if (int(len(article_top_comment_html_stripped)) < comment_len):
                    synthesize_text += url_link_replacer(article_top_comment_html_stripped) + "\n\n"
                else:
                    synthesize_text += url_link_replacer(article_top_comment_html_stripped[:comment_len]) + " comment truncated\n\n"

            # synthesize text and save audio file
            text = synthesize_text
            response = polly.synthesize_speech(Text=text,VoiceId=voiceID,OutputFormat=outputFormat)
            data_stream = response.get("AudioStream")

            filename = str(counter) + ".mp3"
            # f=file(filename, 'wb')
            f = open('sound-files2/' + filename, 'wb')

            while True:
                # stream data
                data = data_stream.read(CHUNK_SIZE)
                # write data
                f.write(data)
                # stop stream if no more data
                if not data:
                    break

            synthesize_text = "" # reset
            continue

    # read and sort sound-files directory
    sound_files = os.listdir('sound-files')
    new_list = []

    for sound_file in sound_files:
        # print (sound_file)
        new_list.extend([sound_file.replace('.mp3', '')])
        # print (new_list)

    # sort array
    new_list = [int(x) for x in new_list]
    new_list.sort()

    # print (new_list)

    last_list = []

    # rebuild files
    for file_num in new_list:
        # print (sound_file)
        last_list.append(str(file_num) + '.mp3')

    # create function to loop over playing sound files
    pygame.mixer.init() # think I only have to do this once
    def play_sound_file(sound_file, cur_file_num):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        else:
            if (cur_file_num < 10):
                # play next song
                cur_file_num = cur_file_num + 1
                play_sound_file('sound-files2/'+str(cur_file_num)+'.mp3', cur_file_num)

    # start playing sound files
    play_sound_file('sound-files2/1.mp3', 1)
