import csv
import json

with open("jouyou.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    rows = list(reader)

for grade_num in range(1, 7):

    kanji_dict = {}
    for index, kanji, kanji_old, radical, strokes, grade, year, meanings, on, kun, frequency, jlpt in rows:
        if int(grade) != grade_num:
            continue
        meaning = meanings.split("|")[0]
        ons = "、".join(on.split("|")[:3])
        kuns = "、".join(kun.split("|")[:3])
        kanji_dict[kanji] = (meaning, ons, kuns)

    with open(f"grade{grade_num}.json", "w", encoding="utf-8") as f:
        json.dump(kanji_dict, f, indent=4, ensure_ascii=False)
