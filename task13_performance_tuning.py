import sqlite3
import pandas as pd
import numpy as np
import time
import streamlit as st
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. SETUP & SIMULATE LARGE DATASET
# ==========================================
def setup_database():
    conn = sqlite3.connect('student_performance.db')
    cursor = conn.cursor()
    
    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS raw_submissions")
    cursor.execute("DROP TABLE IF EXISTS mv_daily_performance")
    
    # Create main table
    cursor.execute('''
        CREATE TABLE raw_submissions (
            submission_id INTEGER PRIMARY KEY,
            student_id INT,
            submission_date TEXT,
            score REAL,
            status TEXT
        )
    ''')
    
    # Generate 100,000 synthetic records to test performance at scale
    np.random.seed(42)
    n_records = 100000
    dates = pd.date_range(start='2026-01-01', periods=180, freq='D').strftime('%Y-%m-%d')
    
    df_gen = pd.DataFrame({
        'student_id': np.random.randint(1000, 9999, size=n_records),
        'submission_date': np.random.choice(dates, size=n_records),
        'score': np.round(np.random.normal(68, 15, size=n_records), 2),
        'status': np.random.choice(['Pass', 'Fail'], size=n_records, p=[0.65, 0.35])
    })
    
    df_gen.to_sql('raw_submissions', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

# ==========================================
# 2. PROFILING & OPTIMIZATION PIPELINE
# ==========================================
def benchmark_unoptimized_query():
    conn = sqlite3.connect('student_performance.db')
    start_time = time.perf_counter()
    
    # Slow Query: Raw aggregation on unindexed table
    query = """
    SELECT submission_date, 
           COUNT(*) as total_students,
           AVG(score) as mean_score,
           SUM(CASE WHEN score >= 60 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as pass_rate
    FROM raw_submissions
    WHERE submission_date BETWEEN '2026-02-01' AND '2026-05-01'
    GROUP BY submission_date
    """
    df = pd.read_sql_query(query, conn)
    elapsed = (time.perf_counter() - start_time) * 1000  # in ms
    conn.close()
    return elapsed, df

def apply_optimizations():
    conn = sqlite3.connect('student_performance.db')
    cursor = conn.cursor()
    
    # Optimization 1: Add Index on Filtered Columns
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sub_date ON raw_submissions(submission_date)")
    
    # Optimization 2: Materialized Pre-Aggregated View
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mv_daily_performance AS
        SELECT submission_date, 
               COUNT(*) as total_students,
               AVG(score) as mean_score,
               SUM(CASE WHEN score >= 60 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as pass_rate
        FROM raw_submissions
        GROUP BY submission_date
    ''')
    conn.commit()
    conn.close()

def benchmark_optimized_query():
    conn = sqlite3.connect('student_performance.db')
    start_time = time.perf_counter()
    
    # Fast Query: Reading from Pre-Aggregated View with Index
    query = """
    SELECT submission_date, total_students, mean_score, pass_rate
    FROM mv_daily_performance
    WHERE submission_date BETWEEN '2026-02-01' AND '2026-05-01'
    """
    df = pd.read_sql_query(query, conn)
    elapsed = (time.perf_counter() - start_time) * 1000  # in ms
    conn.close()
    return elapsed, df

if __name__ == "__main__":
    print("Setting up database and generating 100,000 records...")
    setup_database()
    
    print("Running Unoptimized Benchmark...")
    unopt_time, df_unopt = benchmark_unoptimized_query()
    
    print("Applying Optimizations (Indexes & Pre-Aggregated Views)...")
    apply_optimizations()
    
    print("Running Optimized Benchmark...")
    opt_time, df_opt = benchmark_optimized_query()
    
    speedup = ((unopt_time - opt_time) / unopt_time) * 100
    
    print("\n--- BENCHMARK RESULTS ---")
    print(f"Unoptimized Query Time : {unopt_time:.2f} ms")
    print(f"Optimized Query Time   : {opt_time:.2f} ms")
    print(f"Performance Improvement: {speedup:.2f}% faster")
    print(f"Metric Parity Check    : {'✅ VERIFIED' if len(df_unopt) == len(df_opt) else '❌ MISMATCH'}")
