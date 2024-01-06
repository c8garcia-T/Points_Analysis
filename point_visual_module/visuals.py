import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from points_module.data_build import build_points_by_teacher_per_class_bar_data


def points_by_teacher_per_class_bar(df):
    data = build_points_by_teacher_per_class_bar_data(df)
    fig = px.bar(data, x="teacher", y="count", hover_data=["percentage"])
    fig.update_layout(
        title_text="Distribution of Point Assignment Instances by Teacher"
    )
    fig.show()


def points_by_reasons_per_class_bar(df):
    data = df["reason"].value_counts().reset_index()
    data["percentage"] = (data["count"] / len(df)).round(2) * 100
    fig = px.bar(data, x="reason", y="count", hover_data=["percentage"])
    fig.update_layout(title_text="Distribution of Point Assignment Instances by Reason")
    fig.show()


def plot_box_based_on_positive_to_negative_point_ratio(df):
    # test na
    fig = px.box(
        df["Positive to Negative Points Ratio"],
        title="Net Points Distribution",
    )
    fig.show()


def plot_box_based_on_net_points(df):
    # test na
    fig = px.box(
        df["Points"],
        title="Net Points Distribution",
    )
    fig.show()
