import streamlit as st
import pandas as pd
import time
import random

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

# Sales multipliers for yield calculation
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
    "Pretzel Nuggets-Topped Oreo-Regular": 1.66
}

# Define waste products and their multipliers
waste_products = {
    "Waste - Pretzels": 1,
    "Waste - Mini Dogs (10 ct)": 1.083,
    "Waste - Mini Dogs (14 ct)": 1.517,
    "Waste - Regular Nuggets": 1.66,
    "Waste - Small Nuggets": 1.25,
    "Waste - Pepperoni Nuggets - Regular": 1.66,
    "Waste - Pepperoni Nuggets - Small": 1.25,
    "Waste - Pretzel Dogs": 0.5,
    "Waste - Pretzel Nuggets - Topped Oreo": 1.66
}

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
        "Upload your product mix CSV and enter batches used. The program will automatically calculate waste to achieve a yield between 42-45."
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
                "🥨 Total Batches Used Today", min_value=0, step=1, key="batches_used"
            )

            regenerate = st.button("🔄 Regenerate Yield & Waste")
            if (batches_used > 0 and uploaded_file) and (st.session_state.get('regenerate_clicked', True) or regenerate):
                st.session_state['regenerate_clicked'] = False if not regenerate else True
                # Calculate total sales pretzels
                total_sales_pretzels = 0
                for _, row in pretzels_df.iterrows():
                    name = row["Item Name"]
                    qty = row["Quantity"]
                    multiplier = sales_multipliers.get(name.strip(), 1)
                    total_sales_pretzels += qty * multiplier

                # Calculate target total pretzels (including waste)
                target_yield = round(43.5 + (random.random() * 3 - 1.5), 2)  # Random number between 42-45
                target_total_pretzels = target_yield * batches_used

                # Calculate required waste
                required_waste = target_total_pretzels - total_sales_pretzels

                # Priority weights for waste products (higher = more likely to get more waste)
                waste_priority_weights = {
                    "Waste - Regular Nuggets": 8,
                    "Waste - Pretzels": 7,
                    "Waste - Pepperoni Nuggets - Regular": 6,
                    "Waste - Mini Dogs (14 ct)": 5,
                    "Waste - Small Nuggets": 4,
                    "Waste - Pretzel Nuggets - Topped Oreo": 3,
                    "Waste - Pretzel Dogs": 2,
                    "Waste - Pepperoni Nuggets - Small": 1,
                    "Waste - Mini Dogs (10 ct)": 1,  # Not in your list, lowest priority
                }

                # Weighted random waste distribution
                waste_distribution = {product: 0 for product in waste_products}
                product_list = list(waste_products.keys())
                weights = [waste_priority_weights.get(p, 1) for p in product_list]
                total_weight = sum(weights)
                remaining_waste = int(round(required_waste))
                allocations = [0] * len(product_list)

                # Generate random proportions based on weights
                random_factors = [random.uniform(0.8, 1.2) * w for w in weights]
                factor_sum = sum(random_factors)
                proportions = [f / factor_sum for f in random_factors]

                # Allocate waste based on proportions
                for i, prop in enumerate(proportions):
                    allocations[i] = int(round(prop * remaining_waste))
                # Adjust to ensure sum matches required_waste
                diff = remaining_waste - sum(allocations)
                while diff != 0:
                    idx = random.choices(range(len(product_list)), weights=weights)[0]
                    if diff > 0:
                        allocations[idx] += 1
                        diff -= 1
                    elif diff < 0 and allocations[idx] > 0:
                        allocations[idx] -= 1
                        diff += 1
                for i, product in enumerate(product_list):
                    waste_distribution[product] = allocations[i]

                # Output order to match the user's screenshot
                output_order = [
                    "Waste - Pretzels",
                    "Waste - Regular Nuggets",
                    "Waste - Small Nuggets",
                    "Waste - Pretzel Dogs",
                    "Waste - Pepperoni Nuggets - Regular",
                    "Waste - Pepperoni Nuggets - Small",
                    "Waste - Pretzel Nuggets - Topped Oreo",
                    "Waste - Mini Dogs (14 ct)",
                    "Waste - Mini Dogs (10 ct)"
                ]

                st.markdown("---")
                st.markdown("### 📊 Calculated Waste Distribution")
                for product in output_order:
                    if product in waste_distribution:
                        st.markdown(f"- **{product}**: {int(waste_distribution[product])}")

                st.markdown("---")
                st.markdown(
                    f"<h2>🎯 Target Yield: {target_yield:.2f}</h2>",
                    unsafe_allow_html=True,
                )

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
