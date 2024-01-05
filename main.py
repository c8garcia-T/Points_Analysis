from points_module.data_wrangling import (
    sheets_merge,
    data_wrangling,
    exact_duplicates_handling,
)
from points_module.data_privacy import anonymize_student_n_teacher

raw_data_path = "points_raw_data_by_class/points_data_vicky_t.xlsx"
if __name__ == "__main__":
    points_df = sheets_merge(raw_data_path)
    points_df = anonymize_student_n_teacher(points_df)
    points_df = data_wrangling(points_df)
    points_df = exact_duplicates_handling(points_df)
    print("__main__")
