# Engineering Velocity & GitHub PR Health Engine

An automated ETL ingestion pipeline and SQL analytics system that extracts live pull request data from GitHub, loads it into a normalized SQLite relational database, and calculates developer productivity benchmarks.

## Overview
Engineering teams need visibility into code review turnaround times and workflow bottlenecks. This tool automates the extraction of pull requests from open-source or private repositories, cleans and transforms timestamps to compute Time-to-Merge (TTM), and runs analytical queries on contributor velocity.

## Tech Stack
- Python 3
- requests, pandas, sqlite3, datetime
- SQLite Relational Database

## Key Features
- API Ingestion Client: Modular OOP client fetching pull request datasets via the GitHub REST API with pagination handling.
- Data Engineering Pipeline: Implements idempotent upsert operations (ON CONFLICT DO UPDATE) to prevent duplicate records on re-runs.
- SQL Analytics: Computes median merge velocity (hours), PR approval rates, and author contribution distribution.

## How to Run Locally

Clone or download the repository:
```bash
git clone [https://github.com/saiananduttez/github-pr-velocity.git](https://github.com/saiananduttez/github-pr-velocity.git)
cd github-pr-velocity

