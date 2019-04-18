#!/usr/bin/python

# Script originally provided by AlekseyP
# https://www.reddit.com/r/technology/comments/43fi39/i_set_up_my_raspberry_pi_to_automatically_tweet/
# modifications by roest - https://github.com/roest01
# addition of fast-cli support by jmhbnz - https://github.com/jmhbnz

import os
import csv
import datetime
import time

def runSpeedtest():

        #run speedtest-cli
        print('--- running speedtest ---')
        speedtestCommand= "speedtest-cli --simple"

        if "SPEEDTEST_COMMAND" in os.environ:
            speedtestCommand= os.environ.get('SPEEDTEST_COMMAND')

        if "SPEEDTEST_PARAMS" in os.environ:
            extraParams_= os.environ.get('SPEEDTEST_PARAMS')
            speedtestCommand= speedtestCommand + " " + extraParams_
            print('speedtest with extra parameter: ' + speedtestCommand)
        else:
            print('running with default server')




        a = os.popen(speedtestCommand).read()
        print('ran ', speedtestCommand)

        #split the results into lines
        #speedtest-cli has three rows (ping, download, upload)
        #fast-cli has two rows (download, upload)
        lines = a.split('\n')
        print(a)
        ts = time.time()
        date =datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M:%S')
        print(date)

        #start with default values for speeds
        p = 100
        d = 0
        u = 0


        #if speedtest could not connect set the speeds to 0
        if "Cannot" in a:
                p = 100
                d = 0
                u = 0
        #extract the values for ping down and up values
        else:
                if (os.environ.get('SPEEDTEST_COMMAND') == 'fast'):
                        d = lines[0].split(' ')[0]
                elif (os.environ.get('SPEEDTEST_COMMAND') == 'fast --upload'):
                        d = lines[0].split(' ')[0]
                        u = lines[1].split(' ')[0]
                else:
                        p = lines[0][6:11]
                        d = lines[1][10:14]
                        u = lines[2][8:12]
        print(date,p, d, u)
        #save the data to file for local network plotting
        filepath = os.path.dirname(os.path.abspath(__file__))+'/../data/result.csv'
        fileExist = os.path.isfile(filepath)

        out_file = open(filepath, 'a')
        writer = csv.writer(out_file)

        if fileExist != True:
                out_file.write("timestamp,ping,download,upload")
                out_file.write("\n")

        writer.writerow((ts*1000,p,d,u))
        out_file.close()

        return

if __name__ == '__main__':
        runSpeedtest()
        print('speedtest complete')
