from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the driver (make sure chromedriver is in your PATH)
driver = webdriver.Chrome()
driver.maximize_window()

max_retries = 3
for attempt in range(max_retries):
    try:
        driver.get("https://clcintranet.omsllc.net/Login.aspx?ReturnUrl=%2fDefault.aspx")
        break
    except WebDriverException:
        print(f"Connection error, retrying ({attempt+1}/{max_retries})...")
        time.sleep(5)
else:
    print("Failed to connect after several attempts.")
    driver.quit()
    exit()

# Wait for the page to load
time.sleep(2)

# Enter username
username_field = driver.find_element(By.ID, "ContentPlaceHolder1_Login1_UserName")
username_field.send_keys("Fl187")

# Enter password
password_field = driver.find_element(By.ID, "ContentPlaceHolder1_Login1_Password")
password_field.send_keys("fl187")

# Click the login button
login_button = driver.find_element(By.ID, "ContentPlaceHolder1_Login1_LoginButton")
login_button.click()

# Wait for navigation (adjust as needed)
time.sleep(3)

# Wait for the page to load after login
time.sleep(3)

# Click the "Daily Cash Sheets" link
cash_sheet_link = driver.find_element(By.XPATH, "//a[contains(@href, 'CashSheet.aspx')]")
cash_sheet_link.click()

# Wait for the cash sheet page to load
time.sleep(5)

# Click the "Load Store" button
load_store_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_cmdLoadStore")
load_store_button.click()

# Wait for the next page to load
time.sleep(5)

# Load your JSON data (update the path as needed)
with open("closing_and_yield_data.json", "r") as f:
    data = json.load(f)

# After clicking Load Store and before clicking Cash For Deposit
wait = WebDriverWait(driver, 10)  # wait up to 20 seconds

# Wait for the Net Sales field to be present
net_sales_field = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder2_txtNetSales")))
net_sales = data["yield_calculator"].get("net_sales", 0)
net_sales_field.clear()
net_sales_field.send_keys(str(net_sales))
time.sleep(2)

save_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_cmdSave")
save_button.click()

time.sleep(5)

# Click the "House Bank Verification" tab
house_bank_verification_tab = driver.find_element(By.XPATH, "//span[contains(text(), 'House Bank Verification')]")
house_bank_verification_tab.click()
time.sleep(5)

# Fill Till One Night
till_one_night = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_numTill1Night")
till_one_night.clear()
till_one_night.send_keys('150')
time.sleep(1)

# Fill Till Two Night
till_two_night = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_numTill2Night")
till_two_night.clear()
till_two_night.send_keys('150')
time.sleep(1)

# Fill Change Bank Night
change_night = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_numChangeNight")
change_night.clear()
change_night.send_keys('500')
time.sleep(1)

# Copy the value from Deposit Morning and paste into Deposit Night
deposit_morning_field = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_txtDepositMorning")
deposit_morning_value = deposit_morning_field.get_attribute("value")

deposit_night_field = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_txtDepositNight")
deposit_night_field.clear()
deposit_night_field.send_keys(deposit_morning_value)

time.sleep(3)

save_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_cmdSave")
save_button.click()

time.sleep(5)

# Click the "Cash For Deposit" tab
cash_for_deposit_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Cash For Deposit')]")))
cash_for_deposit_tab.click()

# Wait for the tab content to load
time.sleep(5)

# Map JSON keys to form field IDs
denom_to_field = {
    "coins": "ctl00_ContentPlaceHolder2_numNightShiftCoin",
    "$1.00": "ctl00_ContentPlaceHolder2_numNightShiftOnes",
    "$5.00": "ctl00_ContentPlaceHolder2_numNightShiftFives",
    "$10.00": "ctl00_ContentPlaceHolder2_numNightShiftTens",
    "$20.00": "ctl00_ContentPlaceHolder2_numNightShiftTwenties",
    "$50.00": "ctl00_ContentPlaceHolder2_numNightShiftFifties",
    "$100.00": "ctl00_ContentPlaceHolder2_numNightShiftHundreds"
}

# Get the deposit breakdown from the JSON
deposit_breakdown = data["register_closing"]["deposit_breakdown"]

# Fill the form fields
for denom, field_id in denom_to_field.items():
    value = deposit_breakdown.get(denom, 0)
    input_field = driver.find_element(By.ID, field_id)
    input_field.clear()
    input_field.send_keys(str(value))

# Get the deposit amount from the JSON
deposit_amount = data["register_closing"]["deposit_amount"]

# Input the deposit amount into the 'Cash Payments Received (from tape)' box
# Field ID: ctl00_ContentPlaceHolder2_numTotalDepositTAPE
tape_field = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_numTotalDepositTAPE")
tape_field.clear()
tape_field.send_keys(str(deposit_amount))

# Click the Save button
save_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_cmdSave")
save_button.click()

time.sleep(5)

# Click the "Waste" tab
waste_tab = driver.find_element(By.XPATH, "//span[contains(text(), 'Waste')]")
waste_tab.click()
time.sleep(3)

# Input the batches used value
batches_used = data["yield_calculator"]["batches_used"]
batches_field = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_numBatches")
batches_field.clear()
batches_field.send_keys(str(batches_used))

# Get the waste data from the JSON
waste_data = data["yield_calculator"]["waste_distribution"]

# List of waste input field IDs in the order they appear on the page
waste_field_ids = [
    "ctl00_ContentPlaceHolder2_numWasteQty1",  # Pretzel-Original
    "ctl00_ContentPlaceHolder2_numWasteQty2",  # Pretzel Nuggets-Original-Regular
    "ctl00_ContentPlaceHolder2_numWasteQty3",  # Pretzel Nuggets-Original-Small
    "ctl00_ContentPlaceHolder2_numWasteQty4",  # Pretzel Dog-Original
    "ctl00_ContentPlaceHolder2_numWasteQty5",  # Pretzel Nuggets-Pepperoni-Regular
    "ctl00_ContentPlaceHolder2_numWasteQty6",  # Pretzel Nuggets-Pepperoni-Small
    "ctl00_ContentPlaceHolder2_numWasteQty7",  # Pretzel Nuggets-Topped Oreo-Regular
    "ctl00_ContentPlaceHolder2_numWasteQty8",  # AA-Mini Pretzel Dogs-Large 14 CT
    "ctl00_ContentPlaceHolder2_numWasteQty9",  # AA-Mini Pretzel Dogs-Regular 10 CT
]

# List of waste product keys in the order they appear in your JSON and on the page
waste_keys = [
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

# Fill the waste fields
for field_id, key in zip(waste_field_ids, waste_keys):
    value = waste_data.get(key, 0)
    input_field = driver.find_element(By.ID, field_id)
    input_field.clear()
    input_field.send_keys(str(value))

# Click the Save button on the Waste page
waste_save_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_cmdSave")
waste_save_button.click()
time.sleep(5)

# At this point, you are logged in and can proceed to automate the next steps
# (e.g., navigate to the cash sheet page and fill in the form)

driver.quit()