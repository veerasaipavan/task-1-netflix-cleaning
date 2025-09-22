
import pandas as pd


df = pd.read_csv(r"C:\Users\veera\OneDrive\Desktop\Documents\Desktop\elevate labs\netflix_titles.csv")

print("Original ", df.shape)
print("\nMissing values before cleaning:\n", df.isnull().sum())

df = df.drop_duplicates()



df = df.dropna(subset=["show_id", "title"])


categorical_cols = ["director", "cast", "country", "rating", "duration"]
for col in categorical_cols:
    df[col] = df[col].fillna("unknown")


text_cols = df.select_dtypes(include="object").columns
for col in text_cols:
    df[col] = df[col].astype(str).str.lower().str.strip()


df["date_added"] = pd.to_datetime(df["date_added"], format="%B %d, %Y", errors="coerce")

df = df.dropna(subset=["date_added"])


def split_duration(x):
    if (pd.isnull(x)) or (x == "unknown"):
        return pd.Series([None, None])
    parts = x.split()
    if len(parts) == 2 and parts[0].isdigit():
        return pd.Series([int(parts[0]), parts[1]])
    return pd.Series([None, None])

df[["duration_value", "duration_unit"]] = df["duration"].apply(split_duration)


df["duration_unit"] = df["duration_unit"].fillna("unknown")


df.columns = df.columns.str.lower().str.replace(" ", "_")


df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
df["duration_value"] = pd.to_numeric(df["duration_value"], errors="coerce")


df = df.dropna(subset=["release_year"])


df = df.dropna()

print("\nMissing values after cleaning:\n", df.isnull().sum())
print("\n shape:", df.shape)

df.to_csv("cleaned_netflix.csv", index=False)

