import csv
import json


SIBLINGS = "兄弟姉妹"
NUMBERS = "一二三四五六七八九十百千万"


with open("jouyou.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    rows = list(reader)


def build_set(name, include):

    kanji_dict = {}
    for index, kanji, kanji_old, radical, strokes, grade, year, meanings, on, kun, frequency, jlpt in rows:
        if not include(kanji, grade, year, jlpt, frequency):
            continue
        meanings = meanings.split(" (")[0]
        meaning = meanings.split("|")[0]
        pinyin = "?"
        ons = "、".join(on.split("|")[:3])
        kuns = "、".join(kun.split("|")[:3])
        kanji_dict[kanji] = (meaning, pinyin, ons, kuns)

    with open(name + ".json", "w", encoding="utf-8") as f:
        json.dump(kanji_dict, f, indent=4, ensure_ascii=False)


for grade_num in range(1, 7):
    build_set(f"grade{grade_num}",
              lambda k, g, *_: g == str(grade_num) and k not in SIBLINGS)

build_set("numbers", lambda k, *_: k in NUMBERS)
