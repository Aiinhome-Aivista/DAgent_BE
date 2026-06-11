import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine

def process_csv_job(file_paths, allocated_db_name, db_host, db_user, db_pass, db_port):
    safe_user = quote_plus(db_user)
    safe_pass = quote_plus(db_pass)

    base_url = f"mysql+pymysql://{safe_user}:{safe_pass}@{db_host}:{db_port}"

    target_engine = create_engine(
        f"{base_url}/{allocated_db_name}",
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600
    )

    tables_created = []

    for path in file_paths:
        print(f"\n🚀 Starting processing for file: {path}")

        # Count total rows (for progress calculation)
        print("🔎 Counting rows...")
        with open(path, encoding="latin1") as f:
            total_rows = sum(1 for _ in f)

        print(f"📊 Total rows detected: {total_rows}")

        raw_name = path.split("/")[-1].rsplit('.', 1)[0]
        table_name = "".join([c if c.isalnum() else "_" for c in raw_name]).lower()[:60]

        first_chunk = True
        chunk_size = 300000
        processed_rows = 0

        for chunk in pd.read_csv(
            path,
            chunksize=chunk_size,
            dtype=str,
            encoding="latin1",
            engine="python",
            on_bad_lines="skip",
            memory_map=True
        ):

            processed_rows += len(chunk)
            percent = (processed_rows / total_rows) * 100

            print(
                f"[PROGRESS] {table_name} → "
                f"{percent:.2f}% "
                f"({processed_rows}/{total_rows} rows)"
            )

            chunk.columns = [
                "".join([c if c.isalnum() else "_" for c in col]).lower()
                for col in chunk.columns
            ]

            if first_chunk:
                chunk.to_sql(
                    table_name,
                    target_engine,
                    if_exists='replace',
                    index=False,
                    method='multi',
                    chunksize=1000
                )
                first_chunk = False
            else:
                chunk.to_sql(
                    table_name,
                    target_engine,
                    if_exists='append',
                    index=False,
                    method='multi',
                    chunksize=1000
                )

        tables_created.append(table_name)

        print(f"✅ Finished loading table: {table_name}")

    print("\n🎉 All files processed successfully!")

    return tables_created
