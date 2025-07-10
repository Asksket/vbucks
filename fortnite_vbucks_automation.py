import time
import json
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# URLs
XBOX_APEX_URL = "https://www.xbox.com/en-ZA/games/store/apex-legends-1000-apex-coins/9n5qmznw4bt1"
XBOX_CART_URL = "https://www.xbox.com/en-ZA/cart"
XBOX_FORTNITE_URL = "https://www.xbox.com/en-ZA/play/games/fortnite/9nxmbq9p6kns"
EPIC_AUTH_LINK = "https://epicgames.com/id/api/redirect"
XBOX_REFUND_URL = "https://support.xbox.com/en-ZA/help/subscriptions-billing/buy-games-apps/refund-orders"

# Profile paths (adjust for Linux if needed)
EDGE_PROFILE_PATH = "/workspace/.config/microsoft-edge/Profile 1"  # Linux path
CHROME_PROFILE_PATH = "/workspace/.config/google-chrome/Profile 1"  # Linux path

# Windows paths (uncomment if running on Windows)
# EDGE_PROFILE_PATH = r"C:\Users\asksk\AppData\Local\Microsoft\Edge\User Data\Profile 1"
# CHROME_PROFILE_PATH = r"C:\Users\asksk\AppData\Local\Google\Chrome\User Data\Profile 1"

def setup_browser():
    """Setup browser with existing profile"""
    try:
        # Try Edge first
        if os.path.exists(EDGE_PROFILE_PATH):
            print("[+] Using Edge browser with existing profile...")
            edge_options = EdgeOptions()
            edge_options.add_argument(f"--user-data-dir={os.path.dirname(EDGE_PROFILE_PATH)}")
            edge_options.add_argument(f"--profile-directory={os.path.basename(EDGE_PROFILE_PATH)}")
            edge_options.add_argument("--no-first-run")
            edge_options.add_argument("--no-default-browser-check")
            edge_options.add_experimental_option("detach", True)
            return webdriver.Edge(options=edge_options)
        
        # Fallback to Chrome
        elif os.path.exists(CHROME_PROFILE_PATH):
            print("[+] Using Chrome browser with existing profile...")
            chrome_options = ChromeOptions()
            chrome_options.add_argument(f"--user-data-dir={os.path.dirname(CHROME_PROFILE_PATH)}")
            chrome_options.add_argument(f"--profile-directory={os.path.basename(CHROME_PROFILE_PATH)}")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_experimental_option("detach", True)
            return webdriver.Chrome(options=chrome_options)
        
        else:
            print("[+] Using default browser...")
            return webdriver.Edge()
            
    except Exception as e:
        print(f"[!] Error setting up browser: {e}")
        print("[+] Trying with default browser...")
        return webdriver.Edge()

def wait_for_element(driver, by, value, timeout=30):
    """Wait for element to be present and clickable"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        return element
    except TimeoutException:
        print(f"[!] Timeout waiting for element: {value}")
        return None

def add_to_cart_and_buy(driver):
    """Add Apex token to cart and complete purchase"""
    print("[+] Opening Apex product page...")
    driver.get(XBOX_APEX_URL)
    time.sleep(5)
    
    # Try different possible selectors for "Buy" or "Add to cart" button
    buy_selectors = [
        "button[data-testid='BuyButton']",
        "button[aria-label*='Buy']",
        "button[aria-label*='Purchase']",
        ".buy-button",
        ".purchase-button",
        "button:contains('Buy')",
        "button:contains('Purchase')",
        "[data-testid*='buy']",
        "[data-testid*='purchase']"
    ]
    
    print("[+] Looking for Buy/Add to cart button...")
    buy_button = None
    for selector in buy_selectors:
        try:
            buy_button = driver.find_element(By.CSS_SELECTOR, selector)
            if buy_button and buy_button.is_displayed():
                print(f"[✓] Found buy button with selector: {selector}")
                break
        except NoSuchElementException:
            continue
    
    if not buy_button:
        # Try by text content
        try:
            buy_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Buy') or contains(text(), 'Purchase') or contains(text(), 'Add to cart')]")
        except NoSuchElementException:
            pass
    
    if buy_button:
        print("[+] Clicking buy button...")
        driver.execute_script("arguments[0].click();", buy_button)
        time.sleep(3)
    else:
        print("[!] Could not find buy button, continuing...")
    
    # Navigate to cart
    print("[+] Opening cart to finalize purchase...")
    driver.get(XBOX_CART_URL)
    time.sleep(5)
    
    # Look for checkout/buy button in cart
    checkout_selectors = [
        "button[data-testid='CheckoutButton']",
        "button[aria-label*='Checkout']",
        "button[aria-label*='Buy now']",
        ".checkout-button",
        ".buy-now-button",
        "button:contains('Checkout')",
        "button:contains('Buy now')",
        "[data-testid*='checkout']"
    ]
    
    print("[+] Looking for checkout button in cart...")
    checkout_button = None
    for selector in checkout_selectors:
        try:
            checkout_button = driver.find_element(By.CSS_SELECTOR, selector)
            if checkout_button and checkout_button.is_displayed():
                print(f"[✓] Found checkout button with selector: {selector}")
                break
        except NoSuchElementException:
            continue
    
    if not checkout_button:
        try:
            checkout_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Checkout') or contains(text(), 'Buy now') or contains(text(), 'Complete purchase')]")
        except NoSuchElementException:
            pass
    
    if checkout_button:
        print("[+] Clicking checkout button...")
        driver.execute_script("arguments[0].click();", checkout_button)
        time.sleep(5)
        
        # Wait for purchase confirmation or payment page
        print("[+] Waiting for purchase completion...")
        time.sleep(10)
    else:
        print("[!] Could not find checkout button, purchase may need manual completion")
    
    return True

def open_fortnite_cloud(driver):
    """Open Fortnite in Xbox Cloud Gaming"""
    print("[+] Opening Fortnite in Xbox Cloud...")
    driver.get(XBOX_FORTNITE_URL)
    time.sleep(15)  # Wait for cloud gaming to load
    
    # Look for play button
    play_selectors = [
        "button[data-testid='PlayButton']",
        "button[aria-label*='Play']",
        ".play-button",
        "button:contains('Play')",
        "[data-testid*='play']"
    ]
    
    for selector in play_selectors:
        try:
            play_button = driver.find_element(By.CSS_SELECTOR, selector)
            if play_button and play_button.is_displayed():
                print("[+] Clicking play button...")
                driver.execute_script("arguments[0].click();", play_button)
                break
        except NoSuchElementException:
            continue
    
    time.sleep(30)  # Wait for game to load

def get_epic_auth_code(driver):
    """Get Epic Games authorization code"""
    print("[+] Opening Epic auth link...")
    driver.get(EPIC_AUTH_LINK)
    time.sleep(5)
    
    # Wait for redirect and extract auth code from URL
    current_url = driver.current_url
    if "authorizationCode=" in current_url:
        auth_code = current_url.split("authorizationCode=")[1].split("&")[0]
        print(f"[✓] Auto-extracted auth code: {auth_code[:20]}...")
        return auth_code
    else:
        # Fallback to manual input if auto-extraction fails
        print("[!] Could not auto-extract auth code")
        auth_code = input("Paste the authorizationCode: ").strip()
        return auth_code

def redeem_vbucks(auth_code):
    """Redeem V-Bucks using Epic Games API"""
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
        
        print("[+] Redeeming token for 950 V-Bucks...")
        redeem_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ExchangeGiftToken?profileId=athena"
        redeem_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        redeem_response = requests.post(redeem_url, headers=redeem_headers, json={})
        
        if redeem_response.status_code == 200:
            print("[✔] Token redeemed successfully - 950 V-Bucks added!")
            return True
        else:
            print(f"[✘] Failed to redeem token: {redeem_response.text}")
            return False
            
    except Exception as e:
        print(f"[✘] Error during redemption: {e}")
        return False

def open_refund_page(driver):
    """Open Xbox refund page and auto-fill if possible"""
    print("[+] Opening Xbox refund page...")
    driver.get(XBOX_REFUND_URL)
    time.sleep(5)
    
    # Look for refund form elements and try to auto-fill
    try:
        # Look for recent purchase or refund button
        refund_selectors = [
            "button[data-testid='RefundButton']",
            "button[aria-label*='Refund']",
            ".refund-button",
            "button:contains('Refund')",
            "a:contains('Request refund')"
        ]
        
        for selector in refund_selectors:
            try:
                refund_button = driver.find_element(By.CSS_SELECTOR, selector)
                if refund_button and refund_button.is_displayed():
                    print("[+] Found refund button, clicking...")
                    driver.execute_script("arguments[0].click();", refund_button)
                    time.sleep(3)
                    break
            except NoSuchElementException:
                continue
                
    except Exception as e:
        print(f"[!] Could not auto-click refund: {e}")
    
    print("[✔] Refund page opened. Complete manually if not automated.")

def main():
    """Main automation function"""
    driver = None
    try:
        print("=== FORTNITE V-BUCKS AUTOMATION ===")
        print("[+] Starting browser automation...")
        
        # Setup browser
        driver = setup_browser()
        driver.maximize_window()
        
        # Step 1: Add to cart and buy Apex token
        add_to_cart_and_buy(driver)
        
        # Step 2: Open Fortnite cloud gaming
        open_fortnite_cloud(driver)
        
        # Step 3: Get Epic auth code
        auth_code = get_epic_auth_code(driver)
        
        # Step 4: Redeem V-Bucks
        if auth_code:
            redeem_success = redeem_vbucks(auth_code)
            if redeem_success:
                print("[✔] V-Bucks redemption completed!")
            else:
                print("[✘] V-Bucks redemption failed!")
        
        # Step 5: Open refund page
        open_refund_page(driver)
        
        print("\n[✔] Automation completed!")
        print("Browser will remain open for manual verification/completion if needed.")
        
        # Keep browser open for manual review
        input("Press Enter to close browser and exit...")
        
    except Exception as e:
        print(f"[✘] Error during automation: {e}")
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()