import streamlit as st
import pandas as pd
import time

# Set page config
st.set_page_config(page_title="Register Tools", layout="centered")

# Session expiration (30 minutes)
SESSION_DURATION = 30 * 60  # 30 minutes in seconds
current_time = time.time()
if "session_start" not in st.session_state:
    st.session_state.session_start = current_time
elif current_time - st.session_state.session_start > SESSION_DURATION:
    st.session_state.clear()
    st.session_state.session_start = current_time
    st.warning("Session expired. Starting a new session.")

# Denominations
bills = {"100": 100.00, "50": 50.00, "20": 20.00, "10": 10.00, "5": 5.00, "1": 1.00}
coins = {"0.25": 0.25, "0.10": 0.10, "0.05": 0.05, "0.01": 0.01}
all_denoms = {**bills, **coins}


# --- Helper: Breakdown Bills for Amount ---
def get_limited_breakdown(amount, available_counts):
    breakdown = {}
    remaining = round(amount, 2)
    for label, value in all_denoms.items():
        max_available = available_counts[label]
        max_possible = int(remaining // value)
        to_use = min(max_available, max_possible)
        if to_use > 0:
            breakdown[f"${value:.2f}"] = to_use
            remaining = round(remaining - (to_use * value), 2)
    if remaining > 0.009:
        return {"error": f"⚠️ Unable to match exact amount. ${remaining:.2f} left."}
    return breakdown


# --- Sidebar Navigation ---
st.sidebar.title("🧰 Tools")
tool = st.sidebar.radio(
    "Select a feature",
    ["Register Closing Assistant", "Tip Split Calculator", "Yield Calculator"],
)

# --- Register Closing Assistant ---
if tool == "Register Closing Assistant":
    st.markdown(
        "<h1 style='text-align: center;'>🧾 Register Closing Assistant</h1>",
        unsafe_allow_html=True,
    )
    st.subheader("🪙 Enter Quantity of Each Denomination")
    user_counts = {}
    total_cash = 0.0

    st.markdown("#### 💵 Bills")
    cols_bills = st.columns(len(bills))
    for i, (label, value) in enumerate(bills.items()):
        with cols_bills[i]:
            count = st.number_input(
                f"${label}", min_value=0, step=1, key=f"bill_{label}"
            )
            user_counts[label] = count
            total_cash += count * value

    st.markdown("#### 🪙 Coins")
    cols_coins = st.columns(len(coins))
    for i, (label, value) in enumerate(coins.items()):
        with cols_coins[i]:
            count = st.number_input(
                f"${label}", min_value=0, step=1, key=f"coin_{label}"
            )
            user_counts[label] = count
            total_cash += count * value

    float_amount = 150.00
    deposit_amount = round(total_cash - float_amount, 2)

    st.markdown("---")
    st.markdown(
        f"<h3 style='text-align: center;'>🧮 Total Cash: <span style='color: white;'>${total_cash:.2f}</span></h3>",
        unsafe_allow_html=True,
    )

    if st.button("✅ Calculate Deposit Breakdown"):
        if deposit_amount < 0:
            st.error("❌ Total cash is less than the $150 float.")
        else:
            result = get_limited_breakdown(deposit_amount, user_counts)
            st.markdown(
                f"<h3 style='text-align: center;'>💰 Deposit Amount: <span style='color: green;'>${deposit_amount:.2f}</span></h3>",
                unsafe_allow_html=True,
            )
            if "error" in result:
                st.error(result["error"])
            else:
                st.markdown("### 🔍 Breakdown of Bills/Coins to Remove")
                for denom, count in result.items():
                    st.markdown(f"- **{denom}**: {count}")
                st.success(
                    "✅ Ready to remove the above bills and coins for the deposit."
                )

# --- Tip Split Calculator ---
elif tool == "Tip Split Calculator":
    st.markdown(
        "<h1 style='text-align: center;'>💵 Tip Split Calculator</h1>",
        unsafe_allow_html=True,
    )
    st.subheader("🪙 Enter Quantity of Each Denomination")
    user_counts = {}
    total_cash = 0.0

    st.markdown("#### 💵 Bills")
    cols_bills = st.columns(len(bills))
    for i, (label, value) in enumerate(bills.items()):
        with cols_bills[i]:
            count = st.number_input(
                f"${label}", min_value=0, step=1, key=f"tip_bill_{label}"
            )
            user_counts[label] = count
            total_cash += count * value

    st.markdown("#### 🪙 Coins")
    cols_coins = st.columns(len(coins))
    for i, (label, value) in enumerate(coins.items()):
        with cols_coins[i]:
            count = st.number_input(
                f"${label}", min_value=0, step=1, key=f"tip_coin_{label}"
            )
            user_counts[label] = count
            total_cash += count * value

    st.markdown("---")
    num_workers = st.number_input("👥 How many people worked?", min_value=1, step=1)
    st.markdown(
        f"<h3 style='text-align: center;'>💰 Total Tips: <span style='color: white;'>${total_cash:.2f}</span></h3>",
        unsafe_allow_html=True,
    )

    if st.button("🧮 Split Tips"):
        split_amount = round(total_cash / num_workers, 2)
        st.markdown(
            f"<h3 style='text-align: center;'>Each Person Gets: <span style='color: green;'>${split_amount:.2f}</span></h3>",
            unsafe_allow_html=True,
        )
        result = get_limited_breakdown(split_amount, user_counts)
        if "error" in result:
            st.error(result["error"])
        else:
            st.markdown("### 💸 Bills/Coins to Give Each Person")
            for denom, count in result.items():
                st.markdown(f"- **{denom}**: {count}")
            st.success(
                "✅ Use the above denominations to give each person their tip share."
            )

# --- Yield Calculator ---
elif tool == "Yield Calculator":
    st.markdown(
        "<h1 style='text-align: center;'>🗑️ Waste & Yield Calculator</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "Upload your product mix CSV, enter batches used, and report actual waste."
    )

    uploaded_file = st.file_uploader("📄 Upload Product Mix CSV", type="csv")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file, skiprows=5)
            pretzels_df = df[df["Item Group"] == "Sales Pretzels"]
            pretzels_df = pretzels_df[["Item Name", "Quantity"]]
            pretzels_df["Quantity"] = pd.to_numeric(
                pretzels_df["Quantity"], errors="coerce"
            )
            pretzels_df = pretzels_df.dropna().reset_index(drop=True)
            pretzels_df = pretzels_df[
                ~pretzels_df["Item Name"].str.lower().str.contains("total")
            ]

            st.markdown("### 📏 Sales Quantities (Read-Only)")
            for _, row in pretzels_df.iterrows():
                st.markdown(f"- {row['Item Name']}: {int(row['Quantity'])}")

            st.markdown("---")
            batches_used = st.number_input(
                "🥨 Total Batches Used Today", min_value=0, step=1
            )

            # Waste entry
            st.markdown("### ✏️ Enter Actual Waste Per Product")
            waste_products = {
                "Waste - Pretzels": 1,
                "Waste - Mini Dogs (10 ct)": 1.083,
                "Waste - Mini Dogs (14 ct)": 1.517,
                "Waste - Regular Nuggets": 1.66,
                "Waste - Small Nuggets": 1.25,
                "Waste - Pepperoni Nuggets - Regular": 1.66,
                "Waste - Pepperoni Nuggets - Small": 1.25,
                "Waste - Pretzel Dogs": 0.5,
            }
            waste_inputs = {
                label: st.number_input(label, min_value=0, step=1)
                for label in waste_products
            }

            adjusted_waste = sum(
                waste_inputs[p] * waste_products[p] for p in waste_inputs
            )

            # Exact names as they appear in uploaded CSV
            sales_multipliers = {
                "Pretzel-Cinnamon Sugar": 1,
                "Pretzel-Original": 1,
                "AA-Mini Pretzel Dogs-Regular 10 CT": 1.083,
                "Pretzel Dog-Original": 0.5,
                "Pretzel-Sweet Almond": 1,
                "Pretzel Nuggets-Original-Small": 1.25,
                "Pretzel Nuggets-Original-Regular": 1.66,
                "Pretzel Nuggets-Cinnamon Sugar-Small": 1.25,
                "Pretzel Nuggets-Cinnamon Sugar-Regular": 1.66,
                "Pretzel Nuggets-Pepperoni-Small": 1.25,
                "Pretzel Nuggets-Pepperoni-Regular": 1.66,
                "AA-Mini Pretzel Dogs-Large 14 CT": 1.517,
            }

            total_pretzels = 0

            # Waste breakdown
            for item, qty in waste_inputs.items():
                multiplier = waste_products[item]
                contribution = qty * multiplier
                total_pretzels += contribution

            # Sales breakdown
            for _, row in pretzels_df.iterrows():
                name = row["Item Name"]
                qty = row["Quantity"]
                if "Oreo" in name:
                    continue
                multiplier = sales_multipliers.get(name.strip(), None)
                if multiplier is not None:
                    contribution = qty * multiplier
                    total_pretzels += contribution

            yield_per_batch = (
                round(total_pretzels / batches_used, 2) if batches_used > 0 else 0
            )

            st.markdown("---")

            st.markdown(
                f"<h2>⚠️ Daily Pretzel Yield: {total_pretzels / batches_used:.2f}</h2>",
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
