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
import time

url_vote = "http://japanesesonglyrics.com/wp-admin/admin-ajax.php"

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
    # print(urllib.parse.quote(text))
    payload = "async=translate,sl:"+srt+",tl:"+dest+",st:" + urllib.parse.quote(text) + ",id:1541997726654,qc:true,ac:true,_id:tw-async-translate,_pms:s,_fmt:pc"
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring).text
    try:
        roman=re.findall("tw-answ-source-romanization\">(.*?)</span>",response)[0].strip()
    except:
        roman=text
    try:
        en=re.findall("tw-answ-target-text\">(.*?)</span>",response)[0].strip()
    except:
        en=text

    return [roman,en]


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

querystring_vote = {"_fs_blog_admin":"true"}
headers_vote = {
    'cookie':"wp-saving-post=22909-check; wordpress_4dda44f2851085a46a0d9de2bad94d36=admin%7C1546047790%7COsB8FnKVfqV9Hh1t4N6RgzobFddWJYa516sfLe5Xory%7C0163df8bcd12e9a4c74d74102ce013d04f7a384e462e3090562dfd2f7e1f933d; _ga=GA1.2.397996287.1543393060; _gid=GA1.2.1558347181.1545615290; yasr_visitor_vote_cookie=a%3A3%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A7%3A%22post_id%22%3Bs%3A4%3A%221035%22%3Bs%3A6%3A%22rating%22%3Bs%3A3%3A%225.0%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A7%3A%22post_id%22%3Bs%3A5%3A%2222466%22%3Bs%3A6%3A%22rating%22%3Bs%3A3%3A%225.0%22%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A7%3A%22post_id%22%3Bs%3A5%3A%2222621%22%3Bs%3A6%3A%22rating%22%3Bs%3A3%3A%225.0%22%3B%7D%7D; wordpress_test_cookie=WP+Cookie+check; wordpress_logged_in_4dda44f2851085a46a0d9de2bad94d36=admin%7C1546047790%7COsB8FnKVfqV9Hh1t4N6RgzobFddWJYa516sfLe5Xory%7C9ec38c1397f9b22b0cc173effc06bb1b35e68bbcb26a7ca71d8087b0f9d41639; wp-settings-1=libraryContent%3Dbrowse%26editor%3Dtinymce%26uploader%3D1; wp-settings-time-1=1545874990",
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

    payload =  "action=yasr_send_overall_rating&nonce=986c0d1ac4&rating="+str(rate)+"&post_id="+str(id)

    response = requests.request("POST", url_vote, data=payload, headers=headers_vote, params=querystring_vote)
    print(response.text)
    print(payload)



def insert_rate(data_vote,cusor,ctn):
    sql="""INSERT INTO wp_yasr_log (post_id,multi_set_id,user_id,vote,date,ip) 
                               VALUES (%s,%s,%s,%s,%s,%s)"""
    cusor.execute(sql, data_vote)
    ctn.commit()

def update_des_image(id,post_content,cusor,ctn):
    post_content=post_content.replace("\"","\"\"")
    sql = "UPDATE wp_posts SET post_title =\""+post_content+"\" , post_excerpt =\""+post_content  +"\" WHERE ID = " +str(id)
    cusor.execute(sql)
    sql = """INSERT INTO wp_postmeta (post_id,meta_key,meta_value) 
                                   VALUES (%s,%s,%s)"""
    cusor.execute(sql, (id,"_wp_attachment_image_alt",post_content))
    ctn.commit()


def form(name_song,name_singer,furigana,english,link_video,ro_name):
    if randint(0, 1) == 0:
        mobai = """<p style="text-align: justify;">Today we bring to you the <strong>{0} of {1}</strong><strong> with FULL Japanese lyric and English translation.</strong> Besides that, you can also read the lyric in hiragana or romaji and watch the music video.</p>""".format(name_song,name_singer)
    else:
        mobai = """<p style="text-align: justify;">This post will show you the <strong>FULL Japanese lyric</strong> (both kanji, hiragana and romaji) <strong>and English translation of {0} - {1}.</strong> Plus, you can also listen to the {0} song while reading the lyric.</p>""".format(name_song,name_singer)
    if randint(0, 1) == 0:
        ketbai = """<p style="text-align: justify;">We hope that you guys already found what you looking for, the <strong>FULL lyric and english translation of {0} - {1}</strong> and some information of this Japanese song.
    Let us know your favorite lyric sentences in the comment and don't forget to bookmark this website to read a lot of song lyrics in the future.</p>""".format(name_song,name_singer)
    else:
        ketbai = """<p style="text-align: justify;">Are you satisfy with the <strong>{0} - {1} lyrics and English translation</strong> that we bring to you today? Let us know in the comment and don't forget to bookmark this website to read a lot of song lyrics and translations in the future.</p>""".format(name_song,name_singer)

    content_table = """<h3>Japanese lyrics (Kanji, Hiragana, Romaji)</h3>
                        <p style="text-align: justify;">{0}</p><br>
                        <h3>English translation (Google auto translate)</h3><p style="text-align: justify;">{1}</p>
                           """.format(furigana,english)

    table=content_table
    if "https://www.youtube.com/embed/" != link_video:
        f = mobai \
            + "<h2><strong>{0} - {1}</strong></h2>" + "\n" \
            + "<ul><li>Song Information</li><li>Japanese lyrics (Kanji, Hiragana, Romaji)</li><li>English translation</li></ul>" + "\n" \
            + "<h3>Song Information</h3>" + "\n" \
            + """<ul><li>Song's Orginal Name: <strong>{0}</strong></li><li>Song's Romaji Name: <strong>{3}</strong></li><li>Singer: <strong>{1}</strong></li><li>Song Music Video:</li></ul>""" +'<iframe src={2} width="853" height="480" frameborder="0" allowfullscreen="allowfullscreen"></iframe>' +"\n\n" \
            + "<hr />" + "\n\n" \
            + table + "\n" \
            + "" + "\n" \
            + ketbai
    else:
        f = mobai \
            + "<h2><strong>{0} - {1}</strong></h2>" + "\n" \
            + "<ul><li>Song Information</li><li>Japanese lyrics (Kanji, Hiragana, Romaji)</li><li>English translation</li></ul>" + "\n" \
            + "<h3>Song Information</h3>" + "\n" \
            + """<ul><li>Song's Orginal Name: <strong>{0}</strong></li><li>Song's Romaji Name: <strong>{3}</strong></li><li>Singer: <strong>{1}</strong></li></ul>""" + "\n\n" \
            + "<hr />" + "\n\n" \
            + table + "\n" \
            + "" + "\n" \
            + ketbai
    f = """<script type="application/ld+json">{"@context":"http:\/\/schema.org\/","@type":"BlogPosting","datePublished":"2018-11-29T03:18:10+00:00","headline":"FULL lyric and english translation","mainEntityOfPage":{"@type":"WebPage","@id":"http:\/\/japanesesonglyrics.com\/"},"author":{"@type":"Person","name":"admin"},"publisher":{"@type":"Organization","name":"Japanese Song Lyrics","logo":{"@type":"ImageObject","url":"","width":0,"height":0}},"dateModified":"2018-11-29T03:18:10+00:00","image":{"@type":"ImageObject","url":"http:\/\/japanesesonglyrics.com\/wp-content\/uploads\/2018\/11\/pic5ture-4236.jpg","width":480,"height":360},"name":"FULL lyric and english translation","Review":{"@type":"Review","name":"FULL lyric and english translation","author":{"@type":"Person","name":"admin"},"datePublished":"2018-11-29T03:18:10+00:00","reviewRating":{"@type":"Rating","ratingValue":"""+"\""+str(randint(45,50)/10)  +"\""+"""}}}</script>"""+f.format(name_song,name_singer,link_video,ro_name)
    return f
#




from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
client = Client('http://japanesesonglyrics.com/xmlrpc.php', 'admin', 'FpkVt192U0xA2uBWxX')
image_thum = os.listdir("image_des_wp_pipop")

def insert_pipop_wordpress(filename,data):
    kan = ""
    en="\n\n"
    for x in data["lyric"]:
        kan = kan + x["furigana"] + "\n" + x["roman"] + "\n\n"
        en = en + x["en"]+ "\n\n"

    data_image = {
        'name': str(time.time())+'.jpg',
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
    post.content = form(data["name"],data["singer"],kan,en,"https://www.youtube.com/embed/"+data["link_youtube"].split("v=")[-1],data["name_ro"])
    post.post_status = 'publish'
    post.thumbnail = attachment_id
    post.id = client.call(posts.NewPost(post))

    now_1 = datetime.now()
    # print((post.id, -1, 1, random.randint(45, 50) / 10, now_1, "X.X.X.X"))
    #
    # print((attachment_id,
    #        "{0} lyric, {0} english translation, {0} {1} lyrics".format(data["name"],
    #                                                                    data["singer"])))
    ctn = connect.connect(user="admin_user", password="eup.mobi", host="103.253.145.165",
                          database="admin_songlyrics")
    cusor = ctn.cursor()
    insert_rate((post.id, -1, 1, random.randint(45, 50) / 10, now_1, "X.X.X.X"),cusor,ctn)
    update_des_image(attachment_id,
                     "{0} lyric, {0} english translation, {0} {1} lyrics".format(data["name"],
                                                                               data["singer"]),cusor,ctn)
    # admin_score(post.id,random.randint(45,50)/10)
    print("ok pipop_wp!")



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
def tag_youtube(s):
    if s==None:
        return ""
    return "".join(s)
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

ctn = connect.connect(user="admin_user", password="eup.mobi", host="103.253.145.165",
                          database="pikasmart")
cusor = ctn.cursor()
import requests
import json
cusor.execute("SELECT id FROM  lyric_finder_songs WHERE  name_singer LIKE  'babymetal'")
id=[x[0] for x in cusor.fetchall()]
print(id)
import re
for x in id:
    data_song=json.loads(requests.get("http://pikasmart.com/api/appLyricFinderSongs/song?id={}".format(str(x))).text)
    lyric=json.loads(requests.get("http://pikasmart.com/api/appLyricFinderSongSentences/getListLyricsBylanguageCode?song_id={}".format(str(x))).text)

    data_out={}
    data_out["name"]=data_song["Song"]["name"]
    data_out["name_ro"]=data_song["Song"]["name_ro"]
    data_out["singer"]=data_song["Song"]["singer_name"]
    data_out["date"]=""
    data_out["avata_singer"]=""
    data_out["link_youtube"]=data_song["Song"]["url"]
    data_out["thumbnail"]=data_song["Song"]["thumbnail"]
    id_you=data_out["link_youtube"].split("=")[-1]
    check_title = check(id_you)
    data_out["thumb_max"]=data_out["thumbnail"]
    if check_title[0] != None:
        data_out["thumb_max"]=check_title[2]

    lyric_d=[]
    for x in lyric["Data"]:
        kanji=x["sentence_value"]
        kanna=x["sentence_hira"]
        romanji=x["sentence_ro"]
        furi=get_furi(kanji)
        en=trans(kanji,"ja","en")[1]
        lyric_d.append({"kanji":kanji,"roman":romanji,"hira_kata":kanna,"furigana":furi,"en":en})
    data_out["lyric"]=lyric_d
    insert_pipop_wordpress("whiye.jpg", data_out)
    print(data_out["name"])

