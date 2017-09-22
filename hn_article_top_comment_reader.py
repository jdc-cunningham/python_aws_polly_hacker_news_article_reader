# import for ping, file writing
import os

# do a check first if dekstop is online
hostname = '192.XXX.XXX.XXX'
response = os.system('ping -c 1 ' + hostname)
if response == 0:

    # import for data grab
    import requests
    import json
    import HTMLParser
    parser = HTMLParser.HTMLParser()
    import re

    # import for replacing full urls with word link
    from findurls import url_link_replacer

    # import for directory clearing
    import shutil
    
    # imnport for playing sound
    import pygame
    # initialize pygame for audio playback
    pygame.mixer.init()
    
    # import for AWS CLI
    from boto3 import Session

    # import for text to speech, requires AWS CLI configured
    session = Session(profile_name="adminuser")
    polly = session.client("polly")
    voiceID = "Kendra"
    outputFormat = "mp3"
    CHUNK_SIZE = 1024
    
    # import sys for sys.exit
    import sys

    # get top article ids
    get_top_article_ids_req = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    article_ids_json = (get_top_article_ids_req.content.decode('utf-8'))

    # remove left and right brackets [ ]
    article_ids_json = article_ids_json.replace('[','')
    article_ids_json = article_ids_json.replace(']', '')

    article_ids = article_ids_json.split(',')

    counter = 0

    synth_counter = 0

    synthesize = []

    previous_articles_new = {}

    # this is for the total synthesized file check up to 30
    # make sure not to overwrite articles that have already been synthesized by erasing/creating new previous_articles
    have_synth = {}

    # function for getting article data
    def get_article_top_comment(article_top_comment_id):

        # get article top comment
        article_comment_json_req = requests.get('https://hacker-news.firebaseio.com/v0/item/' + str(article_top_comment_id) + '.json')
        article_comment_json_cont = article_comment_json_req.content.decode('utf-8')
        article_comment_json_loaded = json.loads(article_comment_json_cont)
        article_top_comment_unescaped = parser.unescape(article_comment_json_loaded['text'])
        article_top_comment_html_stripped = re.sub('<[^<]+?>', '', article_top_comment_unescaped)
        article_top_comment = article_top_comment_html_stripped

        return article_top_comment

    for article_id in article_ids:

        # counter max range of 30
        counter = counter + 1
        if (counter < 30):

            # synth counter max range of 10
            # this is the "true" count with regard to synthesizing up to 10 new/changed data
            # specifically if the comment has changed
            if (synth_counter < 10):

                # get top comment if it exists
                article_details_req = requests.get('https://hacker-news.firebaseio.com/v0/item/' + article_id + '.json')
                article_details_json_cont = article_details_req.content.decode('utf-8')
                article_details_json_loaded = json.loads(article_details_json_cont)

                # check for comment
                if 'kids' in article_details_json_loaded:

                    # get id of top comment (first)
                    article_comments = article_details_json_loaded['kids']
                    article_top_comment_id = article_comments[0]

                    # check local text file previous_articles.txt
                    # limit to 10 playing but range from 1 to 30 based on change

                    # empty dict
                    empty_dict = {}

                    # check if previous_articles.txt doesn't exist
                    if not (os.path.isfile('previous_articles.txt')):

                        filename = 'previous_articles.txt'
                        f = open(filename, 'wb')

                        # initialize with empty dict
                        # check if empty
                        if (os.stat('previous_articles.txt').st_size == 0):
                            # write empty json
                            json.dump(empty_dict, open('previous_articles.txt', 'w'))

                        # no reference assume first time, go from 1 to 10
                        # this if branch runs once

                        # get article title
                        article_title = article_details_json_loaded['title']
                        
                        # get article top comment
                        article_top_comment = get_article_top_comment(article_top_comment_id)
                        
                        # add to list to be synthesized
                        # tried to use dictionary but ran into double encoding problems, using random [split]
                        # I remove the . because it's read out loud as dot
                        synthesize.append(article_title + '[split]' + url_link_replacer(article_top_comment).replace('.', ''))

                        # update synth_counter
                        synth_counter = synth_counter + 1

                        # update previous_articles_new
                        previous_articles_new[article_id] = article_top_comment_id

                    else:
                        
                        # file exists, check for changes
                        # first if this article_id is in the previous_articles
                        # if it is, check if the article_topC-omment_id is the same
                        # if it is not the same, add this to the list to be synthesized

                        # check if previous_articles is empty
                        if (os.stat('previous_articles.txt').st_size == 0):
                            # write empty json
                            json.dump(empty_dict, open('previous_articles.txt', 'w'))

                        # load previous_articles.txt
                        previous_articles = json.load(open('previous_articles.txt'))
                        have_synth = previous_articles

                        # check if current article_id in previous_articles
                        if (article_id in previous_articles):

                            # article_id exists, check article_top_comment_id same as one in previous_articles
                            if (previous_articles[article_id] != article_top_comment_id):

                                # get article title
                                article_title = article_details_json_loaded['title']
                                
                                # get article top comment
                                article_top_comment = get_article_top_comment(article_top_comment_id)
                                
                                # add to list to be synthesized
                                # synthesize.append({article_title:article_top_comment})
                                synthesize.append(article_title + '[split]' + url_link_replacer(article_top_comment).replace('.', ''))

                                # update synth_counter
                                synth_counter = synth_counter + 1

                                # update previous_articles_new
                                previous_articles_new[article_id] = article_top_comment_id
                                # print article_id

                        else:

                            # article_id doesn't exist, add to synthesized

                            # get article title
                            article_title = article_details_json_loaded['title']
                            
                            # get article top comment
                            article_top_comment = get_article_top_comment(article_top_comment_id)

                            # add to list to be synthesized
                            # synthesize.append({article_title:article_top_comment})
                            synthesize.append(article_title + '[split]' + url_link_replacer(article_top_comment).replace('.', ''))

                            # update synth_counter
                            synth_counter = synth_counter + 1

                            # update previous_articles_new
                            previous_articles_new[article_id] = article_top_comment_id

            else:

                # stop loop
                break
              
    # define play_sound (this was originally located farther down)
    def play_sound_file(sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
              
    # check if content is 0
    if (len(synthesize) == 0):
      
        # play empty greeting if it exists, otherwise wait for it to be generated/played and terminate below
        if (os.path.isfile('predefined-sounds/no-new-content.mp3')):
          play_sound_file('predefined-sounds/no-new-content.mp3')
        
        # stop execution
        sys.exit()

    # request synth

    # function to synthesize text to speech
    def synth_text(text_to_synth, save_location, file_name):
      
        # global variables
        global polly, session, VoiceID, OuputFormat

        # limiter
        text_len = len(text_to_synth)
        
        if (text_len > 1500):

            # handle error, will truncate
            
            # truncate, the words and spaces for ' content truncated' takes up 18 characters
            # line breaks eg. \n count as 1 character, use two for a good pause between content if needed
            trunc_len = 1482
            
            text_to_synth = text_to_synth[:trunc_len] + ' content truncated'

        # synthesize
        response = polly.synthesize_speech(Text=text_to_synth,VoiceId=voiceID,OutputFormat=outputFormat)
        data_stream = response.get("AudioStream")
        
        # check save_location file, create if it doesn't exist
        if not os.path.exists(save_location):
          os.makedirs(save_location)

        f = open(save_location+'/' + file_name, 'wb')

        while True:
            # stream data
            data = data_stream.read(CHUNK_SIZE)
            # write data
            f.write(data)
            # stop stream if no more data
            if not data:
                break

    # check if predefined-sounds exist
    # create predefined sounds folder
    if not os.path.exists('predefined-sounds'):
        os.makedirs('predefined-sounds')

        # Create list of statements
        statement_list = [
            "Here are some new article comments from Hacker News",
            "Here is an article comment from Hacker News",
            "There are no new article comment changes since last check",
            "Top comment",
            "Title",
            "Number",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10"
        ]

        # synthesize the list items above, setting file name as list string item to lower case concatenated with -
        for i in range(len(statement_list)):
        
          text = statement_list[i]
          response = polly.synthesize_speech(Text=text,VoiceId=voiceID,OutputFormat=outputFormat)
          data_stream = response.get("AudioStream")

          # change name (decrease length) for a couple list items
          if (text == 'Here are some new article comments from Hacker News'):
              filename = 'more-than-one' + ".mp3"
          elif (text == 'Here is an article comment from Hacker News'):
              filename = 'only-one.mp3'
          elif (text == 'There are no new article comment changes since last check'):
              filename = 'no-new-content.mp3'
          else:
              filename = statement_list[i].lower().replace(' ', '-') + ".mp3"
              
          synth_text(text, 'predefined-sounds', filename)

    # check if content is 0
    if (len(synthesize) == 0):
      
        # play empty greeting
        play_sound_file('predefined-sounds/no-new-content.mp3')
        
        # stop execution
        sys.exit()

    # loop through content, synthesize then play

    # check if sound-files folder exists
    if not os.path.exists('sound-files'):
        os.makedirs('sound-files')
    else:
        # empty (deletes folder, need to recreate)
        shutil.rmtree('sound-files')
        os.makedirs('sound-files')

    # this is for the narration counter
    synth_inner_counter = 0
    
    # print json.dumps(synthesize).encode('utf-8')

    for synthesize_article_title in synthesize:

        synth_inner_counter = synth_inner_counter + 1

        synth_article_title_comment_pair = synthesize_article_title
        
        synth_article_title_comment_pair_split = synth_article_title_comment_pair.split('[split]')
        synth_article_title = synth_article_title_comment_pair_split[0].replace('{', '')
        synth_article_comment = synth_article_title_comment_pair_split[1].replace('}', '')
        
        synth_text(synth_article_title, 'sound-files', str(synth_inner_counter) + '-title.mp3')
        synth_text(synth_article_comment, 'sound-files', str(synth_inner_counter) + '-comment.mp3')

        # play the content
        if (synth_inner_counter == 1):
            # first run
            # check count
            synth_cont_len = len(synth_article_title_comment_pair)
            if (synth_cont_len == 0):
                greeting = 'predefined-sounds/'+'no-new-content.mp3'
            elif (synth_cont_len > 1):
                greeting = 'predefined-sounds/'+'more-than-one.mp3'
            else:
                greeting = 'predefined-sounds/'+'only-one.mp3'
    
    # play intro greeting
    play_sound_file(greeting)
    
    # limit play back
    play_counter = 0

    # define and run play_sound_file function until no more content to play
    def play_sound_file_loop(sound_file, cur_file_num):
      
        global play_counter
        
        play_counter = play_counter + 1
        
        if (play_counter > synth_inner_counter):
            return
        
        # play the word "number"
        play_sound_file('predefined-sounds/'+'number.mp3')

        # play the actual number
        play_sound_file('predefined-sounds/'+str(cur_file_num)+'.mp3')

        # play the word "title"
        play_sound_file('predefined-sounds/title.mp3')

        # play the article title
        play_sound_file('sound-files/'+str(cur_file_num)+'-title.mp3')
        
        # top comment
        play_sound_file('predefined-sounds/top-comment.mp3')

        # play the comment
        play_sound_file('sound-files/'+str(cur_file_num)+'-comment.mp3')

        # play next article title comment pair
        cur_file_num = cur_file_num + 1
        play_sound_file_loop('sound-files/'+str(cur_file_num)+'.mp3', cur_file_num)

    # start playing sound files
    play_sound_file_loop('sound-files/1.mp3', 1)

    # after synth write to previous_articles.txt
    have_synth.update(previous_articles_new)
    json.dump(have_synth, open('previous_articles.txt', 'w'))
    
else:
    
    # reset previous_files.txt
    empy_dict = {}
    # write empty json
    json.dump(empty_dict, open('previous_articles.txt', 'w'))
