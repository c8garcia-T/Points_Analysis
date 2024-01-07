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
    st.checkbox(label="Key Insights", key="key_insights_point_analysis_over_time")
    if st.session_state["key_insights_point_analysis_over_time"]:
        with open(
            "markdown_for_streamlit/key_insights_point_analysis_over_time.md",
            "r",
            encoding="utf-8",
        ) as file:
            markdown_text = file.read()
            st.markdown(markdown_text)


def top_and_bottom_student_section(
    aggregated_data_by_student_df_in,
    head_and_tail_students_based_on_net_points_df_in,
    aggregated_data_by_student_with_static_pos_to_neg_ratio_df_in,
    head_and_tail_students_based_on_positive_to_negative_point_ratio_df_in,
):
    st.header("Discovering Top and Bottom Performers", divider="red")
    st.checkbox(
        label="Key Statistics (Class Mean, Std)",
        key="key_statistics_for_highs_and_lows",
    )
    if st.session_state["key_statistics_for_highs_and_lows"]:
        date_info_min = aggregated_data_by_student_df_in.loc[
            head_and_tail_students_based_on_net_points_df_in["student"]
        ][("Records", "start")].min()
        date_info_max = aggregated_data_by_student_df_in.loc[
            head_and_tail_students_based_on_net_points_df_in["student"]
        ][("Records", "end")].max()
        class_mean = aggregated_data_by_student_df_in[("Points", "sum")].mean()
        class_median = aggregated_data_by_student_df_in[("Points", "sum")].median()
        class_std = aggregated_data_by_student_df_in[("Points", "sum")].std()
        st.caption("About Net Points")
        st.write(f"Data Range: {date_info_min.date()} to {date_info_max.date()}")
        st.write(
            f"Mean {round(class_mean,2)} Std {round(class_std,2)} Median {round(class_median,2)}"
        )
        st.caption("About Positive-to-Negative Ratio")
        date_info_min = (
            aggregated_data_by_student_with_static_pos_to_neg_ratio_df_in.loc[
                head_and_tail_students_based_on_positive_to_negative_point_ratio_df_in[
                    "student"
                ]
            ][("Records", "start")].min()
        )
        date_info_max = (
            aggregated_data_by_student_with_static_pos_to_neg_ratio_df_in.loc[
                head_and_tail_students_based_on_positive_to_negative_point_ratio_df_in[
                    "student"
                ]
            ][("Records", "end")].max()
        )
        class_mean = aggregated_data_by_student_with_static_pos_to_neg_ratio_df_in[
            ("Positive to Negative Points Ratio", "Static Estimate")
        ].mean()
        class_median = aggregated_data_by_student_with_static_pos_to_neg_ratio_df_in[
            ("Positive to Negative Points Ratio", "Static Estimate")
        ].median()
        class_std = aggregated_data_by_student_with_static_pos_to_neg_ratio_df_in[
            ("Positive to Negative Points Ratio", "Static Estimate")
        ].std()
        st.write(f"Data Range: {date_info_min.date()} to {date_info_max.date()}")
        st.write(
            f"Mean {round(class_mean,2)} Std {round(class_std,2)} Median {round(class_median,2)}"
        )
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


def reasons_and_teacher_plots_section(points_df_in):
    st.header("Behind the Points", divider="red")
    fig = points_by_teacher_per_class_bar(points_df_in)
    st.plotly_chart(fig)

    st.checkbox(
        label="Show Full Distribution For Point Assignment Reason",
        key="show_full_distribution_for_point_assignment_reason",
    )
    if not st.session_state["show_full_distribution_for_point_assignment_reason"]:
        fig = points_by_reasons_per_class_bar(points_df_in, True)
    elif st.session_state["show_full_distribution_for_point_assignment_reason"]:
        fig = points_by_reasons_per_class_bar(points_df_in)
    st.plotly_chart(fig)
