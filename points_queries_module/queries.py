import pandas as pd


def get_head_and_tail_students_based_on_net_points(df):
    df = (
        df.sort_values(by=("Points", "sum"), ascending=False)["Points", "sum"]
        .reset_index()
        .droplevel(level=1, axis=1)
    )
    df = pd.concat([df[:3], df[-3:]])
    return df


def get_head_and_tail_students_based_on_positive_to_negative_point_ratio(df):
    df = (
        df.sort_values(
            by=("Positive to Negative Points Ratio", "Static Estimate"), ascending=False
        )["Positive to Negative Points Ratio", "Static Estimate"]
        .reset_index()
        .droplevel(level=1, axis=1)
    )
    df = pd.concat([df[:3], df[-3:]])
    return df


def get_comments_usage_by_teacher_info(df):
    comments_info_df = (
        df["comments"].describe().reset_index().rename(columns={"index": "About"})
    )
    comments_count = comments_info_df.iloc[0, 1]
    comments_usage_proportion = round((comments_count / df.shape[0]) * 100, 2)
    print("Dataset Size:", df.shape[0])
    print("Records with Comments:", comments_count)
    print("Percentage Usage of Comments:", comments_usage_proportion)
    return comments_info_df
