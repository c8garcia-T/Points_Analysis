import numpy as np
import plotly.express as px
import streamlit as st
from point_visual_module.visuals import (
    cumulative_sum_of_points_time_series_line,
)


def reasons_bar(df_points_in, selected_student):
    subset_df_by_student = df_points_in[df_points_in.student == selected_student].copy()
    reasons_subset_by_student = subset_df_by_student.reason.value_counts(
        normalize=False
    ).reset_index()
    reasons_subset_by_student["count"] = reasons_subset_by_student["count"].apply(
        lambda x: x if x > 0 else np.nan
    )
    reasons_subset_by_student.dropna(subset=["count"], inplace=True)
    reasons_subset_by_student["Percentage"] = (
        reasons_subset_by_student["count"] / reasons_subset_by_student["count"].sum()
    ) * 100
    title_for_student = f"Reason Distribution For: {selected_student}"
    fig = px.bar(
        reasons_subset_by_student,
        x="reason",
        y="count",
        hover_data=["Percentage"],
        title=title_for_student,
    )
    return fig


def section_cumulative_sum_of_points_time_series_line_single_student(df):
    fig = cumulative_sum_of_points_time_series_line(df)
    st.plotly_chart(fig)
