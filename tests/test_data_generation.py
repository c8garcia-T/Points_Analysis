import numpy as np
import os
import sys
from statistics import mode

sys.path.append(os.getcwd())

from points_module.data_wrangling import (
    sheets_merge,
    data_wrangling,
    exact_duplicates_handling,
)
from points_module.data_privacy import anonymize_student_n_teacher
from points_module.data_generation import aggregate_data_by_student


def test_exact_duplicates_handling():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=files)
        result = sheets_merge(os.path.join(data_dir, files[rand_indx]))
    else:
        result = sheets_merge(os.path.join(data_dir, files[0]))
    result = anonymize_student_n_teacher(result)
    result = data_wrangling(result)
    result = exact_duplicates_handling(result)
    min_all_time_date = result["date"].min()
    max_all_time_date = result["date"].max()
    records_original = result.shape[0]
    aggregate_values_original_all = result["value"].sum()
    total_original_comments = result["comments"].notna().sum()
    random_student = np.random.choice(result.student.tolist())
    random_student_nteachers = result[result.student == random_student][
        "teacher"
    ].nunique()
    random_student_comments_count = result[result.student == random_student][
        "comments"
    ].count()
    random_student_reason_mode = mode(
        result[result.student == random_student]["reason"].tolist()
    )
    result = aggregate_data_by_student(result)
    assert result[("Records", "start")].min() == min_all_time_date
    assert result[("Records", "end")].max() == max_all_time_date
    assert records_original == result[("Records", "count")].sum()
    assert aggregate_values_original_all == result[("Points", "sum")].sum()
    assert total_original_comments == result[("Comments", "count")].sum()
    # random student case for testing
    assert random_student_nteachers == result.loc[random_student]["Teacher"]["nunique"]
    assert (
        random_student_comments_count == result.loc[random_student]["Comments"]["count"]
    )
    assert random_student_reason_mode == result.loc[random_student]["Reason"]["mode"]
