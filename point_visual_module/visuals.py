import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from points_module.data_build import build_points_by_teacher_per_class_bar_data
import numpy as np


def points_by_teacher_per_class_bar(df):
    data = build_points_by_teacher_per_class_bar_data(df)
    fig = px.bar(data, x="teacher", y="count", hover_data=["percentage"])
    fig.update_layout(
        title_text="Distribution of Point Assignment Instances by Teacher"
    )
    return fig


def points_by_reasons_per_class_bar(df, top_three_filter=False):
    data = df["reason"].value_counts().reset_index()
    class_median = data["count"].median()
    if top_three_filter:
        data = data.iloc[:3]
        title_use = "Top Three Reasons For Point Assignment"
    else:
        title_use = "Distribution of Point Assignment Instances by Reason"
    data["percentage"] = (data["count"] / len(df)).round(2) * 100

    fig = px.bar(data, x="reason", y="count", hover_data=["percentage"])
    fig.update_layout(title_text=title_use)
    fig.add_hline(
        y=class_median, line_dash="dash", line_color="red", annotation_text="median"
    )
    fig
    if top_three_filter:
        print(f'Top Three Reasons: {", ".join(data["reason"].tolist())}')
    return fig


def plot_box_based_on_positive_to_negative_point_ratio(df):
    # test na
    fig = px.box(
        df["Positive to Negative Points Ratio"],
        title="Positive-to-Negative Ratio Distribution",
    )
    return fig


def plot_box_based_on_net_points(df):
    # test na
    fig = px.box(
        df["Points"],
        title="Net Points Distribution and statistics",
    )
    return fig


def top_n_bottom_net_point_perf_bar(df_aggregated, df_plot):
    # Test na
    fig = px.bar(
        df_plot,
        x="student",
        y="Points",
        color="Points",
        color_continuous_scale="RdBu_r",
        color_continuous_midpoint=0,
        title="Top and Bottom Performing Students based on Net Points",
    )

    class_median = df_aggregated[("Points", "sum")].median()
    fig.add_hline(
        y=class_median,
        line_dash="dash",
        line_color="red",
        annotation_text="class median",
    )
    return fig


def top_n_bottom_positive_to_negative_ratio_perf_bar(df_aggregated_ratio, df_plot):
    class_mean = df_aggregated_ratio[
        ("Positive to Negative Points Ratio", "Static Estimate")
    ].mean()
    if class_mean == np.inf:
        df_plot["Positive to Negative Points Ratio"] = df_plot[
            "Positive to Negative Points Ratio"
        ].replace(np.inf, 100)
    # Test na
    fig = px.bar(
        df_plot,
        x="student",
        y="Positive to Negative Points Ratio",
        color="Positive to Negative Points Ratio",
        color_continuous_scale="Reds_r",
        color_continuous_midpoint=0,
        title="Top and Bottom Performing Students based on Positive-to-Negative Point Ratio",
    )

    class_median = df_aggregated_ratio[
        ("Positive to Negative Points Ratio", "Static Estimate")
    ].median()
    class_std = df_aggregated_ratio[
        ("Positive to Negative Points Ratio", "Static Estimate")
    ].std()
    if not class_mean == np.inf:
        fig.add_hline(
            y=class_median,
            line_dash="dash",
            line_color="red",
            annotation_text="class median",
        )

    date_info_min = df_aggregated_ratio.loc[df_plot["student"]][
        ("Records", "start")
    ].min()
    date_info_max = df_aggregated_ratio.loc[df_plot["student"]][
        ("Records", "end")
    ].max()

    print(f"Data Range: {date_info_min.date()} to {date_info_max.date()}")
    print(
        f"Mean: {round(class_mean,2)} Std: {round(class_std,2)} Median: {round(class_median,2)}"
    )
    return fig


def cumulative_sum_of_points_time_series_line(df_time_series):
    term_median = df_time_series.running_sum.median()

    fig = px.line(
        df_time_series,
        x="date",
        y="running_sum",
        color="student",
        markers=True,
        line_shape="linear",
        color_discrete_map={
            key: "darksalmon" for key in df_time_series.student.unique()
        },
        title="Cumulative Points Over Time",
    )
    fig.update_traces(line=dict(width=1.5))
    fig.update_traces(marker=dict(size=3))

    fig.add_hline(y=0, line_dash="dash", line_color="gold", annotation_text="Zero Line")
    if not term_median == np.inf:
        fig.add_hline(
            y=term_median, line_dash="dash", line_color="gold", annotation_text="Median"
        )
    return fig
