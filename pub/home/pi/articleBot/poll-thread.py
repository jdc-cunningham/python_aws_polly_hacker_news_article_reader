import os, time

def polling_file_read_function():

    global os, time

    while True:
        str = open('/var/www/html/hn-article-bot/play_state.txt', 'r').read()
        if (str == 'play'):
            
            playback_in_progress = open('/home/pi/articleBot/hn_reader_running.txt', 'r').read()

            # run only once
            if (playback_in_progress == 'no'):
                # update playback_in_progress
                f = open('/home/pi/articleBot/hn_reader_running.txt', 'w')
                f.write('yes')
                f.close()
                # start playing process
                os.system('/usr/bin/python /home/pi/articleBot/hn_article_top_comment_reader_no_ip.py')
        print('hn reader polling...')
        time.sleep(1)

# start function
polling_file_read_function()