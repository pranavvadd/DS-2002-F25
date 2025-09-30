import csv
import json
import pandas as pd

data = [
    [101, "Computer Science", 3.8, "Yes", "15.0"],
    [102, "Mathematics", 3, "No", "12.0"],
    [103, "Physics", 3.9, "Yes", 18.0],
    [104, "Chemistry", 3, "No", "10.0"],
    [105, "Biology", 3.9, "Yes", "14.0"]
]
header = ["student_id", "major", "GPA", "is_cs_major", "credits_taken"]
with open("raw_survey_data.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data)

courses = [
    {
        "course_id": "DS2002",
        "section": "001",
        "title": "Data Science Systems",
        "level": 200,
        "instructors": [
            {"name": "Austin Rivera", "role": "Primary"},
            {"name": "Heywood Williams-Tracy", "role": "TA"}
        ]
    },
    {
        "course_id": "CS2100",
        "section": "002",
        "title": "Data Structures and Algorithms",
        "level": 200,
        "instructors": [
            {"name": "Brianna Morrison", "role": "Primary"},
            {"name": "Xinyao Yi", "role": "Primary"}
        ]
    }
]
with open("raw_course_catalog.json", "w") as file:
    json.dump(courses, file, indent=2)

df = pd.read_csv("raw_survey_data.csv")
df['is_cs_major'] = df['is_cs_major'].replace({'Yes': True, 'No': False})

df['GPA'] = df['GPA'].astype(float)
df['credits_taken'] = df['credits_taken'].astype(float)

df.to_csv("clean_survey_data.csv", index=False)

with open("raw_course_catalog.json") as file:
    data = json.load(file)
df_courses = pd.json_normalize(
    data,
    record_path=['instructors'],
    meta=['course_id', 'section', 'title', 'level']
)
df_courses.to_csv("clean_course_catalog.csv", index=False)