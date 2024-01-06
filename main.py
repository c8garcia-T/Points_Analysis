from points_module.data_build import (
    build_aggregated_data_by_student_df,
    build_clean_df,
    build_aggregated_data_by_student_with_static_pos_to_neg_ratio_df,
    build_points_by_reasons_per_class_bar_data,
)
from point_visual_module.visuals import (
    points_by_teacher_per_class_bar,
    points_by_reasons_per_class_bar,
    plot_box_based_on_net_points,
    plot_box_based_on_positive_to_negative_point_ratio,
)
from points_queries_module.queries import get_head_and_tail_students_based_on_net_points
from IPython.display import display


raw_data_path = "points_raw_data_by_class/points_data_vicky_t.xlsx"
if __name__ == "__main__":
    # Datasets
    points_df = build_clean_df(raw_data_path)
    aggregated_data_by_student_df = build_aggregated_data_by_student_df(raw_data_path)
    aggregated_data_by_student_with_static_pos_to_neg_ratio_df = (
        build_aggregated_data_by_student_with_static_pos_to_neg_ratio_df(raw_data_path)
    )
    # Visuals
    points_by_teacher_per_class_bar(points_df)
    points_by_reasons_per_class_bar(points_df)
    # Tabular Visual
    display(
        get_head_and_tail_students_based_on_net_points(aggregated_data_by_student_df)
    )
    plot_box_based_on_net_points(aggregated_data_by_student_df)
    plot_box_based_on_positive_to_negative_point_ratio(
        aggregated_data_by_student_with_static_pos_to_neg_ratio_df
    )
    print("__main__")
