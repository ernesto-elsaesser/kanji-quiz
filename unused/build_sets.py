import os
import csv
import json


EXCLUDE = "兄弟姉妹"
NUMBERS = "一二三四五六七八九十百千万"

kanjis: dict[str, dict] = {}

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
            "pinyins": [],
        }

with open("hanzi.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for rank, char, pinyin, pinyin_no_accents, meaning, alt, alt2, trad1, trad2 in reader:
        if pinyin[0].isupper():
            continue
        for kanji in (char[0], alt, alt2, trad1, trad2):
            info = kanjis.get(kanji)
            if info is not None:
                info["pinyins"].append(pinyin)


sets_py = open("sets.py", "w")

sets_py.write("SETS = {\n")


def add_set(name: str, include):

    kanji_dict = {k: i for k, i in kanjis.items() if include(k, i)}
    sets_py.write(f"  '{name}': {kanji_dict},\n")


for grade_num in range(1, 7):
    add_set(f"GRADE {grade_num}", lambda k, i: i["grade"] == str(grade_num))

for jlpt_level in range(1, 6):
    add_set(f"JLPT N{jlpt_level}", lambda k, i: i["jlpt"] == jlpt_level)

add_set("NUMBERS", lambda k, _: k in NUMBERS)

sets_py.write("}\n")

sets_py.close()
