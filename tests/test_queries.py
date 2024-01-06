import numpy as np
import os
import sys

sys.path.append(os.getcwd())
from points_module.data_build import build_aggregated_data_by_student_df
from points_queries_module.queries import get_head_and_tail_students_based_on_net_points


def test_build_points_by_reasons_per_class_bar_data():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=files)
        df = build_aggregated_data_by_student_df(
            os.path.join(data_dir, files[rand_indx])
        )
    else:
        df = build_aggregated_data_by_student_df(os.path.join(data_dir, files[0]))
    result = get_head_and_tail_students_based_on_net_points(df)
    assert not result.empty
    assert result.shape[0] == 6
