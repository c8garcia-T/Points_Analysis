import streamlit as st
from point_visual_module.visuals import (
    points_by_teacher_per_class_bar,
    points_by_reasons_per_class_bar,
    plot_box_based_on_net_points,
    plot_box_based_on_positive_to_negative_point_ratio,
)
from points_module.data_build import (
    build_clean_df,
    build_aggregated_data_by_student_df,
    build_aggregated_data_by_student_with_static_pos_to_neg_ratio_df,
    build_points_time_series_df,
)
from points_queries_module.queries import (
    get_head_and_tail_students_based_on_net_points,
    get_head_and_tail_students_based_on_positive_to_negative_point_ratio,
)
from streamlit_module.sections import (
    section_cumulative_sum_of_points_time_series_line,
    top_and_bottom_student_section,
)

# Data Source
data_source = "points_raw_data_by_class/points_data_vicky_t.xlsx"
# Preliminary Builds
points_df = build_clean_df(data_source)
aggregated_data_by_student_df = build_aggregated_data_by_student_df(data_source)
aggregated_data_by_student_with_static_pos_to_neg_ratio_df = (
    build_aggregated_data_by_student_with_static_pos_to_neg_ratio_df(data_source)
)
head_and_tail_students_based_on_net_points_df = (
    get_head_and_tail_students_based_on_net_points(aggregated_data_by_student_df)
)
head_and_tail_students_based_on_positive_to_negative_point_ratio_df = (
    get_head_and_tail_students_based_on_positive_to_negative_point_ratio(
        aggregated_data_by_student_with_static_pos_to_neg_ratio_df
    )
)
points_time_series_df = build_points_time_series_df(points_df)


#### Section 1
st.title("The Dynamics of Points: Unraveling Patterns in Student Scores")
section_cumulative_sum_of_points_time_series_line(points_time_series_df)
top_and_bottom_student_section(
    aggregated_data_by_student_df,
    head_and_tail_students_based_on_net_points_df,
    aggregated_data_by_student_with_static_pos_to_neg_ratio_df,
    head_and_tail_students_based_on_positive_to_negative_point_ratio_df,
)

fig = points_by_teacher_per_class_bar(points_df)
st.plotly_chart(fig)

st.checkbox(
    label="Show Full Distribution For Point Assignment Reason",
    key="show_full_distribution_for_point_assignment_reason",
)
if not st.session_state["show_full_distribution_for_point_assignment_reason"]:
    fig = points_by_reasons_per_class_bar(points_df, True)
elif st.session_state["show_full_distribution_for_point_assignment_reason"]:
    fig = points_by_reasons_per_class_bar(points_df)
st.plotly_chart(fig)
#### Section 2
st.header("Discovering Top and Bottom Performers", divider="red")
fig = plot_box_based_on_net_points(aggregated_data_by_student_df)
st.plotly_chart(fig)

fig = plot_box_based_on_positive_to_negative_point_ratio(
    aggregated_data_by_student_with_static_pos_to_neg_ratio_df
)
st.plotly_chart(fig)

st.checkbox(
    label="Positive-to-Negative Point Ratio Definition",
    key="show_positive_to_neg_definition",
)
if st.session_state["show_positive_to_neg_definition"]:
    with open(
        "markdown_for_streamlit/show_positive_to_neg_definition.md",
        "r",
        encoding="utf-8",
    ) as file:
        markdown_text = file.read()
        st.markdown(markdown_text)
