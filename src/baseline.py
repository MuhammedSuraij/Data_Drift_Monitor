import json

def compute_baseline(df):
    df=df.select_dtypes(include=["int64","float64"])
    baseline={
        "mean":df.mean().to_dict(),
        "std":df.std().to_dict(),
        "min":df.min().to_dict(),
        "max":df.max().to_dict()
    }
    return baseline

def save_baseline(baseline,path):
    with open(path,"w") as f:
        json.dump(baseline,f,indent=4)
