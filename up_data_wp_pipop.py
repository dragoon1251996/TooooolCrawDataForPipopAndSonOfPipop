import json
from random import randint
import mysql.connector as connect
ctn=connect.connect(user="admin_user",password="eup.mobi",host="103.253.145.165",database="admin_songlyrics")
cusor=ctn.cursor()
import random
import time
import os

import requests

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




def insert_rate(data_vote):
    sql="""INSERT INTO wp_yasr_log (post_id,multi_set_id,user_id,vote,date,ip) 
                               VALUES (%s,%s,%s,%s,%s,%s)"""
    cusor.execute(sql, data_vote)
    ctn.commit()

def update_des_image(id,post_content):
    sql = "UPDATE wp_posts SET post_title ='"+post_content+"' , post_excerpt ='"+post_content  +"' WHERE ID = " +str(id)
    cusor.execute(sql)
    ctn.commit()
    sql = """INSERT INTO wp_postmeta (post_id,meta_key,meta_value) 
                                   VALUES (%s,%s,%s)"""
    cusor.execute(sql, (id,"_wp_attachment_image_alt",post_content))
    ctn.commit()


def form(name_song,name_singer,furigana,english,link_video):
    if randint(0, 1) == 0:
        mobai = """<p style="text-align: justify;">Today we bring to you the <strong>{0}</strong><strong> with FULL Japanese lyric and English translation.</strong> Beside that, you can also reading the lyric in hiragana or romaji and watching the {1} music video.</p>""".format(name_song,name_singer)
    else:
        mobai = """<p style="text-align: justify;">This post will show you the <strong>FULL Japanese lyric</strong> (both kanji, hiragana and romaji) <strong>and English translation of {0} - {1}.</strong> Plus, you can also listening to the {0} song while reading the lyric.</p>""".format(name_song,name_singer)
    if randint(0, 1) == 0:
        ketbai = """<p style="text-align: justify;">We hope that you guys already found what you looking for, the <strong>FULL lyric and english translation of {0} - {1}</strong> and some information of this japanese song.
    Let us know your favorite lyric sentences in the comment and don't forget to bookmark this website to read a lot of song lyrics in the future.</p>""".format(name_song,name_singer)
    else:
        ketbai = """<p style="text-align: justify;">Are you satisfy with the <strong>{0} - {1} lyric and english translation</strong> that we bring to you today? Let us know in the comment and don't forget to bookmark this website to read a lot of song lyrics and translations in the future.</p>""".format(name_song,name_singer)

    name_table = """<td style="vertical-align: top ;padding: 8px 8px; word-break: break-word; " width="50%">
                    <h3>Original lyric (Japanese lyric)</h3></td>
                    <td style=" vertical-align: top ; padding: 8px 8px; word-break: break-word;" width="50%">
                    <h3>English translation</h3>
                    </td>"""

    content_table = """<tr>
                        <td  style="vertical-align: center ; padding: 0px 10px;  word-break: break-word;">
                        <p style="text-align: justify;">{0}</p>
                        </td>
                        <td style="vertical-align: top ; padding: 13px 10px; word-break: break-word; ">
                        <p style="text-align: justify;">{1}</p>
                        </td>
                        </tr>""".format(furigana,english)

    table = """<font color="black" ><table border="1" width="100%" cellspacing="0" cellpadding="0"><tbody>""" + "\n" + name_table + "\n" + content_table + "\n" + """</tbody></table></font>"""
    if "https://www.youtube.com/embed/" != link_video:
        f = mobai \
            + "<h2><strong>{0} - {1}</strong></h2>" + "\n" \
            + "<ul><li>Song Information</li><li>Original lyric (Japanese lyric)</li><li>English translation</li></ul>" + "\n" \
            + "<h3>Song Information</h3>" + "\n" \
            + """<ul><li>Song's Orginal Name: <strong>{0}</strong></li><li>Singer: <strong>{1}</strong></li><li>Song Music Video:</li></ul>""" +'<iframe src={2} width="853" height="480" frameborder="0" allowfullscreen="allowfullscreen"></iframe>' +"\n\n" \
            + "<hr />" + "\n\n" \
            + table + "\n" \
            + "" + "\n" \
            + ketbai
    else:
        f = mobai \
            + "<h2><strong>{0} - {1}</strong></h2>" + "\n" \
            + "<ul><li>Song Information</li><li>Original lyric (Japanese lyric)</li><li>English translation</li></ul>" + "\n" \
            + "<h3>Song Information</h3>" + "\n" \
            + """<ul><li>Song's Orginal Name: <strong>{0}</strong></li><li>Singer: <strong>{1}</strong>""" + "\n\n" \
            + "<hr />" + "\n\n" \
            + table + "\n" \
            + "" + "\n" \
            + ketbai
    print(link_video)
    f = f.format(name_song,name_singer,link_video)
    return f


from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
client = Client('http://japanesesonglyrics.com/xmlrpc.php', 'admin', 'FpkVt192U0xA2uBWxX')

image_thum = os.listdir("image_des_wp_pipop")


def S(filename,data):

    kan = ""
    for x in data["lyric"]:
        kan = kan + x["furigana"] + "<br>" + x["roman"] + "<br><br>"
    # filename = 'image/1035.jpg'
    data_image = {
        'name': 'whiye.jpg',
        'type': 'image/jpeg',
    }
    if "http" in data["thumbnail"]:
        dow(data["thumbnail"], filename)
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
    post.title = data["name"]+ " - "+data["singer"]+" with FULL lyric and english translation"
    post.content = form(data["name"],data["singer"],kan,"\n"+"Updating!!!","https://www.youtube.com/embed/"+data["link_youtube"].split("v=")[-1])
    post.post_status = 'publish'
    post.thumbnail = attachment_id
    post.id = client.call(posts.NewPost(post))
    from datetime import datetime
    now = datetime.now()
    insert_rate((post.id, -1, 1, random.randint(45, 50) / 10, now, "X.X.X.X"))

    update_des_image(attachment_id,
                     "{0} lyric, {0} english translation, {0} {1} lyrics".format(data["name"],
                                                                               data["singer"]))



S("vuong.jpg",json.load(open("data_lyric_finder/2018_12_21_16_29_49_000435.json",encoding="utf-8")))