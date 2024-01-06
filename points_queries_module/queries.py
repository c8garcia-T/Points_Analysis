import pandas as pd


def get_head_and_tail_students_based_on_net_points(df):
    df = df.sort_values(by=("Points", "sum"), ascending=False)
    df = pd.concat([df[:3], df[-3:]])
    return df
