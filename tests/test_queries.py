import numpy as np
import os
import sys

sys.path.append(os.getcwd())
from points_module.data_build import (
    build_aggregated_data_by_student_df,
    build_aggregated_data_by_student_with_static_pos_to_neg_ratio_df,
    build_clean_df,
)
from points_queries_module.queries import (
    get_head_and_tail_students_based_on_net_points,
    get_head_and_tail_students_based_on_positive_to_negative_point_ratio,
    get_comments_usage_by_teacher_info,
)


def test_get_head_and_tail_students_based_on_net_points():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=len(files))
        df = build_aggregated_data_by_student_df(
            os.path.join(data_dir, files[rand_indx])
        )
    else:
        df = build_aggregated_data_by_student_df(os.path.join(data_dir, files[0]))
    top_val_expected = df[("Points", "sum")].max()
    bottom_val_expected = df[("Points", "sum")].min()
    result = get_head_and_tail_students_based_on_net_points(df)
    assert not result.empty
    assert result.shape[0] == 6
    assert result["Points"].iloc[0] == top_val_expected
    assert result["Points"].iloc[-1] == bottom_val_expected


def test_get_head_and_tail_students_based_on_positive_to_negative_point_ratio():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=len(files))
        df = build_aggregated_data_by_student_with_static_pos_to_neg_ratio_df(
            os.path.join(data_dir, files[rand_indx])
        )
    else:
        df = build_aggregated_data_by_student_with_static_pos_to_neg_ratio_df(
            os.path.join(data_dir, files[0])
        )
    top_val_expected = df[
        ("Positive to Negative Points Ratio", "Static Estimate")
    ].max()
    bottom_val_expected = df[
        ("Positive to Negative Points Ratio", "Static Estimate")
    ].min()
    result = get_head_and_tail_students_based_on_positive_to_negative_point_ratio(df)
    assert not result.empty
    assert result.shape[0] == 6
    assert result["Positive to Negative Points Ratio"].iloc[0] == top_val_expected
    assert result["Positive to Negative Points Ratio"].iloc[-1] == bottom_val_expected


def test_get_comments_usage_by_teacher_info():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=len(files))
        df = build_clean_df(os.path.join(data_dir, files[rand_indx]))
    else:
        df = build_clean_df(os.path.join(data_dir, files[0]))
    result = get_comments_usage_by_teacher_info(df)
    assert all(
        df["comments"].describe().reset_index().rename(columns={"index": "About"})
        == result
    )
