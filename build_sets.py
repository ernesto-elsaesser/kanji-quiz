import csv
import json

with open("jouyou.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    rows = list(reader)

for set_grade in ["1", "2"]:

    kanji_dict = {}
    for index, kanji, kanji_old, radical, strokes, grade, year, meanings, on, kun, frequency, jlpt in rows:
        if grade == set_grade:
            kanji_dict[kanji] = (meanings.upper(), on, kun)

    with open(f"grade{set_grade}.json", "w", encoding="utf-8") as f:
        json.dump(kanji_dict, f, indent=4, ensure_ascii=False)
