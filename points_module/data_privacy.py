# Objective: Anonymize Student and Teacher Names
# currently this function only anonymizes teacher names since student is anonymized form source
import pandas as pd
import numpy as np


def anonymize_student_n_teacher(df):
    teacher_names = df["teacher"].unique()
    random_ids = set(
        np.random.randint(low=0, high=len(teacher_names) * 10, size=len(teacher_names))
    )
    mapping_ids = {
        teacher: f"ID_{id_rand}" for id_rand, teacher in zip(random_ids, teacher_names)
    }
    df["teacher"] = df["teacher"].map(mapping_ids)
    return df
