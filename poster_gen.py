#!/usr/bin/python3
# Copyright Anoop S 2020
# covid-kerala poster generator by Anoop S based on fillerink's ieee-covid-poster-generator
# completely automated , requires no input from user
# optionally date can be passed eg: ./make_poster.py "18-05-2020"
import datetime
import os
import re
import sys
import json
import subprocess
import urllib.request


def get_data_for_date(date_today):
    covid_district_data=[]
    covid_state_data={}
    covid_state_data_to_keep = ['confirmed','recoveredCumulative','deceasedCumulative','confirmedCumulative'] 
    JSON_URL= 'https://raw.githubusercontent.com/c19k/website-data/master/docs/summary/'
    resp = urllib.request.urlopen(JSON_URL+str(date_today)+".json")
    json_data_today = json.loads(resp.read())
    for i in json_data_today["prefectures"]:
        covid_district_data_dict = {"district":i["name"],"newlyConfirmed":i["newlyConfirmed"],"zone":i["zone"],"deaths":i["deaths"]}
        covid_district_data.append(covid_district_data_dict)
    for i in json_data_today["daily"]:
        if i ["date"] == str(date_today):
            for j in covid_state_data_to_keep:
                covid_state_data.update({j:i[j]})
    data_last_updated_time = json_data_today["updated"].split()[1]
    return covid_district_data,  covid_state_data, data_last_updated_time


def make_poster():
    covid_district_data, covid_state_data,data_last_updated_time = get_data_for_date(dateobj)
    src_file = "./covid_blank.png"
    out_file = "./output_{}.png".format(dateobj)
    fonts = "./fonts/Cantarell-Bold.otf"
    text_pos_district = {"Kasaragod":" -370,230","Kannur":"-310,345","Kozhikode":"-260,445","Malappuram":"-220,540","Wayanad":"10,340","Palakkad":"140,548","Thrissur":"-140,650","Idukki":"210,675","Ernakulam":"-125,755","Kottayam":"-100,850","Pathanamthitta":"270,940","Alappuzha":"-80,925","Kollam":"-35,995","Thiruvananthapuram":"300,1065"}
    text_pos_info = {"confirmed":"364,455","recoveredCumulative":"364,582","deceasedCumulative":"364,698","confirmedCumulative":"364,820"}
    district_image_pos = {"Kasaragod":["170","113"],"Kannur":["233.75","220.5"],"Kozhikode":["311.74","329.51"],"Malappuram":["372.75","391.50"],"Wayanad":["357.74","291.76"],"Palakkad":["419","459"],"Thrissur":["401.2","560.5"],"Idukki":["553.5","653.125"],"Ernakulam":["451","665.125"],"Kottayam":["496.6125","762"],"Pathanamthitta":["522","848"],"Alappuzha":["483.5","836"],"Kollam":["521.25","919"],"Thiruvananthapuram":["566.5","989"]}
    # draw time and date 
    tmp = "text 440,180 '{}'".format(dateobj)
    cmd = 'convert -font {} -pointsize 20 -gravity North -fill white -draw "{}" {} {} '.format(fonts,tmp,src_file,out_file)
    subprocess.call(cmd, shell=True)
    tmp = "text 440,215 '{}'".format(data_last_updated_time)
    cmd = 'convert -font {} -pointsize 20 -gravity North -fill white -draw "{}" {} {} '.format(fonts,tmp,out_file,out_file)
    subprocess.call(cmd, shell=True)
    # annotate district values
    for i in covid_district_data:
        district = i["district"]
        tmp = "text {} '{}'".format(text_pos_district[district],i['newlyConfirmed'])
        cmd = 'convert -font {} -pointsize 23 -gravity North -draw "{}" {} {} '.format(fonts,tmp,out_file,out_file)
        subprocess.call(cmd, shell=True)
    # TEXT GENERATED FOR THE 4 STATUS
    for i in covid_state_data.keys():
        tmp = "text {} '{}'".format(text_pos_info[i],covid_state_data[i])
        cmd = 'convert -font {} -pointsize 23 -gravity North -draw "{}" {} {} '.format(fonts,tmp,out_file,out_file)
        subprocess.call(cmd, shell=True)
    # stitch  district images
    for i in covid_district_data:
        district = i["district"]
        district_img = district+"_"+i["zone"]+".png"
        cmd = 'convert {}  ./images/{} -background none -gravity center  -gravity northwest -geometry +{}+{} -composite {}'.format(out_file,district_img,district_image_pos[district][0],district_image_pos[district][1],out_file)
        subprocess.call(cmd, shell=True)





if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("covid_poster_gen.py [dd-mm-yyyy]")
            print("generates poster for current date if no argument given ")
            sys.exit()
        else:
            datearg = sys.argv[1]
            dsplit = [int(i) for i  in re.split(r'[-/]\s*', datearg)]
            dateobj = datetime.date(day=dsplit[0], month=dsplit[1], year=dsplit[2])
    else:
        dateobj = datetime.date.today()

    make_poster()
