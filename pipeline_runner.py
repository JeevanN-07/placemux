import argparse
import logging
import os
import sys
import pandas as pd
import numpy as np

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def extract_data(records: int) -> pd.DataFrame:
    """Stage 1: Extract raw data with dynamic parameterization."""
    logging.info(f"STAGE 1: Extracting {records} raw transaction records...")
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=records, freq="h")
    amounts = np.round(np.random.exponential(scale=100, size=records) + 5, 2)
    customers = [f"CUST_{np.random.randint(100, 150):03d}" for _ in range(records)]
    
    df = pd.DataFrame({
        "transaction_id": range(1000, 1000 + records),
        "timestamp": dates,
        "customer_id": customers,
        "amount": amounts
    })
    logging.info(f"STAGE 1 COMPLETE: Extracted {len(df)} rows.")
    return df

def validate_data(df: pd.DataFrame) -> None:
    """Stage 2: Data Quality Checks between stages."""
    logging.info("STAGE 2: Running Data Quality Assertion Checks...")
    assert not df.empty, "Data Quality Error: DataFrame is empty!"
    assert df["amount"].min() > 0, "Data Quality Error: Negative or zero amounts detected!"
    assert df["customer_id"].isnull().sum() == 0, "Data Quality Error: Null customer IDs found!"
    logging.info("STAGE 2 COMPLETE: All Data Quality checks passed successfully.")

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Stage 3: Transform & Aggregate."""
    logging.info("STAGE 3: Transforming data and generating Customer Aggregates...")
    aggregated = df.groupby("customer_id").agg(
        total_spend=("amount", "sum"),
        transaction_count=("amount", "count"),
        avg_basket_size=("amount", "mean"),
        last_active=("timestamp", "max")
    ).reset_index()
    logging.info(f"STAGE 3 COMPLETE: Transformed into {len(aggregated)} customer profile records.")
    return aggregated

def load_data(df: pd.DataFrame, output_path: str) -> None:
    """Stage 4: Idempotent Load & Versioned Output."""
    logging.info(f"STAGE 4: Saving output idempotently to {output_path}...")
    if os.path.exists(output_path):
        os.remove(output_path)  # Enforce idempotency by clearing existing file
    df.to_csv(output_path, index=False)
    logging.info(f"STAGE 4 COMPLETE: Output written cleanly to {output_path}.")

def main():
    parser = argparse.ArgumentParser(description="Task 19 Analytical Data Pipeline Runner")
    parser.add_argument("--records", type=int, default=500, help="Number of records to extract")
    parser.add_argument("--output", type=str, default="pipeline_output.csv", help="Output file path")
    args = parser.parse_args()

    logging.info("=== PIPELINE EXECUTION STARTED ===")
    raw_df = extract_data(args.records)
    validate_data(raw_df)
    transformed_df = transform_data(raw_df)
    load_data(transformed_df, args.output)
    logging.info("=== PIPELINE EXECUTION COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
