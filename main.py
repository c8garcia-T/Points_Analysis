from points_module.data_wrangling import load_data

raw_data_path = "points_raw_data_by_class/points_data_vicky_t.xlsx"
if __name__ == "__main__":
    load_data(raw_data_path)
    print("__main__")
