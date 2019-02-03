import requests
import re
import html2text
# get_romanji



querystring = {"vet":"12ahUKEwjSgcPShM7eAhUH_GEKHaG2D5kQqDgwAHoECAYQFg..i","ei":"EQTpW5K1EYf4hwOh7b7ICQ","yv":"3"}
import urllib

headers = {
    'host': "www.google.com",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0; Waterfox) Gecko/20100101 Firefox/56.2.5",
    'accept': "*/*",
    'referer': "https://www.google.com/",
    'content-type': "application/x-www-form-urlencoded;charset=utf-8",
    'cookie': "NID=146=p-KPB8sQ6nqjr8I56LiEJzjdcsk7Wh91oDwr0jU0rfwOfN4Y_l9T4j_5uaSDg_6tDMSEXmPdhueoxwYM4w6meuHTK1R-Mej8-9Fm4kiEb8kFw8wVPnrgtaefkgNPq3W9ro81wpyImN-QtPVKILiNYq5UN07oTQWarcfgEXHOl0w6PR7uE4Xh14o; 1P_JAR=2018-11-12-04; OGP=-5061451:; DV=AwAhS-7BuJMeYH8oIYu_J3hJpKxjcBY",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'postman-token': "840316e0-b716-91d0-b2be-4011273befa2"
    }
url = "https://www.google.com.vn/async/translate"
querystring = {"vet":"12ahUKEwjSgcPShM7eAhUH_GEKHaG2D5kQqDgwAHoECAYQFg..i","ei":"EQTpW5K1EYf4hwOh7b7ICQ","yv":"3"}

def trans(text,srt,dest):
    payload = "async=translate,sl:"+srt+",tl:"+dest+",st:" + urllib.parse.quote(text) + ",id:1541997726654,qc:true,ac:true,_id:tw-async-translate,_pms:s,_fmt:pc"
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    return re.findall("tw-answ-source-romanization\">(.*?)</span>",response.text)[0].capitalize()



def tag_youtube(s):
    if s==None:
        return ""
    return "".join(s)

# check_video_youtube
id_of_video = '0IgltG0Zsd4'
your_api_key = 'AIzaSyAgWw9-PCBxi3BP-JAHNtz57LVcbJPtaiw'

def check(id_of_video):
    # contentDetails
    # status
    # statistics
    url = f'https://www.googleapis.com/youtube/v3/videos?id={id_of_video}&key={your_api_key}&part=snippet'
    url_get = requests.get(url).json()
    if len(url_get["items"])==0:
        return [None,"",""]
    try:
        thum=list(url_get["items"][0]["snippet"]["thumbnails"].values())[-1]["url"]
    except:
        thum="http://img.youtube.com/vi/"+id_of_video+"/0.jpg"

    return [url_get["items"][0]["snippet"].get("title"),url_get["items"][0]["snippet"].get("title")
            +url_get["items"][0]["snippet"].get("description")
            + tag_youtube(url_get["items"][0]["snippet"].get("tags"))
            ,thum
            ]
# download image
def dow(url,link):
    with open(link, 'wb') as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)




# key_lyric
def multiple_replace(string, rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]), flags=re.DOTALL)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)


# get_furigana,getromanji,getkata_hira
from furigana.furigana import split_furigana
import re
from datetime import datetime
def get_hira_kata(s):
    S=""
    for t in s.split(" "):
        try:
            temp=split_furigana(t)
        except:
            return ""
        for x in temp:
            if len(x)==1:
                S=S+x[0]
            else:
                S=S+x[1]
        S=S+" "
    return " ".join([x for x in re.sub(u"([\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f-\u3300-\u33ff\ufe30-\ufe4f\uf900-\ufaff\U0002f800-\U0002fa1f\u30a0-\u30ff\u2e80-\u2eff\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf]+)", r" \1 ", S).strip().capitalize().split(" ") if x!=""])

def conv_final(furi):
    temp=""
    for pair in furi:
        if len(pair) == 2:
            kanji, hira = pair
            temp=temp+"<ruby><rb>{0}</rb><rt>{1}</rt></ruby>".format(kanji, hira)
        else:
            temp=temp+pair[0]
    return '<font  size = "3" style="color:#000000">'+temp.replace("<rt>",'<rt><font  size = "2" style="color:#2c87f0">').replace("</rt>",'</font></rt>')+'</font>'

import json
def get_furi(s):
    temp=[]
    for x in s.split(" "):
        try:
            temp.append(conv_final(split_furigana(x)))
        except:
            temp.append(x)

    return " ".join(temp)



def cra(ind):
    data=requests.get("https://www.uta-net.com/song/"+str(ind))
    data.encoding="utf-8"
    data=data.text
    singer=html2text.html2text(re.findall("<span itemprop=\"byArtist name\">((.|\n)*?)</span>",data)[0][0]).strip().capitalize()
    name=html2text.html2text(re.findall("<span>曲名：((.|\n)*?)</span>",data)[0][0]).strip().capitalize()
    try:
        name_romanji = trans(name, "ja", "en")
        if name_romanji == "":
            name_romanji = name
    except:
        name_romanji = name

    lyric_raw = re.findall("div id=\"kashi_area\" itemprop=\"text\"((.|\n)*?)/div>", data)
    lyric = [x.strip().capitalize().replace("\u3000", " ") for x in
             re.findall(">(.*?)<", lyric_raw[0][0]) if x.strip() != ""]

    youtube_link_check = ""
    image_thum_max = ""
    try:
        li = "https://www.uta-net.com" + \
             re.findall("<p class=\"youtube_button\"><a href=\"(.*?)\"", data.replace("\n", ""))[0]
        youtube_link = requests.get(li)
        youtube_link.encoding = "utf-8"
        youtube_link = \
            re.findall("https://www.youtube.com/embed/((.|\n)*?)\?", youtube_link.text)[0][0]
        check_title = check(youtube_link)
        if check_title[0] != None:
            dic = {" ": "", "(": "", ")": ""}

            if multiple_replace(name, dic).lower() in multiple_replace(check_title[0],dic).lower() and multiple_replace(singer,dic).lower() in multiple_replace(check_title[1], dic).lower():
                youtube_link_check = "https://www.youtube.com/watch?v=" + youtube_link
                image_thum_max = check_title[2]
    except:
        pass

    avata_singer = "/assets_lyric_finder/img/singer/default_singer.jpg"
    try:
        link_dow = \
        re.findall("<img src=\"(.*?)\"", re.findall("<div class=\"right\">((.|\n)*?)</div>", data)[0][0])[0]
        if "http" in link_dow:
            avata_singer = "assets_lyric_finder/img/singer/iruyas_" + link_dow.split("/")[-1]
            dow(link_dow, avata_singer)
            avata_singer = "/" + avata_singer
        else:
            avata_singer = "/assets_lyric_finder/img/singer/default_singer.jpg"
    except:
        avata_singer = "/assets_lyric_finder/img/singer/default_singer.jpg"

    lyric_data = []
    for x in lyric:
        try:
            romanji = trans(x, "ja", "en")
            if romanji == "":
                romanji = x
        except:
            romanji = x
            pass
        try:
            hira_kata = get_hira_kata(x)
            if hira_kata == "":
                hira_kata = x
        except:
            hira_kata = x
            pass

        try:
            furi = get_furi(x)
            if furi == "":
                furi = x
        except:
            furi = x
            pass
        lyric_data.append({"kanji": x, "roman": romanji, "hira_kata": hira_kata, "furigana": furi})
    try:
        date=re.findall("発売日：((.|\n)*?)<",data)[0][0].strip()
    except:
        date=""

    if "http" in youtube_link_check:
        data_output = {"name": name.strip().capitalize(), "name_ro": name_romanji.strip().capitalize(),
                       "singer": singer.strip().capitalize(), "date": date, "avata_singer": avata_singer,
                       "link_youtube": youtube_link_check, "thumb_max": image_thum_max,
                       "thumbnail": "http://img.youtube.com/vi/" + youtube_link_check.split("v=")[-1] + "/0.jpg",
                       "lyric": lyric_data}
    else:
        data_output = {"name": name.strip().capitalize(), "name_ro": name_romanji.strip().capitalize(),
                       "singer": singer.strip().capitalize(), "date": date, "avata_singer": avata_singer,
                       "link_youtube": youtube_link_check, "thumb_max": "", "thumbnail": "", "lyric": lyric_data}
    with open("full_data/"+str(ind)+".json", "w", encoding="utf-8") as file:
        json.dump(data_output, file, ensure_ascii=False, indent=4)
# print(html2text.html2text("Firstxxxxx"))
# 222000

# kkk=[187827, 5095, 217803, 189439, 195790, 181748, 187823]
# kkk=[103, 193767, 195791, 99, 5096, 217800, 187825, 195793]
kkk=[217804, 189441, 108854, 102, 199549, 189440, 220573]
kkk=[193770, 187824, 108851, 215483, 193769, 223280]
kkk=[215485, 223276, 217798, 184808, 223279, 184811, 184810]
kkk=[181750, 220576, 187826, 195787, 215481, 199550, 108855, 199548]
kkk=[101, 217802, 215484, 215482, 217797, 184809, 193771, 195792, 5099]
kkk=[193768, 215480, 104, 217801, 5097, 195788, 189438, 217799, 223278]
kkk=[181747, 195786, 108853, 220575, 181751, 223277, 220574, 195789, 5098, 108852, 189442]



for x in kkk:
    print(x)
    try:
        cra(x)
    except:
        print("XXX:",str(x))
        continue
# print(get_furi("地下で進められた研究 だが今 日の目浴びそうさ thank you"))