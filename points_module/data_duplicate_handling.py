import pandas as pd
from statistics import mode


def aggregate_data_by_student(df):
    # Perform Aggregation by Student
    functions_to_apply = {
        "date": ["count", "min", "max"],
        "value": [lambda x: sum(abs(x)), "sum", "mean", "std", "var"],
        "negative_point_assigned": ["sum", "mean", "std", "var", "count"],
        "positive_point_assigned": ["sum", "mean", "std", "var", "count"],
        "reason": mode,
        "teacher": "nunique",
        "comments": "count",
    }
    result = df.groupby(by="student", observed=False).agg(func=functions_to_apply)
    column_renaming_map_outer_level_0 = {"value": "Points", "date": "Records"}
    column_renaming_map_inner_level_1 = {
        "<lambda_0>": "absolute sum",
        "min": "start",
        "max": "end",
    }
    result.rename(columns=column_renaming_map_outer_level_0, level=0, inplace=True)
    result.rename(columns=column_renaming_map_inner_level_1, level=1, inplace=True)
    # Capitalize Outer Level Column Names
    outer_level_0_names = result.columns.get_level_values(0).unique()
    result.rename(
        columns={i: i.capitalize().replace("_", " ") for i in outer_level_0_names},
        level=0,
        inplace=True,
    )
    return result
