import os
import json
import html2text
d=os.listdir("full_data")
di=os.listdir("full_data_config")

d=list(set(d)-set(di))
print(d)
err=[]
i=0
from furigana.furigana import split_furigana
import re
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

def get_furi(s):
    temp=[]
    for x in s.split(" "):
        try:
            temp.append(conv_final(split_furigana(x)))
        except:
            temp.append(x)

    return " ".join(temp)


# print(get_furi("再びの幕を開ける章 赤に染めろ 街を走るこの報道"))


ind=json.load(open("ind.json",encoding="utf-8"))["ind"]
with open("ind.json", "w", encoding="utf-8") as f:
    json.dump({"ind":ind+100000}, f, ensure_ascii=False, indent=4)

i=ind


for x in d:

    i+=1
    print(i)
    try:
        dataa=json.load(open("full_data/"+x,encoding="utf-8"))
        print(dataa)
        dataa["name"]=html2text.html2text(dataa["name"]).replace("\n"," ").strip()
        dataa["name_ro"]=html2text.html2text(dataa["name_ro"]).replace("\n"," ").strip()
        dataa["singer"]=html2text.html2text(dataa["singer"]).replace("\n"," ").strip()
        for x1 in range(len(dataa["lyric"])):
            # print(dataa["lyric"][x]["hira_kata"])
            dataa["lyric"][x1]["hira_kata"]=get_hira_kata(dataa["lyric"][x1]["kanji"])
            dataa["lyric"][x1]["furigana"]=get_furi(dataa["lyric"][x1]["kanji"])

        with open("full_data_config/"+x,"w",encoding="utf-8") as f:
            json.dump(dataa,f,ensure_ascii=False,indent=4)

    except:
        err.append(x)

print(err)


