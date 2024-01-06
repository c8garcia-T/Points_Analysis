# Objective: Anonymize Student and Teacher Names
# currently this function only anonymizes teacher names since student is anonymized form source
import pandas as pd
from random import shuffle


def anonymize_student_n_teacher(df):
    teacher_names = df["teacher"].unique()
    random_ids = [i for i, _ in enumerate(teacher_names)]
    shuffle(random_ids)
    mapping_ids = {
        teacher: f"ID_{id_rand}" for id_rand, teacher in zip(random_ids, teacher_names)
    }
    df["teacher"] = df["teacher"].map(mapping_ids)
    return df
