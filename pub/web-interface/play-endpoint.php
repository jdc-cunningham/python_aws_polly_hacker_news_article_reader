<?php

    // at this time this endpoint is only designed to trigger playback
    // may look into pause/play in the future

    error_log('play-endpoint.php ran');
    error_log(exec('whoami'));

    if ($_SERVER['REQUEST_METHOD'] == 'POST') {

        $play_command = $_POST['play_command'];

        $state_return = [];

        error_log('play command: ' . $play_command);

        if ($play_command == 'play') {

            // read hn_reader_running.txt
            $play_state = file_get_contents('/home/pi/articleBot/hn_reader_running.txt', true);

            // $play_state = 'no';

            error_log('play state: ' . $play_state);

            if ($play_state == 'no') {
                // change file
                $myfile = fopen('play_state.txt', "w") or die("Unable to open file");
                $txt = "play";
                fwrite($myfile, $txt);
                fclose($myfile);
                error_log('if ran: no');
                // hn reader currently not playing, play
                // exec('/usr/bin/python /home/pi/articleBot/hn_article_top_comment_reader_no_ip.py');
                // shell_exec('/home/pi/articleBot/hn_article_top_comment_reader_no_ip.py');
                $state_return['state'] = 'hn reader started';

                // non-ending loop safety close
                if ($play_state == 'no') {
                    
                    sleep(10); // in ten seconds update play_state.txt

                    $myfile = fopen('play_state.txt', "w") or die("Unable to open file");
                    $txt = "off";
                    fwrite($myfile, $txt);
                    fclose($myfile);
                    
                }

            }
            else if ($play_state == 'yes') {
                error_log('if ran: yes');
                $myfile = fopen('play_state.txt', "w") or die("Unable to open file");
                $txt = "off";
                fwrite($myfile, $txt);
                fclose($myfile);
                // don't play
                $state_return['state'] = 'hn reader currently playing';
            }

            echo json_encode($state_return);

            error_log('bottom reached');

        }

    }