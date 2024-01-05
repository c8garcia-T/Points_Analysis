# functions for data wrangling
import pandas as pd
import numpy as np


def sheets_merge(source_path: str):
    column_names = ["date", "reason", "value", "comments", "teacher"]
    dict_output = pd.read_excel(
        source_path, sheet_name=None, header=None, names=column_names, usecols="A:E"
    )
    df_list = [df for df in dict_output.values()]
    # creating student column
    for student, df in zip(dict_output.keys(), df_list):
        df["student"] = student
    # combining operation
    df_points = pd.concat(df_list, axis=0, ignore_index=True)
    return df_points


def data_wrangling(df):
    # processing Value Column str->int
    # pattern
    extract_int_and_sign = r"(\d+)\s*\(\s*([+-])\s*\)"
    # catch values
    int_n_sign_extracted = df.value.str.extract(pat=extract_int_and_sign)
    # convinience renaming
    int_n_sign_extracted.rename(columns={0: "value", 1: "sign"}, inplace=True)
    # sign col str to int
    int_n_sign_extracted["sign_processed"] = int_n_sign_extracted.sign.map(
        {"+": 1, "-": -1}
    )
    int_n_sign_extracted.drop(columns="sign", inplace=True)
    # data type (str) to int
    int_n_sign_extracted = int_n_sign_extracted.astype(int)
    # processed value
    int_n_sign_extracted["value_processed"] = (
        int_n_sign_extracted.value * int_n_sign_extracted.sign_processed
    )
    # replace old value column with processed version
    df["value"] = int_n_sign_extracted["value_processed"]
    # reason and teacher column dtype str -> categorical (non ordered)
    df["reason"] = df["reason"].astype("category")
    df["teacher"] = df["teacher"].astype("category")
    df["student"] = df["student"].astype("category")
    # Generate Columns for aggregation of points
    df["negative_point_assigned"] = df["value"].apply(lambda x: x if x < 0 else np.nan)
    df["positive_point_assigned"] = df["value"].apply(lambda x: x if x > 0 else np.nan)
    return df


def exact_duplicates_handling(df):
    """
    Example:
    If ["date", "reason", "teacher", "student"] are the same.
    That means a teacher simply didn't input the right value on the first attempt or
    where limited by the 5 point option in the attendance page.
    Effect:
    - Proper representation of points assigned.
    """
    # You can merge a row if the following are the same
    criteria_for_duplicates = ["date", "reason", "teacher", "student"]
    # Gather all entries to merge
    duplicate_entries = df[
        df.duplicated(keep=False, subset=criteria_for_duplicates)
    ].copy()
    # Perform Merge
    duplicates_merged = (
        duplicate_entries.groupby(by=criteria_for_duplicates, observed=True)
        .agg(
            {
                "value": "sum",
                "comments": lambda x: x,
                "negative_point_assigned": "sum",
                "positive_point_assigned": "sum",
            }
        )
        .reset_index()
    )
    # Process Comments
    # keep only strings
    duplicates_merged["comments"] = duplicates_merged["comments"].apply(
        lambda x: [i for i in x if not pd.isna(i)]
    )
    # concatenate comments with a space if present else impute with np.nan
    duplicates_merged["comments"] = duplicates_merged["comments"].apply(
        lambda x: " ".join(x) if x else np.nan
    )
    # Correct column order
    duplicates_merged = duplicates_merged.loc[:, df.columns.to_list()]
    # Creating new df without duplicates
    df_no_duplicates = df[
        ~df.duplicated(keep=False, subset=criteria_for_duplicates)
    ].copy()

    # Adding merged rows to original df (w/o duplicates)
    result_df = pd.concat(
        [df_no_duplicates, duplicates_merged], ignore_index=True, axis=0
    )
    return result_df
