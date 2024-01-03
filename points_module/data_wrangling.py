# functions for data wrangling
import pandas as pd


def load_data(source_path: str):
    column_names = ["date", "reason", "value", "comments", "teacher"]
    dict_output = pd.read_excel(
        source_path, sheet_name=None, header=None, names=column_names, usecols="A:E"
    )
    assert type(dict_output) == dict
    df_list = [df for df in dict_output.values()]
    # creating student column
    for student, df in zip(dict_output.keys(), df_list):
        df["student"] = student
    # combining operation
    df_points = pd.concat(df_list, axis=0, ignore_index=True)
    assert df_points.shape[1] == 6
    assert df_points.columns.tolist() == (column_names + ["student"])
    return 1
