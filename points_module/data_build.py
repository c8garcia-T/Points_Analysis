from points_module.data_wrangling import (
    sheets_merge,
    data_wrangling,
    exact_duplicates_handling,
)
from points_module.data_privacy import anonymize_student_n_teacher
from points_module.data_duplicate_handling import aggregate_data_by_student
import pandas as pd


def build_clean_df(raw_data_path: str):
    df = sheets_merge(raw_data_path)
    df = anonymize_student_n_teacher(df)
    df = data_wrangling(df)
    result = exact_duplicates_handling(df)
    return result


def build_aggregated_data_by_student_df(raw_data_path: str):
    result = aggregate_data_by_student(build_clean_df(raw_data_path))
    return result


def build_aggregated_data_by_student_with_static_pos_to_neg_ratio_df(
    raw_data_path: str,
):
    # end of term static estimate

    result = build_aggregated_data_by_student_df(raw_data_path)
    result[("Positive to Negative Points Ratio", "Static Estimate")] = (
        result[("Positive point assigned", "sum")]
        / result[("Negative point assigned", "sum")].abs()
    )
    return result


def build_points_by_teacher_per_class_bar_data(df):
    # Teacher Distribution of points
    result = df["teacher"].value_counts().reset_index(name="count")
    result["percentage"] = (result["count"] / len(df)).round(2) * 100

    return result


def build_points_by_reasons_per_class_bar_data(df):
    # Teacher Distribution of points
    result = df["reason"].value_counts().reset_index(name="count")
    result["percentage"] = (result["count"] / len(df)).round(2) * 100

    return result


def build_points_time_series_df(df):
    group_by_student_df = (
        df.groupby(by=["date", "student"], observed=True)
        .agg({"value": "sum"})
        .reset_index()
    )
    group_by_student_df.sort_values(by=["student", "date"], inplace=True)
    group_by_student_df["running_sum"] = group_by_student_df.groupby(
        by=["student"], observed=False
    ).value.cumsum()

    return group_by_student_df
