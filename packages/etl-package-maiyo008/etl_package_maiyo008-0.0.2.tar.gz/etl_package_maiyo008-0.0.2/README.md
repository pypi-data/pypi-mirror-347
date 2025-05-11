# etl_package_maiyo008

---

A simple yet extensible Python ETL (Extract, Transform, Load) pipeline that supports loading data from Parquet files, performing basic transformations, and writing to a PostgreSQL database. Designed to be easily reusable and ideal for automation tasks.

## 📦 Installation

To install the package from PyPI:

```
pip install etl-package-maiyo008
```

## 🧠 Features

- Extract data from Parquet files
- Transform data by:
  - Removing duplicates
  - Dropping rows with blank fields
- Load data into PostgreSQL with:
  - Chunked inserts for performance
  - Progress feedback via tqdm
- Load data into a csv file
  - Separator is a comma
  - Creates the csv within the same working directory

## 📁 Project Structure

```
etl_package_maiyo008/
├── etl.py
├── __init__.py
```

## 🚀 Quickstart Guide

1. Import the package

```
from etl_package_maiyo008.etl import Extract, Transform, Load
```

2. Extract data

Exctract from a parquet file

```
df = Extract.load_parquet("data/sample_data.parquet")
```

Extract from an API

```
df = Extract.load_api(url)
```

3. Transform data

```
df_clean = Transform.remove_duplicates(df)
df_clean = Transform.remove_blanks(df_clean)
```

4. Load Data to PostgreSQL

```
conn = Load.connect_postgres(
    database="mydb",
    host="localhost",
    user="myuser",
    password="mypassword"
)

Load.write_to_db(df_clean, table_name="cleaned_data", conn=conn)
```

5. Load Data to csv

```
Load.write_to_csv(df, filename)
```

## 📚 Method Reference

**Extract**
`Extract.load_parquet(path: str)`

- Loads a Parquet file into a pandas DataFrame.

**Transform**
`Transform.remove_duplicates(df: pd.DataFrame)`

- Removes duplicate rows from the DataFrame.

`Transform.remove_blanks(df: pd.DataFrame)`

- Removes rows with missing/blank values.

**Load**
`Load.connect_postgres(database, host, user, password, port=5432)`

- Creates a connection to a PostgreSQL database using SQLAlchemy.

`Load.write_to_db(df, table_name, conn, chunk_size=1000)`

- Writes the DataFrame to a PostgreSQL table in chunks, providing progress feedback.

## ⚠️ Requirements

- pandas
- psycopg2-binary
- SQLAlchemy
- tqdm
- pyarrow or fastparquet (for Parquet support)

Install requirements with:

```
pip install pandas psycopg2-binary SQLAlchemy tqdm pyarrow
```

## ✅ License

- MIT License
