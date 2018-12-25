# -*- coding: utf-8 -*-
import requests
import re
import json
import os
from datetime import datetime
from random import randint
import mysql.connector as connect
import random
import html2text


# update pipop wordpress




import requests

url_vote = "http://japanesesonglyrics.com/wp-admin/admin-ajax.php"

querystring_vote = {"_fs_blog_admin":"true"}
headers_vote = {
    'cookie': "wordpress_4dda44f2851085a46a0d9de2bad94d36=admin%7C1545876171%7CXh8uSoPelBERaEVQ0UTzDEoTbexo7KdsAV1R4khGrJQ%7Cded672c6c902af242c68ae420f31032a4149b422ba36ced15206614a05bc58fb; wp-saving-post=22665-check; _ga=GA1.2.397996287.1543393060; wp-settings-1=libraryContent%3Dbrowse%26editor%3Dtinymce%26uploader%3D1; wp-settings-time-1=1545482037; _gid=GA1.2.1558347181.1545615290; yasr_visitor_vote_cookie=a%3A3%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A7%3A%22post_id%22%3Bs%3A4%3A%221035%22%3Bs%3A6%3A%22rating%22%3Bs%3A3%3A%225.0%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A7%3A%22post_id%22%3Bs%3A5%3A%2222466%22%3Bs%3A6%3A%22rating%22%3Bs%3A3%3A%225.0%22%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A7%3A%22post_id%22%3Bs%3A5%3A%2222621%22%3Bs%3A6%3A%22rating%22%3Bs%3A3%3A%225.0%22%3B%7D%7D; wordpress_test_cookie=WP+Cookie+check; wordpress_logged_in_4dda44f2851085a46a0d9de2bad94d36=admin%7C1545876171%7CXh8uSoPelBERaEVQ0UTzDEoTbexo7KdsAV1R4khGrJQ%7Ce31db67ddf7542b997e420c7c74943e8fc12de3d0a2c985eca5d8a9f189666ee",
    'host': "japanesesonglyrics.com",
    'origin': "http://japanesesonglyrics.com",
    'referer': "http://japanesesonglyrics.com/wp-admin/post.php?post=22670&action=edit",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/76.0.114 Chrome/70.0.3538.114 Safari/537.36",
    'x-requested-with': "XMLHttpRequest",
    'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
    'content-length': "73",
    'connection': "keep-alive",
    'accept-language': "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    'accept-encoding': "gzip, deflate",
    'accept': "*/*",
    'cache-control': "no-cache",
    'postman-token': "f089289b-9652-dd2f-b818-c9680c2d55b1"
    }

def admin_score(id,rate):

    payload =  "action=yasr_send_overall_rating&nonce=ae3bbf26bb&rating="+str(rate)+"&post_id="+str(id)
    # payload = "action=yasr_send_overall_rating&nonce=ae3bbf26bb&rating=4.2&post_id=22848"

    response = requests.request("POST", url_vote, data=payload, headers=headers_vote, params=querystring_vote)
    print(response.text)
    print(payload)



def insert_rate(data_vote,cusor,ctn):
    sql="""INSERT INTO wp_yasr_log (post_id,multi_set_id,user_id,vote,date,ip) 
                               VALUES (%s,%s,%s,%s,%s,%s)"""
    cusor.execute(sql, data_vote)
    ctn.commit()

def update_des_image(id,post_content,cusor,ctn):
    sql = "UPDATE wp_posts SET post_title ='"+post_content+"' , post_excerpt ='"+post_content  +"' WHERE ID = " +str(id)
    cusor.execute(sql)
    ctn.commit()
    sql = """INSERT INTO wp_postmeta (post_id,meta_key,meta_value) 
                                   VALUES (%s,%s,%s)"""
    cusor.execute(sql, (id,"_wp_attachment_image_alt",post_content))
    ctn.commit()

def form(name_song,name_singer,furigana,english,link_video,ro_name):
    if randint(0, 1) == 0:
        mobai = """<p style="text-align: justify;">Today we bring to you the <strong>{0}</strong><strong> with FULL Japanese lyric and English translation.</strong> Beside that, you can also reading the lyric in hiragana or romaji and watching the {1} music video.</p>""".format(name_song,name_singer)
    else:
        mobai = """<p style="text-align: justify;">This post will show you the <strong>FULL Japanese lyric</strong> (both kanji, hiragana and romaji) <strong>and English translation of {0} - {1}.</strong> Plus, you can also listening to the {0} song while reading the lyric.</p>""".format(name_song,name_singer)
    if randint(0, 1) == 0:
        ketbai = """<p style="text-align: justify;">We hope that you guys already found what you looking for, the <strong>FULL lyric and english translation of {0} - {1}</strong> and some information of this japanese song.
    Let us know your favorite lyric sentences in the comment and don't forget to bookmark this website to read a lot of song lyrics in the future.</p>""".format(name_song,name_singer)
    else:
        ketbai = """<p style="text-align: justify;">Are you satisfy with the <strong>{0} - {1} lyric and english translation</strong> that we bring to you today? Let us know in the comment and don't forget to bookmark this website to read a lot of song lyrics and translations in the future.</p>""".format(name_song,name_singer)

    content_table = """<h3>Original lyric (Japanese lyric)</h3>
                        <p style="text-align: justify;">{0}</p><br>
                        <h3>English translation</h3><p style="text-align: justify;"><i>{1}</i></p>
                           """.format(furigana,english)

    table=content_table
    if "https://www.youtube.com/embed/" != link_video:
        f = mobai \
            + "<h2><strong>{0} - {1}</strong></h2>" + "\n" \
            + "<ul><li>Song Information</li><li>Original lyric (Japanese lyric)</li><li>English translation</li></ul>" + "\n" \
            + "<h3>Song Information</h3>" + "\n" \
            + """<ul><li>Song's Orginal Name: <strong>{0}</strong></li><li>Song's Romaji Name: <strong>{3}</strong></li><li>Singer: <strong>{1}</strong></li><li>Song Music Video:</li></ul>""" +'<iframe src={2} width="853" height="480" frameborder="0" allowfullscreen="allowfullscreen"></iframe>' +"\n\n" \
            + "<hr />" + "\n\n" \
            + table + "\n" \
            + "" + "\n" \
            + ketbai
    else:
        f = mobai \
            + "<h2><strong>{0} - {1}</strong></h2>" + "\n" \
            + "<ul><li>Song Information</li><li>Original lyric (Japanese lyric)</li><li>English translation</li></ul>" + "\n" \
            + "<h3>Song Information</h3>" + "\n" \
            + """<ul><li>Song's Orginal Name: <strong>{0}</strong></li><li>Song's Romaji Name: <strong>{3}</strong></li><li>Singer: <strong>{1}</strong></li></ul>""" + "\n\n" \
            + "<hr />" + "\n\n" \
            + table + "\n" \
            + "" + "\n" \
            + ketbai

    f = f.format(name_song,name_singer,link_video,ro_name)
    return f

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
client = Client('http://japanesesonglyrics.com/xmlrpc.php', 'admin', 'FpkVt192U0xA2uBWxX')
image_thum = os.listdir("image_des_wp_pipop")

def S(filename,data):
    ctn=connect.connect(user="admin_user",password="eup.mobi",host="103.253.145.165",database="admin_songlyrics")
    cusor=ctn.cursor()
    kan = ""
    for x in data["lyric"]:
        kan = kan + x["furigana"] + "\n" + x["roman"] + "\n\n"

    data_image = {
        'name': 'whiye.jpg',
        'type': 'image/jpeg',
    }
    if "http" in data["thumbnail"]:
        dow(data["thumb_max"], filename)
    else:
        filename="image_des_wp_pipop/"+image_thum[random.randint(0,390)]
    # read the binary file and let the XMLRPC library encode it into base64
    with open(filename, 'rb') as img:
        data_image['bits'] = xmlrpc_client.Binary(img.read())
    response = client.call(media.UploadFile(data_image))
    attachment_id = response['id']
    post = WordPressPost()
    cate=[]
    cate.append("Jpop Lyrics")
    post.terms_names = {
      'category': cate,
    }
    post.title = "FULL lyric and english translation of "+data["name"]+ " - "+data["singer"]
    post.content = form(data["name"],data["singer"],kan,"Updating!!!","https://www.youtube.com/embed/"+data["link_youtube"].split("v=")[-1],data["name_ro"])
    post.post_status = 'publish'
    post.thumbnail = attachment_id
    post.id = client.call(posts.NewPost(post))
    now_1 = datetime.now()
    print((post.id, -1, 1, random.randint(45, 50) / 10, now_1, "X.X.X.X"))

    print((attachment_id,
           "{0} lyric, {0} english translation, {0} {1} lyrics".format(data["name"],
                                                                       data["singer"])))


    insert_rate((post.id, -1, 1, random.randint(45, 50) / 10, now_1, "X.X.X.X"),cusor,ctn)

    update_des_image(attachment_id,
                     "{0} lyric, {0} english translation, {0} {1} lyrics".format(data["name"],
                                                                               data["singer"]),cusor,ctn)
    admin_score(post.id,random.randint(45,50)/10)


# check_video_youtube
id_of_video = '0IgltG0Zsd4'
your_api_key = 'AIzaSyAgWw9-PCBxi3BP-JAHNtz57LVcbJPtaiw'

def tag_youtube(s):
    if s==None:
        return ""
    return "".join(s)


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


# get_furigana,getromanji,getkata_hira
from furigana.furigana import split_furigana
import re
from datetime import datetime


def conv_final(furi):
    temp=""
    for pair in furi:
        if len(pair) == 2:
            kanji, hira = pair
            temp=temp+"<ruby><rb>{0}</rb><rt>{1}</rt></ruby>".format(kanji, hira)
        else:
            temp=temp+pair[0]
    return '<font  size = "3" style="color:#000000">'+temp.replace("<rt>",'<rt><font  size = "2" style="color:#2c87f0">').replace("</rt>",'</font></rt>')+'</font>'

def get_furi(s):
    temp=[]
    for x in s.split(" "):
        try:
            temp.append(conv_final(split_furigana(x)))
        except:
            temp.append(x)

    return " ".join(temp)


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

# get_romanji
def trans(text,srt,dest):
    # print(urllib.parse.quote(text))
    payload = "async=translate,sl:"+srt+",tl:"+dest+",st:" + urllib.parse.quote(text) + ",id:1541997726654,qc:true,ac:true,_id:tw-async-translate,_pms:s,_fmt:pc"
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    return re.findall("tw-answ-source-romanization\">(.*?)</span>",response.text)[0].capitalize()

# key_lyric
def multiple_replace(string, rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]), flags=re.DOTALL)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)
def key_lyric(s):
    s=s.lower().replace("\u3000"," ")
    dic = {"\n": " ", "\"": " ", "\'": " ", "、": " ", "。": " ","\r":" ","!":" ",".":" ",",":" ","\u3000":" ","\\":" ","\ufeff":" "}
    temp= multiple_replace(re.sub(u"([\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f-\u3300-\u33ff\ufe30-\ufe4f\uf900-\ufaff\U0002f800-\U0002fa1f\u30a0-\u30ff\u2e80-\u2eff\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf]+)", r"(((\1)))", s),dic)
    kan=[x for x in "".join(re.findall("\(\(\((.*?)\)\)\)",temp)) if x !=" "]
    eng=[y for y in " ".join(re.findall("\)\)\)(.*?)\(\(\(",")))"+temp+"(((")).split(" ") if y!=""]
    return list(set(kan+eng))

# check lyric
def check_lyric(lyric,cache_lyric):
    key=key_lyric(lyric)
    l_key=len(key)
    for x in cache_lyric:
        l_x=len(x)
        score=len(list(set(key)&set(x)))/l_key*(min(l_key,l_x)/max(l_key,l_x))
        if score>0.9:
            return [True,key]
    return [False,key]



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




def save(data,name):
    with open(name,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=4)

def save_(data,name):
    with open(name,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False)

def crawl():
    cache_lyric = json.load(open("cache_lyric.json", encoding="utf-8"))
    data_cron=[]
    link = "https://www.uta-net.com/user/newsong/release_top.html"
    data = requests.get(link)
    data.encoding = "utf-8"
    data_page_0 = data.text
    page = [x[0] for x in re.findall("page=((.|\n)*?)\"",data_page_0)]
    # link_lyric = [x[0] for x in re.findall("<tr((.|\n)*?)</tr>",data_page_0)]
    # temp=json.load(open("cache_uta_net.json",encoding="utf-8"))
    # for x in link_lyric:
    #     try:
    #         print("kkk")
    #         name_link = re.findall("<td>(.*?)</td>", x)[0]
    #         name = re.findall(">(.*?)<", name_link)[0]
    #         singer = re.findall("<td>(.*?)</td>", x)[1]
    #         date = re.findall("<td class=\"align_c\">(.*?)</td>", x)[0]
    #         cache_raw=json.dumps([name,singer,date])
    #         if temp.get(cache_raw)==None:
    #             link_lyric="https://www.uta-net.com"+re.findall("<a href=\"(.*?)\"",name_link)[0]
    #             lyric_kanji=requests.get(link_lyric)
    #             lyric_kanji.encoding="utf-8"
    #             lyric_kanji=lyric_kanji.text
    #             lyric_raw=re.findall("div id=\"kashi_area\" itemprop=\"text\"((.|\n)*?)/div>",lyric_kanji)
    #             lyric=[x.strip().capitalize().replace("\u3000"," ") for x in re.findall(">(.*?)<",lyric_raw[0][0]) if x.strip()!=""]
    #             temp[cache_raw] = ""
    #             check_lyric_in_cache=check_lyric(" ".join(lyric),cache_lyric)
    #             if check_lyric_in_cache[0]==False:
    #                 cache_lyric.append(check_lyric_in_cache[1])
    #                 youtube_link_check=""
    #                 image_thum_max=""
    #                 try:
    #                     li="https://www.uta-net.com"+re.findall("<p class=\"youtube_button\"><a href=\"(.*?)\"",lyric_kanji.replace("\n",""))[0]
    #                     youtube_link=requests.get(li)
    #                     youtube_link.encoding="utf-8"
    #                     youtube_link=re.findall("https://www.youtube.com/embed/((.|\n)*?)\?",youtube_link.text)[0][0]
    #                     check_title = check(youtube_link)
    #                     if check_title[0] != None:
    #                         dic = {" ": "", "(": "", ")": ""}
    #                         if multiple_replace(name, dic).lower() in multiple_replace(check_title[0], dic).lower() and multiple_replace(singer, dic).lower() in multiple_replace(check_title[1], dic).lower():
    #                             youtube_link_check = "https://www.youtube.com/watch?v=" + youtube_link
    #                             print("https://www.youtube.com/watch?v=" + youtube_link)
    #                             image_thum_max=check_title[2]
    #                 except:
    #                     pass
    #                 avata_singer="/assets_lyric_finder/img/singer/default_singer.jpg"
    #                 try:
    #                     link_dow=re.findall("<img src=\"(.*?)\"",re.findall("<div class=\"right\">((.|\n)*?)</div>",lyric_kanji)[0][0])[0]
    #                     if "http" in link_dow:
    #                         avata_singer="assets_lyric_finder/img/singer/iruyas_"+link_dow.split("/")[-1]
    #                         print(link_dow)
    #                         dow(link_dow,avata_singer)
    #                         avata_singer="/"+avata_singer
    #                     else:
    #                         avata_singer = "/assets_lyric_finder/img/singer/default_singer.jpg"
    #                 except:
    #                     avata_singer = "/assets_lyric_finder/img/singer/default_singer.jpg"
    #                 lyric_data=[]
    #                 for x in lyric:
    #                     try:
    #                         romanji=trans(x,"ja","en")
    #                         if romanji=="":
    #                             romanji=x
    #                     except:
    #                         romanji=x
    #                         pass
    #                     try:
    #                         hira_kata=get_hira_kata(x)
    #                         if hira_kata=="":
    #                             hira_kata=x
    #                     except:
    #                         hira_kata=x
    #                         pass
    #                     try:
    #                         furi = get_furi(x)
    #                         if furi == "":
    #                             furi = x
    #                     except:
    #                         furi = x
    #                         pass
    #                     lyric_data.append({"kanji":x,"roman":romanji,"hira_kata":hira_kata,"furigana":furi})
    #
    #                 if "http" in youtube_link_check :
    #                     data_output = {"name": name.strip().capitalize(), "singer": singer.strip().capitalize(),"date": date, "avata_singer": avata_singer, "link_youtube": youtube_link_check,"thumb_max":image_thum_max,"thumbnail": "http://img.youtube.com/vi/" + youtube_link_check.split("v=")[-1] + "/0.jpg", "lyric": lyric_data}
    #                 else:
    #                     data_output = {"name": name.strip().capitalize(), "singer": singer.strip().capitalize(),"date": date, "avata_singer": avata_singer, "link_youtube": youtube_link_check,"thumb_max":"","thumbnail":"" , "lyric": lyric_data}
    #
    #                 save(data_output,"data_lyric_finder/"+str(datetime.now()).replace(".","_").replace(" ","_").replace("-","_").replace(":","_")+".json")
    #                 save_(cache_lyric,"cache_lyric.json")
    #                 S("whyew.jpg",data_output)
    #                 print("Cron ok")
    #
    #     except:
    #         continue
    # with open("cache_uta_net.json", "w", encoding="utf-8") as file:
    #     json.dump(temp, file, ensure_ascii=False,indent=4)

    for x in page:
        link_page = link + "?page=" + x
        data = requests.get(link_page)
        data.encoding = "utf-8"
        data_page_0 = data.text
        link_lyric = [x[0] for x in re.findall("<tr((.|\n)*?)</tr>", data_page_0)]
        temp = json.load(open("cache_uta_net.json", encoding="utf-8"))
        for x in link_lyric:
            try:
                name_link = re.findall("<td>(.*?)</td>", x)[0]
                name = html2text.html2text(re.findall(">(.*?)<", name_link)[0])
                try:
                    name_romanji=trans(name,"ja","en")
                    if name_romanji=="":
                        name_romanji=name
                except:
                    name_romanji=name
                singer = html2text.html2text(re.findall("<td>(.*?)</td>", x)[1])
                date = re.findall("<td class=\"align_c\">(.*?)</td>", x)[0]
                cache_raw = json.dumps([name, singer, date])
                if temp.get(cache_raw) == None:
                    link_lyric = "https://www.uta-net.com" + re.findall("<a href=\"(.*?)\"", name_link)[0]
                    lyric_kanji = requests.get(link_lyric)
                    lyric_kanji.encoding = "utf-8"
                    lyric_kanji = lyric_kanji.text
                    lyric_raw = re.findall("div id=\"kashi_area\" itemprop=\"text\"((.|\n)*?)/div>", lyric_kanji)
                    lyric = [x.strip().capitalize().replace("\u3000", " ") for x in
                             re.findall(">(.*?)<", lyric_raw[0][0]) if x.strip() != ""]
                    temp[cache_raw] = ""
                    check_lyric_in_cache = check_lyric(" ".join(lyric), cache_lyric)
                    if check_lyric_in_cache[0] == False:
                        cache_lyric.append(check_lyric_in_cache[1])
                        youtube_link_check = ""
                        image_thum_max=""
                        try:
                            li = "https://www.uta-net.com" + re.findall("<p class=\"youtube_button\"><a href=\"(.*?)\"",lyric_kanji.replace("\n", ""))[0]
                            youtube_link = requests.get(li)
                            youtube_link.encoding = "utf-8"
                            youtube_link = \
                            re.findall("https://www.youtube.com/embed/((.|\n)*?)\?", youtube_link.text)[0][0]
                            check_title = check(youtube_link)
                            if check_title[0] != None:
                                dic = {" ": "", "(": "", ")": ""}
                                if multiple_replace(name, dic).lower() in multiple_replace(check_title[0],dic).lower() and multiple_replace(singer, dic).lower() in multiple_replace(check_title[1], dic).lower():
                                    youtube_link_check = "https://www.youtube.com/watch?v=" + youtube_link
                                    print("https://www.youtube.com/watch?v=" + youtube_link)
                                    image_thum_max = check_title[2]

                            # check_title=check(youtube_link)
                            # if check_title[0] != None:
                            #     dic = {" ": "", "(": "", ")": ""}
                            #     if multiple_replace(name, dic).lower() in multiple_replace(check_title[0],dic).lower() and multiple_replace(singer, dic).lower() in multiple_replace(check_title[1], dic).lower():
                            #         youtube_link_check = "https://www.youtube.com/watch?v=" + youtube_link
                            #         print("https://www.youtube.com/watch?v=" + youtube_link)

                        except:
                            pass
                        avata_singer = "/assets_lyric_finder/img/singer/default_singer.jpg"
                        try:
                            link_dow = re.findall("<img src=\"(.*?)\"",re.findall("<div class=\"right\">((.|\n)*?)</div>", lyric_kanji)[0][0])[0]
                            if "http" in link_dow:
                                avata_singer = "assets_lyric_finder/img/singer/iruyas_" + link_dow.split("/")[-1]
                                print(link_dow)
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

                        if "http" in youtube_link_check:
                            data_output = {"name": name.strip().capitalize(),"name_ro":name_romanji.strip().capitalize(), "singer": singer.strip().capitalize(),"date": date, "avata_singer": avata_singer,"link_youtube": youtube_link_check, "thumb_max": image_thum_max,"thumbnail": "http://img.youtube.com/vi/" + youtube_link_check.split("v=")[-1] + "/0.jpg", "lyric": lyric_data}
                        else:
                            data_output = {"name": name.strip().capitalize(),"name_ro":name_romanji.strip().capitalize(), "singer": singer.strip().capitalize(), "date": date, "avata_singer": avata_singer,"link_youtube": youtube_link_check, "thumb_max": "", "thumbnail": "","lyric": lyric_data}

                        # if "http" in youtube_link_check:
                        #     data_output = {"name": name.strip().capitalize(), "singer": singer.strip().capitalize(),"date": date, "avata_singer": avata_singer,"link_youtube": youtube_link_check,"thumbnail": "http://img.youtube.com/vi/" + youtube_link_check.split("v=")[-1] + "/0.jpg", "lyric": lyric_data}
                        # else:
                        #     data_output = {"name": name.strip().capitalize(), "singer": singer.strip().capitalize(),"date": date, "avata_singer": avata_singer,"link_youtube": youtube_link_check, "thumbnail": "", "lyric": lyric_data}

                        save(data_output,
                             "data_lyric_finder/" + str(datetime.now()).replace(".", "_").replace(" ", "_").replace("-","_").replace(":", "_") + ".json")
                        save_(cache_lyric, "cache_lyric.json")
                        S("whiye.jpg",data_output)
                        print("Cron ok")
            # except:
            except Exception as e:
                print(e)
                ctn = connect.connect(user="admin_user", password="eup.mobi", host="103.253.145.165",
                                      database="admin_songlyrics")
                cusor = ctn.cursor()

                continue

        with open("cache_uta_net.json", "w", encoding="utf-8") as file:
            json.dump(temp, file, ensure_ascii=False,indent=4)

    for d in data_cron:
        print(d)



crawl()

