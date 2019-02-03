import re



import re

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

def convert(text):
    """
    Convert from 'Tieng Viet co dau' thanh 'Tieng Viet khong dau'
    text: input string to be converted
    Return: string converted
    """
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output

def isEnglish(s):
    s=convert(s)
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True




import html2text
from scrapy.selector import Selector
import requests
import urllib
import mysql.connector as connect

def name_singer_ro(singer_name):
    try:
        temp=isEnglish(singer_name)
    except:
        temp=False

    if temp == True:
        print("mapIsEnglishName: " + singer_name)
        return singer_name
    else:
        try:
            ctn = connect.connect(user="admin_user", password="eup.mobi", host="103.253.145.165",
                                  database="pikasmart")
            cusor = ctn.cursor()
            cusor.execute("SELECT name_singer_value,name_singer_romaji from lyric_finder_singer_name_convert")
            map_singer={}
            for x in cusor.fetchall():
                map_singer[x[0].lower().strip()]=x[1].strip()
            if map_singer.get(singer_name.lower().strip())!=None:
                print("getMapFromDataBase: "+singer_name+" : "+ map_singer[singer_name.lower()])
                return map_singer[singer_name.lower()]

        except:
            return False
        try:

            infor = requests.get("https://www.google.com/search?q="+urllib.parse.quote(singer_name)).text
            # try:
            name_ro=html2text.html2text(Selector(text=infor).xpath(".//div[starts-with(@class, 'FSP1Dd')]").extract()[0]).strip()
            cusor.execute("INSERT INTO lyric_finder_singer_name_convert (name_singer_value,name_singer_romaji) VALUES (%s,%s)",(singer_name,name_ro))
            ctn.commit()
            print("mapFound: "+singer_name+" : "+name_ro)
            return name_ro
            # except:
            #     name_ro = Selector(text=infor).xpath(".//div[starts-with(@class, 'JYQZge vrQIef')]").extract()[0]
            #     return html2text.html2text(name_ro)
        except:
            text=html2text.html2text(infor).lower()
            if "a robot" in text and "ip address" in text:
                return False
            cusor.execute(
                "INSERT INTO lyric_finder_singer_name_convert (name_singer_value,name_singer_romaji) VALUES (%s,%s)",
                (singer_name.strip(), singer_name.strip()))
            ctn.commit()
            print("mapNotFound: "+singer_name+" : "+singer_name)
            return singer_name






# name_singer_ro("Q-MHz feat.日高光啓 a.k.a. SKY-HI")

# print( unidecode.unidecode("千尋, thousand fathoms"))





import mysql.connector as connect
import requests
from scrapy.selector import Selector

import json
ctn = connect.connect(user="admin_user", password="eup.mobi", host="103.253.145.165",
                          database="pikasmart")
cusor = ctn.cursor()




import re

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

def convert(text):
    """
    Convert from 'Tieng Viet co dau' thanh 'Tieng Viet khong dau'
    text: input string to be converted
    Return: string converted
    """
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output

def isEnglish(s):
    s=convert(s)
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

cusor.execute("select name from lyric_finder_singer")
# name_singer=list(set([x[0] for x in cusor.fetchall() if isEnglish(x[0])==False]))
# with open("nameKanji.json","w",encoding="utf-8") as f:
#     json.dump(name_singer,f,ensure_ascii=False,indent=4)

name_singer=json.load(open("nameKanji.json",encoding="utf-8"))


headers = {
    'cookie':"CGIC=IlV0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44; CONSENT=YES+VN.vi+20180429-14-0; SID=9gZaRfypZDVgf-6wpDbkaJe8io2bgMf1HfiAPWONY3Zh771vHn8kJGxDOZqtlXHmlcE9aA.; HSID=A1T_3fFub6aOOdT3J; SSID=AOOdwXQgYSIucZ2mZ; APISID=FZoKGRY8othue8Tn/A69G4pn4FWWXZrmwE; SAPISID=hfbfu2FH4T1fEcIG/A-BSOTNqtfv63_5QV; OGPC=19010494-2:; OGP=-19010494:; NID=156=XIjUJpZ2CBGZQ3m4MgFmLg6c9hwgj1-t1iiIycQS0ptAUtQo2SpHkOZdjfb1MAEuvys3FyIcp0HUbYjL-qLLlxb-VeYMXRvfxVDyWUR3fZ1f8Pdao0uEX5rA8LLKb_kIrz4VlFu9N6frcyoFPcZp9rVY6Vmt8uFm9PG1oGZ3reyVvS3Ne_v26nGwNsBproxZezZC07c2U7WuLlTtIp3FetauqNvy8va-dkK_SEQdf14bteZcLvFz-nmFx9DRKfJzkk3nzZmLYNorFn3PfNfm91f9LH9iLLB0mm0u93LqkPUdZBsCpolzgjwjsUpG2OtdnNDRkuO_DBGJyav1EI6NSf2dSbQkDIif1s26w-vjODYY8eB_DPFmcykfFuUnNelsKzRF6_dO6TL3YpRlcDziwbDdJ9-YcurHMfy0cnUVkAFpPC3dkcMMLUJSJGmh1QeCgyfQrOrvDxq5t4anbffOBgUzNYOFVypggTtZ_zjMAchW1K2GgWpFe-I; DV=E4G89O-Bg5ivECBuCtWvdH13aVWXiFbFnRULTMb8_QEAAGC8rWKyRZv8wwAAALgHGACE7GREUQAAAL7waBe6cLSgFAAAwJ7Rz2pycKZGBqACELXrd6iumDSYAagAOJ85pD_5bHt-ACoAG2jETFGYbPQggAqAwCqLfZL73aoLoAIA; UULE=a+cm9sZToxIHByb2R1Y2VyOjEyIHByb3ZlbmFuY2U6NiB0aW1lc3RhbXA6MTU0ODQ5NDM5NzA4NzAwMCBsYXRsbmd7bGF0aXR1ZGVfZTc6MjEwMDMxNTE3IGxvbmdpdHVkZV9lNzoxMDU4MzQ5MTI0fSByYWRpdXM6MTE5NTk4MA==; 1P_JAR=2019-01-26-09; GOOGLE_ABUSE_EXEMPTION=ID=6827382ff12c10b5:TM=1548494539:C=r:IP=58.187.32.86-:S=APGng0sbLJOFGHRNAMN88GAsaOsu7AH2jg; SIDCC=ABtHo-GL1dLHHOkCE7UHu7z7JAn8Xs4G-9lRh1PEax8Weet0hWy018wl-v02Cl2YYyUt7BrxPTvC",
    'cache-control': "no-cache",
    'postman-token': "11bc0631-2de2-21d4-a46e-6a28d58ab5b0"
    }

def get_name_ro(singer_name,ind):
    try:
        infor = requests.get("https://www.google.com/search?q=" + urllib.parse.quote(singer_name)+" singer").text
        name_ro = html2text.html2text(Selector(text=infor).xpath(".//div[starts-with(@class, 'FSP1Dd')]").extract()[0]).strip()
        with open("name_singer_google_add/{}.json".format(str(ind)),"w",encoding="utf-8") as f:
            json.dump({singer_name:name_ro},f,ensure_ascii=False,indent=4)
        print(name_ro)
        return name_ro

    except:
        text = html2text.html2text(infor).lower()
        if "a robot" in text and "ip address" in text:
            return False
        pass

import time
import os
temp= [x.split(".")[0] for x in os.listdir("name_singer_ro_google")]
add=list(set([str(x) for x in range(len(name_singer))])-set(temp))
# print([str(x) for x in range(len(name_singer))])

for x in range(16163,len(name_singer)):
    if str(x) not in temp:
        time.sleep(2)
        print(x,name_singer[x])
        if get_name_ro(name_singer[x],x)== False:
            break




