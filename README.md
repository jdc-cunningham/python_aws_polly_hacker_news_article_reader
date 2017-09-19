# Read Top 10 Articles from Hacker News out loud with Python, AWS Polly and Raspberry Pi
Grabs top 10 articles from Hacker News and passes them to Amazon Polly with basic formatting (limit to 1500 chars) and plays through Raspberry Pi PWM audio output

## video
https://www.youtube.com/watch?v=fWfatVYML9o?t=23s

## requirements
* AWS Polly Account (free 5M characters per month)
  * Need AWSCLI with access key, secret key, region
* Raspberry Pi connected to internet
  * Low pass filter circuit (parts) if using Raspberry Pi Zero (no headphone jack) need resistor, capacitor, film capacitor
* Python Boto3 sdk

Currently this runs on Python 2.7.9 on Raspbian, but I was developing it on Python 3.7, in particular the HTML.Parser to unescape HTML may be problematic.

## Intro
After getting a taste of Amazon Polly's capability (text to speech synthesis) I wanted to make something that reads Hacker News' articles out loud. In general I like to read the comments not so much the link itself. The links also bring around the unknown page structure for scraping which is not my intent. So this script runs through crontab every hour and checks if my desktop is connected to the local network (if I'm home) as this desktop is usually off when I'm not home.

I have to be honest I had no idea what I was doing, I initially wanted to develop this with JavaScript but that didn't make sense as far as running it "back end" or "headless" and I'm not speaking for Node I currently don't use Node. I meant the regular client side JavaScript which would require a front end page being open to run the script... so I switched to Python entirely which I've never really used Python before so it was cool to learn some of it. I also apologize before hand if somehting looks really stupid like the url replacement. Initially the synthesizer would read every character in a URL outloud which quickly became annoying. There are also other random quirks to correct like reading a -> out loud as "minus greater than" or something like that.

## General steps
1) Get the data from Hacker News' API
  * get list of top stories: https://hacker-news.firebaseio.com/v0/topstories.json (outputs list of ids)
  * get title of story from individual story JSON https://hacker-news.firebaseio.com/v0/item/id.json (pass in id from above)
  * get top comment from individual story JSON above
  * concatenate into one string with line breaks for pauses in speech, and limit to 1500 characters (truncate comment if necessary)
  * some formatting, I've only implemented a url to the word "link" formatter
2) Pass data to Amazon Polly
  * Here is where I really did not know what I was doing, I went through a lot of their docs, but ultimately I stripped part of their server.py script and had to figure out how to write the streaming data into a file and got lucky.
  * This is where you need the AWS CLI to be setup correctly on your local system and then login to Amazon and generate a user (non-root) for an access key/secret key, and I just gave full permissions to Amazon Polly only
3) Go through a directories' contents and play sound
  * I needed to use pygame as several Stack Overflow threads mentioned it, in Windows I used os.start and it would use Groove to play the sound, not ideal with regard to Raspberry Pi/Headless
  * I just named the files 1.mp3, 2.mp3, etc... and limited to just 10 articles as reading an article outloud takes time
  * Every time it runs, it deletes the directory contents where the sound files are stored and recreates it (not ideal I realize).
  * I have a Pi Zero and they don't have a headphone jack so I used a tutorial by Adafruit to get sound to output through pin 13 (GPIO) and had to build a little low pass filter
  * the audio is surprisingly good I mean it's not playing music just speech but good enough, had to up the volume using a command amixer sset PCM,0 200%
  * link: https://learn.adafruit.com/adding-basic-audio-ouput-to-raspberry-pi-zero/pi-zero-pwm-audio
  
## Closing thoughts

Yeah it's pretty cool, I got all of my "goals" accomplished, I had to build a lot of random small things and then join it together I apologize if the code looks trash (it most likely does) I am new to Python need to improve/optimize code in general.

It's kind of funny, now that I have it I don't know if I actually want to keep it. The voice kind of drones on, in my opinion the Kendra voice ID is good, I do have a preference for female voices. But the "Lexicons" could use work but I have no idea about that at this time. In particular the questions, has that general "raise voice at the end" pattern and it doens't work, usually I just leave out question marks in a question but that's not implemented in this code.

## Files
Aside from all of the imports generally there are just two files, the main file read-articles-2.7.9-cp2.py and findurls.py to replace full urls with the word 'link'

