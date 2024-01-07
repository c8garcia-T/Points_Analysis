import streamlit as st

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

from streamlit_module.individual_student_page import reasons_bar
from streamlit_module.individual_student_page import (
    section_cumulative_sum_of_points_time_series_line_single_student,
)

# Data Source
data_source = "data_public_ok/points_data_vicky_t.xlsx"
# Preliminary Dataset Builds
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

st.title("Explore the Available Data of a Student")
students_in_data = points_df.student.unique().tolist()

students_in_data_str = ", ".join(students_in_data)
st.write("Student Names:")
st.write(students_in_data_str)
st.number_input(
    "Pick a Student",
    step=1,
    min_value=1,
    max_value=len(students_in_data),
    help='Example: For Student named "Sheet1" enter 1',
    key="selected_student",
)
if st.session_state["selected_student"]:
    selected_student = "Sheet" + str(st.session_state["selected_student"])
    subset_df = points_df[(points_df.student == selected_student)]
    st.header(f"Selected Student: {selected_student}", divider="red")
    st.caption(f"Available Records ({subset_df.shape[0]})")
    st.dataframe(
        subset_df,
        hide_index=True,
    )
    fig = reasons_bar(points_df, selected_student)
    st.plotly_chart(fig)
    st.header("Point Analysis Over Time", divider="red")
    st.checkbox(
        label="View All Students", key="view_all_students_timeseries_net_points"
    )

    if not st.session_state["view_all_students_timeseries_net_points"]:
        section_cumulative_sum_of_points_time_series_line_single_student(
            points_time_series_df[points_time_series_df["student"] == selected_student]
        )
    else:
        section_cumulative_sum_of_points_time_series_line_single_student(
            points_time_series_df
        )
