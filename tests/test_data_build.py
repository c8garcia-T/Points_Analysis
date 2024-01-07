import numpy as np
import os
import sys

sys.path.append(os.getcwd())

from points_module.data_build import (
    build_aggregated_data_by_student_df,
    build_clean_df,
    build_aggregated_data_by_student_with_static_pos_to_neg_ratio_df,
    build_points_by_teacher_per_class_bar_data,
    build_points_by_reasons_per_class_bar_data,
    build_points_time_series_df,
)


def test_build_clean_df():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=len(files))
        result = build_clean_df(os.path.join(data_dir, files[rand_indx]))
    else:
        result = build_clean_df(os.path.join(data_dir, files[0]))
    assert not result.empty


def test_build_aggregated_data_by_student_df():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=len(files))
        result = build_aggregated_data_by_student_df(
            os.path.join(data_dir, files[rand_indx])
        )
    else:
        result = build_aggregated_data_by_student_df(os.path.join(data_dir, files[0]))
    assert not result.empty


def test_build_aggregated_data_by_student_with_static_pos_to_neg_ratio_df():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=len(files))
        result = build_aggregated_data_by_student_with_static_pos_to_neg_ratio_df(
            os.path.join(data_dir, files[rand_indx])
        )
    else:
        result = build_aggregated_data_by_student_with_static_pos_to_neg_ratio_df(
            os.path.join(data_dir, files[0])
        )
    assert not result.empty


def test_build_points_by_teacher_per_class_bar_data():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=len(files))
        result = build_clean_df(os.path.join(data_dir, files[rand_indx]))
    else:
        result = build_clean_df(os.path.join(data_dir, files[0]))
    result = build_points_by_teacher_per_class_bar_data(result)
    assert not result.empty


def test_build_points_by_reasons_per_class_bar_data():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=len(files))
        result = build_clean_df(os.path.join(data_dir, files[rand_indx]))
    else:
        result = build_clean_df(os.path.join(data_dir, files[0]))
    result = build_points_by_reasons_per_class_bar_data(result)
    assert not result.empty


def test_build_points_time_series_df():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=len(files))
        df = build_clean_df(os.path.join(data_dir, files[rand_indx]))
    else:
        df = build_clean_df(os.path.join(data_dir, files[0]))
    random_student = np.random.choice(df.student.unique().tolist())
    random_student_data = df[df.student == random_student]
    expected_net_points = random_student_data.value.sum()

    result = build_points_time_series_df(df)
    result_for_random_student = (
        result[result["student"] == random_student]
        .sort_values(by="date")
        .reset_index(drop=True)
    )
    assert result_for_random_student["value"].sum() == expected_net_points
    assert result_for_random_student["running_sum"].tolist()[-1] == expected_net_points
