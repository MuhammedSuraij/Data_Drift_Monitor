import pandas as pd
import os

def load_data(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".csv":
        return pd.read_csv(path)
    
    elif ext ==".json":
        return pd.read_json(path)

    elif ext in [".xls",".xlsx"]:
        return pd.read_excel(path)
    
    elif ext == ".parquet":
        return pd.read_parquet(path)
    
    else:
        raise ValueError(f"Unsupported file format: {ext}")