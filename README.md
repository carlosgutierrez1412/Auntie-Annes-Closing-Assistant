# Auntie Anne's Closing Assistant 🧾🥨

This project is a **Streamlit-based tool built to automate and streamline the end-of-day closing procedures** at Auntie Anne’s. As a shift leader, I experienced firsthand how manual and repetitive some of our daily closing tasks can be — from counting cash registers to splitting team tips and calculating dough yield based on sales and waste.

To make these processes faster, more accurate, and less stressful for team members, I built this tool.

---

## 🚀 Key Features

### ✅ Register Closing Assistant
Helps automate the process of preparing the deposit:
- Enter quantities of each bill and coin
- Automatically subtracts the $150 float
- Outputs the **optimal set of denominations to remove** for the deposit, using only what you have on hand

### 💸 Tip Split Calculator
Simplifies tip distribution among team members:
- Input the counted bills and coins
- Enter the number of team members
- The app splits the tips evenly and tells you exactly how to distribute the cash per person

### 📊 Waste & Yield Calculator
Replaces the manual Excel-based process:
- Upload the daily **Product Mix CSV** from Qubeyond
- Enter the number of batches used
- Input waste for key products (Mini Dogs, Nuggets, Pretzel Dogs)
- Calculates adjusted waste yield, sales yield, and total yield per batch — using the **same logic and multipliers from the store’s Excel sheet**

---

## 🧠 Why I Built This

The goal was simple: **make closing faster, easier, and more consistent**.

Before this tool, we relied on paper, calculators, and an Excel sheet that required manual data entry and formula tracking. This led to:
- Inconsistencies in how deposits and tips were handled
- Errors in waste/yield calculations
- Extra time spent on tasks that could be automated

This app reduces mental load at the end of a long shift, speeds up the closing process, and ensures better accuracy and consistency.

---

## 🛠 Tech Stack

- **Python**
- **Streamlit** for the web UI
- **Pandas** for CSV parsing and data manipulation
- **Session state** with expiration logic for temporary data persistence
- **Local file caching** (optional) to hold data across reloads
