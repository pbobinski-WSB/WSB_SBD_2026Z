import os
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession

print("\n--- 1. INICJALIZACJA SPARK I ICEBERG ---")
spark = SparkSession.builder.appName("IcebergDemo").getOrCreate()
# W obrazie tabulario środowisko jest już połączone z katalogiem 'demo'

print("\n--- 2. TWORZENIE PLIKU CSV I PARQUET (Porównanie) ---")
# Generujemy 2 miliony wierszy w Pandas
df_pd = pd.DataFrame({
    'id': np.arange(2000000),
    'name': ['Jan'] * 2000000,
    'city': ['Warszawa'] * 2000000,
    'salary': np.random.randint(4000, 15000, size=2000000)
})

# Zapis do CSV
csv_path = '/home/iceberg/warehouse/test.csv'
df_pd.to_csv(csv_path, index=False)

# Zapis do Parquet
parquet_path = '/home/iceberg/warehouse/test.parquet'
df_pd.to_parquet(parquet_path, index=False)

# Porównanie rozmiaru (TUTAJ ROBISZ PAUZĘ NA WYKŁADZIE, studenci widzą różnicę!)
csv_size = os.path.getsize(csv_path) / (1024 * 1024)
parquet_size = os.path.getsize(parquet_path) / (1024 * 1024)
print(f"Rozmiar CSV: {csv_size:.2f} MB")
print(f"Rozmiar Parquet: {parquet_size:.2f} MB")


print("\n--- 3. TWORZENIE TABELI ICEBERG ---")
# Ładujemy do Sparka
df_spark = spark.read.parquet(parquet_path)

# Zapisujemy jako tabelę Iceberg
df_spark.writeTo("demo.default.employees").createOrReplace()

print("\nIle jest wierszy obecnie?")
spark.sql("SELECT COUNT(*) FROM demo.default.employees").show()

print("\n--- 4. TRANSAKCJA ACID: KASOWANIE DANYCH ---")
print("Kasujemy osoby zarabiające poniżej 10000 PLN...")
spark.sql("DELETE FROM demo.default.employees WHERE salary < 10000")

print("\nIle wierszy zostało po DELETE?")
spark.sql("SELECT COUNT(*) FROM demo.default.employees").show()


print("\n--- 5. MAGIA: TIME TRAVEL (PODRÓŻ W CZASIE) ---")
print("Pobieramy historię migawek (Snapshots)...")
snapshots = spark.sql("SELECT snapshot_id, committed_at FROM demo.default.employees.snapshots").collect()

# Pobieramy ID pierwszego snapshota (przed kasowaniem)
first_snapshot_id = snapshots[0]['snapshot_id']

print(f"\nUżywamy Time Travel, aby odpytać stan bazy z chwili Snapshotu: {first_snapshot_id}")
spark.sql(f"SELECT COUNT(*) FROM demo.default.employees VERSION AS OF {first_snapshot_id}").show()

print("\nDane odzyskane z ukrytych, nienadpisanych plików Parquet. Koniec dema!")