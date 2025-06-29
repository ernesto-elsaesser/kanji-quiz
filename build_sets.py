import os
import csv
import json


EXCLUDE = "兄弟姉妹"
NUMBERS = "一二三四五六七八九十百千万"

kanjis = {}

with open("kanji.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for index, kanji, kanji_old, radical, strokes, grade, year, meanings, on, kun, frequency, jlpt in reader:
        if kanji in EXCLUDE:
            continue
        kanjis[kanji] = {
            "grade": grade,
            "jlpt": int(jlpt),
            "meaning": meanings.split(" (")[0].split("|")[0],
            "ons": on.split("|")[:3],
            "kuns": kun.split("|")[:3],
            "pinyin": "?",
        }

with open("hanzi.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for rank, char, pinyin, pinyin_no_accents, meaning, alternative, alternative2, trad1, trad2 in reader:
        if char in kanjis:
            kanjis[char]["pinyin"] = pinyin


os.makedirs("sets", exist_ok=True)


def build_set(name, include):

    kanji_dict = {k: i for k, i in kanjis.items() if include(k, i)}
    with open(f"sets/{name}.json", "w", encoding="utf-8") as f:
        json.dump(kanji_dict, f, indent=4, ensure_ascii=False)


for grade_num in range(1, 7):
    build_set(f"GRADE {grade_num}", lambda k, i: i["grade"] == str(grade_num))

for jlpt_level in range(6):
    build_set(f"JLPT N{jlpt_level}", lambda k, i: i["jlpt"] == jlpt_level)

build_set("NUMBERS", lambda k, _: k in NUMBERS)
