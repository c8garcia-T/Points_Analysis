import streamlit as st
from point_visual_module.visuals import (
    points_by_teacher_per_class_bar,
    points_by_reasons_per_class_bar,
    plot_box_based_on_net_points,
    plot_box_based_on_positive_to_negative_point_ratio,
    top_n_bottom_net_point_perf_bar,
    top_n_bottom_positive_to_negative_ratio_perf_bar,
    cumulative_sum_of_points_time_series_line,
)

from points_queries_module.queries import (
    get_head_and_tail_students_based_on_net_points,
    get_head_and_tail_students_based_on_positive_to_negative_point_ratio,
)


def section_cumulative_sum_of_points_time_series_line(df):
    st.header("Point Analysis Over Time", divider="red")

    fig = cumulative_sum_of_points_time_series_line(df)
    st.plotly_chart(fig)


def top_and_bottom_student_section(
    aggregated_data_by_student_df_in,
    head_and_tail_students_based_on_net_points_df_in,
    aggregated_data_by_student_with_static_pos_to_neg_ratio_df_in,
    head_and_tail_students_based_on_positive_to_negative_point_ratio_df_in,
):
    fig = top_n_bottom_net_point_perf_bar(
        aggregated_data_by_student_df_in,
        head_and_tail_students_based_on_net_points_df_in,
    )
    st.plotly_chart(fig)
    fig = top_n_bottom_positive_to_negative_ratio_perf_bar(
        aggregated_data_by_student_with_static_pos_to_neg_ratio_df_in,
        head_and_tail_students_based_on_positive_to_negative_point_ratio_df_in,
    )
    st.plotly_chart(fig)
    st.checkbox(
        label="What to do with the Top and Low Achievers?",
        key="what_to_do_with_the_top_and_low_achievers",
    )
    if st.session_state["what_to_do_with_the_top_and_low_achievers"]:
        with open(
            "markdown_for_streamlit/concerns_and_recommendations_for_low_achievers.md",
            "r",
            encoding="utf-8",
        ) as file:
            markdown_text = file.read()
            st.markdown(markdown_text)
        with open(
            "markdown_for_streamlit/recognition_and_encouragement_for_high_achievers.md",
            "r",
            encoding="utf-8",
        ) as file:
            markdown_text = file.read()
            st.markdown(markdown_text)
