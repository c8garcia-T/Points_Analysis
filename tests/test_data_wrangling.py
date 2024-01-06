import numpy as np
import os
import sys

sys.path.append(os.getcwd())

from points_module.data_wrangling import (
    sheets_merge,
    data_wrangling,
    exact_duplicates_handling,
)
from points_module.data_privacy import anonymize_student_n_teacher


def test_sheets_merge():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=files)
        result = sheets_merge(os.path.join(data_dir, files[rand_indx]))
    else:
        result = sheets_merge(os.path.join(data_dir, files[0]))
    assert result.shape[1] == 6
    assert result.columns.tolist() == (
        ["date", "reason", "value", "comments", "teacher"] + ["student"]
    )


def test_data_wrangling():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=files)
        result = sheets_merge(os.path.join(data_dir, files[rand_indx]))
    else:
        result = sheets_merge(os.path.join(data_dir, files[0]))
    result = anonymize_student_n_teacher(result)
    result = data_wrangling(result)
    # Check Creation of columns
    assert all(
        (
            (
                result["negative_point_assigned"].fillna(0)
                + result["positive_point_assigned"].fillna(0)
            )
            == result["value"]
        ).tolist()
    )
    # Desired data types
    desired_dtypes = {
        "value": np.int64,
        "negative_point_assigned": np.float64,
        "positive_point_assigned": np.float64,
    }

    # Check if DataFrame has the desired data types

    assert all(result[col].dtype == dtype for col, dtype in desired_dtypes.items())
    assert len(result["reason"].cat.categories) > 1
    assert len(result["teacher"].cat.categories) > 1
    assert len(result["student"].cat.categories) > 1


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

    criteria_for_duplicates = ["date", "reason", "teacher", "student"]
    # Gather all entries to merge
    duplicate_entries = result[
        result.duplicated(keep=False, subset=criteria_for_duplicates)
    ].copy()
    duplicate_entries["count"] = 1
    # Perform Merge
    duplicates_merged_count_info = (
        duplicate_entries[criteria_for_duplicates + ["count"]]
        .groupby(by=criteria_for_duplicates, observed=True)
        .agg("count")
        .reset_index()
    )["count"]
    records_to_keep_count = duplicates_merged_count_info.shape[0]

    record_count_before_duplicate_handling = result.shape[0]
    expected_record_count = (
        record_count_before_duplicate_handling - duplicates_merged_count_info.sum()
    ) + records_to_keep_count
    result = exact_duplicates_handling(result)
    assert result.shape[0] == expected_record_count
    assert (
        (
            result.negative_point_assigned.fillna(0)
            + result.positive_point_assigned.fillna(0)
        )
        == result.value
    ).sum() == result.shape[0]
    assert result["comments"].dtype == object
