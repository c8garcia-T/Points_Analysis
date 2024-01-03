import pytest
import numpy as np
import os
import sys

sys.path.append(os.getcwd())

from points_module.data_wrangling import sheets_merge


def test_sheets_merge():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=files)
        result = sheets_merge(os.path.join(data_dir, files[rand_indx]))
    else:
        result = sheets_merge(os.path.join(data_dir, files[0]))
    assert result.shape[1] == 6
    assert result.columns.tolist() == (
        ["date", "reason", "value", "comments", "teacher"] + ["student"]
    )
