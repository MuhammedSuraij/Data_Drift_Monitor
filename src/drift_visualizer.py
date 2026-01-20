import matplotlib.pyplot as plt
import pandas as pd
import os


def plot_numeric_drift(train_col, new_col, feature_name, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(8,4))
    plt.hist(train_col, bins=30, alpha=0.6, label="Train", density=True)
    plt.hist(new_col, bins=30, alpha=0.6, label="New", density=True)

    plt.title(f"Numeric Drift: {feature_name}")
    plt.xlabel(feature_name)
    plt.ylabel("Density")
    plt.legend()

    file_path=f"{output_dir}/{feature_name}_numeric_drift.png"
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

    return file_path

def plot_categorical_drift(train_col, new_col, feature_name, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)

    train_dist= train_col.value_counts(normalize=True)
    new_dist= new_col.value_counts(normalize=True)

    df= pd.DataFrame({
        "Train": train_dist,
        "New": new_dist
    }).fillna(0)

    df.plot(kind="bar", figsize=(8,4))

    plt.title(f"Categorical Drift: {feature_name}")
    plt.ylabel("Probability")
    plt.xlabel(feature_name)
    plt.xticks(rotation=45)
    plt.tight_layout()

    file_path= f"{output_dir}/{feature_name}_categorical_drift.png"
    plt.savefig(file_path)
    plt.close()

    return file_path


