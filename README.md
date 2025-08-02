# Global Organizational Data Analysis

This project performs computational analysis on large organizational datasets from around the world using **pure Python (no libraries)**. It reads a CSV file and returns two dictionaries:

1. Country-level statistics (t-test on profits, Minkowski distance between employee count and salary)
2. Category-level nested dictionary ranking organizations by employee size and profit change

---

## 📁 Project Structure

23905593.py # Main Python file (named using student ID)
Organisations.csv # Sample input file (CSV format) ( you can use other csv in repo)
README.md # Project overview and instructions


---

## ▶️ How to Run

You need Python 3 installed. Open a Python interpreter and call the `main()` function from your script.

```python
# Example usage in Python shell
from 23905593 import main

output1, output2 = main('Organisations.csv')

# Example checks
print(output1['brazil'])        # → [-0.5175, 10174.3314]
print(output2['biotechnology']) # → {'org_id1': [...], 'org_id2': [...], ...}

📌 Requirements & Constraints
No external modules (e.g., csv, math, statistics) used.
Do not use input() or print() (except for graceful error messages).
File must be named exactly as your student ID (e.g., 23905593.py).
Handles case-insensitive strings and skips rows with:
Negative/zero values
Missing required fields
Duplicate organization IDs

🔬 Computations Performed
1. Country-level Dictionary:

{
  'country1': [t_test_score, minkowski_distance],
  ...
}

2. Category-level Nested Dictionary:

{
  'category1': {
    'org_id1': [num_employees, profit_change %, rank],
    ...
  },
  ...
}

All floating point values are rounded to 4 decimal places, and all strings are converted to lowercase.