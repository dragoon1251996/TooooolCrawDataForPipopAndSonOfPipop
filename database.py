import json
import  re
import mysql.connector as connect
ctn1=connect.connect(user="admin_user",password="eup.mobi",host="103.253.145.165",database="pikasmart")
cusor1=ctn1.cursor()

def multiple_replace(string, rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]), flags=re.DOTALL)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)
def config_text(s):
    s=s.lower().replace("\u3000"," ")
    dic = {"\n": " ", "\"": " ", "\'": " ", "、": " ", "。": " ","\r":" ","!":" ",".":" ",",":" ","\u3000":" ","\\":" ","\ufeff":" "}
    temp= multiple_replace(re.sub(u"([\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f-\u3300-\u33ff\ufe30-\ufe4f\uf900-\ufaff\U0002f800-\U0002fa1f\u30a0-\u30ff\u2e80-\u2eff\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf]+)", r"(((\1)))", s),dic)
    kan=[x for x in "".join(re.findall("\(\(\((.*?)\)\)\)",temp)) if x !=" "]
    eng=[y for y in " ".join(re.findall("\)\)\)(.*?)\(\(\(",")))"+temp+"(((")).split(" ") if y!=""]
    return list(set(kan+eng))


print(config_text("でも正,!...しい嘘 のつき方 hello"))
sql_lyric="""SELECT song_period_id, sentence_value from lyric_finder_song_sentences"""
cusor1.execute(sql_lyric)
data_lyric=cusor1.fetchall()

data_l={}
for x in data_lyric:
    data_l[x[0]]=x[1]







sql="""SELECT id,song_id from lyric_finder_song_periods"""
cusor1.execute(sql)
data=cusor1.fetchall()
temp={}
for x in data:
    t=[]
    try:
        if temp.get(str(x[1]))==None:
            temp[str(x[1])]=data_l[x[0]]
        else:
            temp[str(x[1])]=temp[str(x[1])]+" "+data_l[x[0]]
    except:
        continue




for x in temp:
    temp[x]=config_text(temp[x])


with open("cache_lyric.json","w",encoding="utf-8") as f:
    json.dump(list(temp.values()),f,ensure_ascii=False)