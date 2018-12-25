# from random import randint
# import mysql.connector as connect
# ctn=connect.connect(user="admin_user",password="eup.mobi",host="103.253.145.165",database="admin_songlyrics")
# cusor=ctn.cursor()
#
#
#
# # update pipop wordpress
# def insert_rate(data_vote):
#     sql="""INSERT INTO wp_yasr_log (post_id,multi_set_id,user_id,vote,date,ip)
#                                VALUES (%s,%s,%s,%s,%s,%s)"""
#     cusor.execute(sql, data_vote)
#     ctn.commit()
#
# def update_des_image(id,post_content):
#     sql = "UPDATE wp_posts SET post_title ='"+post_content+"' , post_excerpt ='"+post_content  +"' WHERE ID = " +str(id)
#     cusor.execute(sql)
#     ctn.commit()
#     sql = """INSERT INTO wp_postmeta (post_id,meta_key,meta_value)
#                                    VALUES (%s,%s,%s)"""
#     cusor.execute(sql, (id,"_wp_attachment_image_alt",post_content))
#     print("vuong")
#     ctn.commit()
#
#
# for x in range(1000):
#     update_des_image(22678, "Poker faith lyric, Poker faith english translation, Poker faith 315 stars(インテリ ver.) lyrics")
#     insert_rate((22678, -1, 10, 4.8, "2018-12-25 09:48:53.173668", "X.X.X.X"))




import requests

url = "http://japanesesonglyrics.com/wp-admin/admin-ajax.php"

querystring = {"_fs_blog_admin":"true"}

payload = "action=yasr_send_overall_rating&nonce=ae3bbf26bb&rating=4.9&post_id=22848"
headers = {
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

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)