import pandas as pd

success_dir = "Desktop/DETC/section1/successful/"
section2_dir = "Desktop/DETC/section2/"

df = pd.read_csv(success_dir+"successful.csv", header=0, nrows=50)
df.to_csv(section2_dir+"members.csv", index=False, encoding='utf-8')
