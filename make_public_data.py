import pandas as pd
import os
from random import shuffle


# Define a function to apply to the second column
def modify_column(column):
    teacher_names = column.unique()
    random_ids = [i for i, _ in enumerate(teacher_names)]
    shuffle(random_ids)
    mapping_ids = {
        teacher: f"ID_{id_rand}" for id_rand, teacher in zip(random_ids, teacher_names)
    }
    column = column.map(mapping_ids)

    return column


if "__name__" == "__name__":
    raw_data_path = "points_raw_data_by_class/Sammul_3m_points.xlsx"
    dfs = pd.read_excel(raw_data_path, sheet_name=None, header=None)
    # Modify the fifth column in each DataFrame
    column_to_modify = 4  # Assuming Python indexing (0-based), selects the fifth column
    for sheet_name, df in dfs.items():
        if len(df.columns) > column_to_modify:
            df.iloc[:, column_to_modify] = modify_column(df.iloc[:, column_to_modify])

    # Write the modified DataFrames back to a new Excel file
    output_excel_file_path = os.path.join(
        "data_public_ok", os.path.basename(raw_data_path)
    )
    with pd.ExcelWriter(output_excel_file_path, engine="xlsxwriter") as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=None)

    print(
        f"Excel file '{output_excel_file_path}' has been created with modified columns."
    )
