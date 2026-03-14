import pandas as pd
df = pd.read_csv("place you file path here") ## if not working then use 

# df = pd.read_csv(r"place you file path here")

for c in df.columns:
    print(repr(c))

df.columns = df.columns.str.strip()

df = df.rename(columns={
    "Symbol": "Ticker",
    "Longname": "InstrumentName",
    "Sector": "InstrumentType",
    "Currentprice": "Price"
})

print(df.columns)

print(df.head())
print(df.columns)
print("Shape:", df.shape)
print("Total rows:", len(df))

df["Currency"] = "USD"

import random
import string

def fake_isin():
    return "US" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

df["ISIN"] = [fake_isin() for _ in range(len(df))]

instrument_df = df[[
    "ISIN",
    "Ticker",
    "InstrumentName",
    "InstrumentType",
    "Currency",
    "Exchange",
    "Price"
]]

print(instrument_df.head())
print("Instrument shape:", instrument_df.shape)

vendorA = instrument_df.copy()
vendorA["Vendor"] = "VendorA"

vendorB = instrument_df.copy()
vendorB["Vendor"] = "VendorB"
vendorB["Price"] = vendorB["Price"] * 1.01

vendorC = instrument_df.copy()
vendorC["Vendor"] = "VendorC"

vendorC.loc[5, "ISIN"] = None
vendorC.loc[10, "Price"] = -5

import os
print("Current working directory:", os.getcwd())

vendorA.to_csv(r"C:\Users\KODAVATH SHASHIKANTH\OneDrive\Desktop\Python\FileI\PROJECT\Data\vendor_a.csv", index=False)
vendorB.to_csv(r"C:\Users\KODAVATH SHASHIKANTH\OneDrive\Desktop\Python\FileI\PROJECT\Data\vendor_b.csv", index=False)
vendorC.to_csv(r"C:\Users\KODAVATH SHASHIKANTH\OneDrive\Desktop\Python\FileI\PROJECT\Data\vendor_c.csv", index=False)

print("Vendor files saved")

all_vendors = pd.concat([vendorA, vendorB, vendorC], ignore_index=True)

print("All vendor rows:", all_vendors.shape)

all_vendors["valid_isin"] = all_vendors["ISIN"].notna()
all_vendors["valid_price"] = all_vendors["Price"] > 0
all_vendors["valid_currency"] = all_vendors["Currency"].isin(["USD"])

exceptions = all_vendors[
    ~(all_vendors["valid_isin"] &
      all_vendors["valid_price"] &
      all_vendors["valid_currency"])
]

print("Exceptions:", exceptions.shape)

exceptions.to_csv(r"C:\Users\KODAVATH SHASHIKANTH\OneDrive\Desktop\Python\FileI\PROJECT\Data\exceptions.csv", index=False)

conflicts = all_vendors.groupby("ISIN").agg({
    "Price": "nunique",
    "Vendor": "count"
}).reset_index()

conflicts = conflicts[conflicts["Price"] > 1]

print("Conflicts found:", conflicts.shape)

conflicts.to_csv(r"C:\Users\KODAVATH SHASHIKANTH\OneDrive\Desktop\Python\FileI\PROJECT\Data\conflicts.csv", index=False)

priority_map = {
    "VendorA": 1,
    "VendorB": 2,
    "VendorC": 3
}

all_vendors["priority"] = all_vendors["Vendor"].map(priority_map)

sorted_data = all_vendors.sort_values(["ISIN", "priority"])

golden_copy = sorted_data.drop_duplicates(subset=["ISIN"], keep="first")

print("Golden copy shape:", golden_copy.shape)
print(golden_copy.head())

golden_copy.to_csv(
r"C:\Users\KODAVATH SHASHIKANTH\OneDrive\Desktop\Python\FileI\PROJECT\Data\golden_copy.csv",
index=False
)

total_records = len(all_vendors)
total_instruments = golden_copy["ISIN"].nunique()
exception_count = len(exceptions)
conflict_count = len(conflicts)

print("Total records:", total_records)
print("Unique instruments:", total_instruments)
print("Exceptions:", exception_count)
print("Conflicts:", conflict_count)

vendor_stats = all_vendors.groupby("Vendor").size().reset_index(name="records")

print(vendor_stats)

metrics = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Unique Instruments",
        "Exceptions",
        "Conflicts"
    ],
    "Value": [
        total_records,
        total_instruments,
        exception_count,
        conflict_count
    ]
})

metrics.to_csv(
r"C:\Users\KODAVATH SHASHIKANTH\OneDrive\Desktop\Python\FileI\PROJECT\Data\metrics.csv",
index=False
)
