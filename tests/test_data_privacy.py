import pytest
import numpy as np
import os
import sys

sys.path.append(os.getcwd())

from points_module.data_wrangling import sheets_merge
from points_module.data_privacy import anonymize_student_n_teacher


def test_anonymize_student_n_teacher():
    data_dir = "points_raw_data_by_class"
    files = os.listdir(data_dir)
    if len(files) > 1:
        rand_indx = np.random.randint(low=0, high=files)
        result = sheets_merge(os.path.join(data_dir, files[rand_indx]))
    else:
        result = sheets_merge(os.path.join(data_dir, files[0]))
    teacher_names = set(result.teacher.unique())
    result = anonymize_student_n_teacher(result)
    teacher_anonymized = set(result.teacher.unique())
    assert len(teacher_names) == len(teacher_anonymized)
    assert not teacher_names.intersection(teacher_anonymized)
