import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducible marketplace event generation
np.random.seed(42)

# 1. Simulate Marketplace Event Stream (Tracking Plan Implementation)
n_events = 500
start_time = datetime(2026, 8, 1)

users = [f"usr_{i:03d}" for i in range(1, 51)]
listings = [f"lst_{i:03d}" for i in range(1, 21)]
event_types = ["search_executed", "listing_viewed", "match_requested", "transaction_completed"]
event_weights = [0.40, 0.35, 0.15, 0.10]

data = []
for _ in range(n_events):
    timestamp = start_time + timedelta(minutes=np.random.randint(0, 10080))
    user_id = np.random.choice(users)
    event = np.random.choice(event_types, p=event_weights)
    listing_id = np.random.choice(listings) if event != "search_executed" else None
    value = round(np.random.uniform(50, 500), 2) if event == "transaction_completed" else 0.0
    
    data.append({
        "timestamp": timestamp,
        "user_id": user_id,
        "event_type": event,
        "listing_id": listing_id,
        "transaction_value": value
    })

df_events = pd.DataFrame(data).sort_values("timestamp").reset_index(drop=True)

# 2. Liquidity & Marketplace Health Metric Computation
total_searches = len(df_events[df_events["event_type"] == "search_executed"])
total_views = len(df_events[df_events["event_type"] == "listing_viewed"])
total_matches = len(df_events[df_events["event_type"] == "match_requested"])
total_txns = len(df_events[df_events["event_type"] == "transaction_completed"])

search_to_view_rate = (total_views / total_searches) * 100 if total_searches > 0 else 0
match_fill_rate = (total_txns / total_matches) * 100 if total_matches > 0 else 0
gross_merchandise_value = df_events["transaction_value"].sum()

print("==================================================")
print("  PHASE 2 TASK 1: MARKETPLACE HEALTH METRICS")
print("==================================================")
print(f"Total Events Tracked:           {len(df_events)}")
print(f"Total Search Events:            {total_searches}")
print(f"Total Listing Views:            {total_views}")
print(f"Total Match Requests:           {total_matches}")
print(f"Completed Transactions:         {total_txns}")
print(f"Search-to-View Liquidity Rate:  {search_to_view_rate:.2f}%")
print(f"Match Fill Liquidity Rate:      {match_fill_rate:.2f}%")
print(f"Gross Merchandise Value (GMV):  ${gross_merchandise_value:,.2f}")
print("==================================================")

# Save processed event dataset
df_events.to_csv("marketplace_events.csv", index=False)
