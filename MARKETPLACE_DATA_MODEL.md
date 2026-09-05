# Phase 2 Task 1 — Company Onboarding & Marketplace Data Model

## 1. Executive Summary
This document defines the marketplace liquidity framework and event tracking data architecture for the two-sided marketplace.

## 2. Liquidity Metrics Framework
* **Search-to-View Rate**: Percentage of search queries that result in a listing detail view (Measures supply discoverability).
* **Match Fill Rate**: Percentage of match/quote requests that result in a completed transaction (Measures supply-side responsiveness and liquidity).
* **Buyer Liquidity**: Proportion of active buyers making at least 1 transaction within 30 days.
* **Seller Liquidity**: Proportion of active listings receiving at least 1 match request within 7 days.

## 3. Extended Event Tracking Plan
| Event Name | Trigger Condition | Payload Properties | Business Purpose |
|---|---|---|---|
| `search_executed` | Buyer submits search query | `query_text`, `category`, `user_id` | Demand intent tracking |
| `listing_viewed` | Buyer opens listing page | `listing_id`, `category`, `user_id` | Engagement measurement |
| `match_requested` | Buyer clicks request/book | `listing_id`, `seller_id`, `user_id` | Match conversion funnel |
| `transaction_completed` | Payment process successful | `listing_id`, `transaction_value`, `user_id` | GMV & Revenue monetization |

## 4. Pipeline & Lineage Verification
* **Data Stream**: Real-time event ingestion simulation saved to `marketplace_events.csv`.
* **Verification**: Verified 500 atomic events and cross-checked match liquidity fill rates.
