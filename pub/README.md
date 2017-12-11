# Hacker News Article Top Comment Reader (Web Triggered Version)
## With Raspberyr Pi, Amazon Polly on Python

The original version was triggered by a set interval through CRON. In my case I was running it every 2 hours. I eventually found this to be quite distracting as having to stop what you're doing and listen for up to 10 minutes...

So I opted for a web version. This version is not great, I just wanted to get the job done and here it is.

It still technically runs on CRON except all that does is make sure a thread is running, which listens for a file change from PHP through the web interface which is a simple "click to run".

## Note

The contents have to extracted into their appropriate locations eg. front-end code goes into ```/var/www/html``` and back-end goes into ```/home/pi/articleBot``` as specified by the two folders in this branch

### How does it work?

The base code is pretty much the same as before, in fact you need to keep the same directory/permissions. I primarily made a copy of the hn_article_top_comment_reader.py module and named the copy to hn_article_top_comment_reader_no_ip.py As the file name states, this version has no ip dependency (checking if some machine on local network is connected).

This version requires you to click on a basic web interface and it changes the file. Then a back-end process that is polling picks up that change and runs the back-end commands. The primary problem is the inability to acces the /home directory and audio with pygame. I tried differnt things, did not figure it out. This works for me at this time.

There is a prevent-double play catch on the front and back end. I ran into that problem while getting this version to run. The playback ran multiple times and had voice overlap.

### Problems

I have not come up with a reset at this time, so if you have to restart the thread(s), you will have to kill all instance(s) of waiting-thread.py and poll-thread.py

>pkill -f poll-thread.py
>pkill -f waiting-thread.py

Then you have to reset the state files to their "off" positions

(front-end)
play_state.txt -> off

(back-end)
poll_started.txt -> no
hn_reader_running.txt -> no

### Things to note

This largely depends on the original version/having that working/understanding requirements like the AWS CLI. The required folders and common re-used sound files should be generated automatically provided the write permissions are in place.

The other big thing (really biggest problem I think) is the file permissions settings.

>/var/www/html

Both ```web-interface.html``` and ```play-endpoint.php``` are owned by pi:pi and have 644 permissions 
```play_state.txt``` is owned by www-data in order to change it (read write) and has 755 permission or I may have used chmod +x


>/home/pi/articleBot

Everything should be owned by pi:pi and have 644 for files and 755 for directories

This is because the back-end process is started by the Raspberry Pi rather than Apache/front-end.
