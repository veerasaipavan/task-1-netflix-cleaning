# task-1-netflix-cleaning
Data cleaning and preprocessing on Netflix dataset
# Task 1: Data Cleaning and Preprocessing (Netflix Dataset)

## 🎯 Objective
The goal of this task was to **clean and preprocess the raw Netflix Movies and TV Shows dataset** by handling missing values, duplicates, inconsistent formats, and ensuring the data is analysis-ready.  

This task is part of the **Data Analyst Internship assignment (Task 1)**.  

---

## 📂 Files in this Repositor
- **dataset/**
  - `netflix_titles.csv` → Original dataset from Kaggle  
  - `cleaned_netflix.csv` → Final cleaned dataset after preprocessing  

- **code/**
  - `task1_intern.py` → Python script containing the full cleaning pipeline  

- **screenshots/** *(optional)*  
  - Before/after cleaning checks (missing values, dataset shape, etc.)  

- **README.md**  
  - This documentation file explaining what was done  

---

## ⚙️ Data Cleaning Steps

### 1. Checked Dataset Shape & Missing Values
- Used `.shape` and `.isnull().sum()` to check number of rows/columns and missing values.  

### 2. Removed Duplicates
- Applied `.drop_duplicates()` to remove any duplicate rows.  

### 3. Handled Missing Values
- Dropped rows missing **critical identifiers** (`show_id`, `title`).  
- Filled missing categorical fields (`director`, `cast`, `country`, `rating`, `duration`) with `"unknown"`.  

### 4. Standardized Text Values
- Converted all text columns to **lowercase** and stripped extra spaces.  

### 5. Fixed Date Formats
- Converted the `date_added` column to **datetime** format.  
- Dropped rows where `date_added` could not be parsed.  

### 6. Cleaned `duration` Column  ✅ (Important)
- The original `duration` column contained mixed values like `"90 min"` (movies) and `"2 Seasons"` (TV shows).  
- To make it analysis-ready, the column was split into two parts:  
  - `duration_value` → numeric part (e.g., 90, 2)  
  - `duration_unit` → unit (`min`, `season`)  

**Why this step matters:**  
- Allows calculations like *average movie length in minutes* or *distribution of TV show seasons*.  
- Without splitting, numeric and text data are mixed, making analysis difficult.  

### 7. Renamed Columns
- Converted all column names to **lowercase with underscores** for consistency.  

### 8. Ensured Correct Data Types  ✅ (Important)
- Converted `release_year` and `duration_value` into **numeric types**.  
- Rows with invalid `release_year` were dropped.  

**Why this step matters:**  
- Ensures proper sorting and calculations.  
- Example: without conversion, `"100"` would be treated as a string and incorrectly sorted before `"20"`.  

### 9. Final Cleanup
- Dropped any remaining null values.  
- Verified no missing data remained.  
- Saved the cleaned dataset as `cleaned_netflix.csv`.  

---

## ✅ Final Results
- **Original dataset shape:** `8807 rows × 12 columns`  
- **Cleaned dataset shape:** `8794 rows × 14 columns`  
- **Added columns:** `duration_value`, `duration_unit`  
- **All missing values handled** and dataset ready for analysis.  

---

## 🚀 Tools Used
- Python 3.10  
- Pandas  
- PyCharm IDE  
### code 
'''

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

'''
