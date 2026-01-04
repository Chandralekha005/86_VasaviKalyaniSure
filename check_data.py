import pandas as pd

DATA_DIR = "data/sec_data/extracted_2019q1"

num = pd.read_csv(f"{DATA_DIR}/num.txt", sep="\t", low_memory=False)
pre = pd.read_csv(f"{DATA_DIR}/pre.txt", sep="\t", low_memory=False)
sub = pd.read_csv(f"{DATA_DIR}/sub.txt", sep="\t", low_memory=False)

print("num:", num.shape)
print("pre:", pre.shape)
print("sub:", sub.shape)

num.head()
