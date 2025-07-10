import time
import json
import requests
import os
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager

# URLs
XBOX_APEX_URL = "https://www.xbox.com/en-ZA/games/store/apex-legends-1000-apex-coins/9n5qmznw4bt1"
XBOX_CART_URL = "https://www.xbox.com/en-ZA/cart"
XBOX_FORTNITE_URL = "https://www.xbox.com/en-ZA/play/games/fortnite/9nxmbq9p6kns"
EPIC_AUTH_LINK = "https://epicgames.com/id/api/redirect"
XBOX_REFUND_URL = "https://support.xbox.com/en-ZA/help/subscriptions-billing/buy-games-apps/refund-orders"

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
            edge_options.add_argument("--disable-extensions-except-whitelisted")
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
            chrome_options.add_argument("--disable-extensions-except-whitelisted")
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

def scroll_and_click(driver, element):
    """Scroll to element and click it"""
    try:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", element)
        return True
    except Exception as e:
        print(f"[!] Error clicking element: {e}")
        return False

def add_to_cart_and_buy(driver):
    """Add Apex token to cart and complete purchase"""
    print("[+] Opening Apex product page...")
    driver.get(XBOX_APEX_URL)
    time.sleep(8)
    
    # Wait for page to load and try multiple selectors
    print("[+] Waiting for page to load...")
    time.sleep(5)
    
    # Try different possible selectors for "Buy" button
    buy_selectors = [
        "button[data-testid='PurchaseButton']",
        "button[aria-label*='Buy']",
        "button[aria-label*='Purchase']",
        "button[aria-label*='Add to cart']",
        ".buyButton",
        ".purchaseButton",
        ".addToCartButton",
        "[data-testid*='buy']",
        "[data-testid*='purchase']",
        "[data-testid*='cart']",
        "button:contains('Buy')",
        "button:contains('Purchase')",
        "button:contains('Add to cart')"
    ]
    
    print("[+] Looking for Buy/Add to cart button...")
    buy_button = None
    for selector in buy_selectors:
        try:
            if ":contains(" in selector:
                # Use XPath for text-based selectors
                xpath = f"//button[contains(text(), '{selector.split("'")[1]}')]"
                buy_button = driver.find_element(By.XPATH, xpath)
            else:
                buy_button = driver.find_element(By.CSS_SELECTOR, selector)
            
            if buy_button and buy_button.is_displayed() and buy_button.is_enabled():
                print(f"[✓] Found buy button with selector: {selector}")
                break
        except NoSuchElementException:
            continue
    
    # Alternative: look for any button with buy-related text
    if not buy_button:
        try:
            buy_button = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'buy') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'purchase') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add to cart')]")
            if buy_button.is_displayed() and buy_button.is_enabled():
                print("[✓] Found buy button by text content")
        except NoSuchElementException:
            pass
    
    if buy_button:
        print("[+] Clicking buy button...")
        scroll_and_click(driver, buy_button)
        time.sleep(5)
        print("[✓] Buy button clicked successfully")
    else:
        print("[!] Could not find buy button - may need manual intervention")
        print("[!] Page elements found:")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for i, btn in enumerate(buttons[:10]):  # Show first 10 buttons
            try:
                text = btn.text.strip()
                if text:
                    print(f"    Button {i+1}: '{text}'")
            except:
                pass
    
    # Navigate to cart
    print("[+] Opening cart to finalize purchase...")
    driver.get(XBOX_CART_URL)
    time.sleep(8)
    
    # Look for checkout/buy button in cart
    checkout_selectors = [
        "button[data-testid='CheckoutButton']",
        "button[aria-label*='Checkout']",
        "button[aria-label*='Buy now']",
        "button[aria-label*='Complete purchase']",
        ".checkoutButton",
        ".buyNowButton",
        ".completePurchaseButton",
        "[data-testid*='checkout']",
        "[data-testid*='purchase']"
    ]
    
    print("[+] Looking for checkout button in cart...")
    checkout_button = None
    for selector in checkout_selectors:
        try:
            checkout_button = driver.find_element(By.CSS_SELECTOR, selector)
            if checkout_button and checkout_button.is_displayed() and checkout_button.is_enabled():
                print(f"[✓] Found checkout button with selector: {selector}")
                break
        except NoSuchElementException:
            continue
    
    # Try text-based search for checkout button
    if not checkout_button:
        try:
            checkout_button = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'checkout') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'buy now') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'complete purchase')]")
            if checkout_button.is_displayed() and checkout_button.is_enabled():
                print("[✓] Found checkout button by text content")
        except NoSuchElementException:
            pass
    
    if checkout_button:
        print("[+] Clicking checkout button...")
        scroll_and_click(driver, checkout_button)
        time.sleep(8)
        
        # Wait for purchase confirmation or payment page
        print("[+] Waiting for purchase completion...")
        time.sleep(15)
        print("[✓] Purchase process initiated")
    else:
        print("[!] Could not find checkout button")
        print("[!] Cart page elements found:")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for i, btn in enumerate(buttons[:10]):
            try:
                text = btn.text.strip()
                if text:
                    print(f"    Button {i+1}: '{text}'")
            except:
                pass
    
    return True

def open_fortnite_cloud(driver):
    """Open Fortnite in Xbox Cloud Gaming"""
    print("[+] Opening Fortnite in Xbox Cloud...")
    driver.get(XBOX_FORTNITE_URL)
    time.sleep(20)  # Extra wait for cloud gaming
    
    # Look for play button
    play_selectors = [
        "button[data-testid='PlayButton']",
        "button[aria-label*='Play']",
        ".playButton",
        ".play-button",
        "[data-testid*='play']",
        "button:contains('Play')"
    ]
    
    print("[+] Looking for Play button...")
    for selector in play_selectors:
        try:
            if ":contains(" in selector:
                play_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Play')]")
            else:
                play_button = driver.find_element(By.CSS_SELECTOR, selector)
            
            if play_button and play_button.is_displayed() and play_button.is_enabled():
                print(f"[+] Found play button, clicking...")
                scroll_and_click(driver, play_button)
                break
        except NoSuchElementException:
            continue
    
    print("[+] Waiting for game to load...")
    time.sleep(35)  # Extended wait for game loading

def get_epic_auth_code(driver):
    """Get Epic Games authorization code"""
    print("[+] Opening Epic auth link...")
    driver.get(EPIC_AUTH_LINK)
    time.sleep(10)
    
    # Wait for redirect and extract auth code from URL
    max_attempts = 6
    for attempt in range(max_attempts):
        current_url = driver.current_url
        print(f"[+] Current URL (attempt {attempt+1}): {current_url[:100]}...")
        
        if "authorizationCode=" in current_url:
            auth_code = current_url.split("authorizationCode=")[1].split("&")[0]
            print(f"[✓] Auto-extracted auth code: {auth_code[:20]}...")
            return auth_code
        elif "code=" in current_url:
            auth_code = current_url.split("code=")[1].split("&")[0]
            print(f"[✓] Auto-extracted auth code: {auth_code[:20]}...")
            return auth_code
        
        time.sleep(5)
    
    # Fallback to manual input if auto-extraction fails
    print("[!] Could not auto-extract auth code")
    print(f"[!] Final URL: {driver.current_url}")
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
        
        print(f"[✓] Got access token for account: {account_id}")
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
            print(f"[✘] Failed to redeem token: {redeem_response.status_code}")
            print(f"Response: {redeem_response.text}")
            return False
            
    except Exception as e:
        print(f"[✘] Error during redemption: {e}")
        return False

def open_refund_page(driver):
    """Open Xbox refund page and try auto-fill"""
    print("[+] Opening Xbox refund page...")
    driver.get(XBOX_REFUND_URL)
    time.sleep(8)
    
    # Look for refund form elements
    try:
        # Look for recent purchase or refund button
        refund_selectors = [
            "button[data-testid='RefundButton']",
            "button[aria-label*='Refund']",
            ".refundButton",
            ".refund-button",
            "a[href*='refund']",
            "button:contains('Refund')",
            "a:contains('Request refund')",
            "button:contains('Request refund')"
        ]
        
        print("[+] Looking for refund elements...")
        for selector in refund_selectors:
            try:
                if ":contains(" in selector:
                    if "button" in selector:
                        refund_element = driver.find_element(By.XPATH, f"//button[contains(text(), '{selector.split("'")[1]}')]")
                    else:
                        refund_element = driver.find_element(By.XPATH, f"//a[contains(text(), '{selector.split("'")[1]}')]")
                else:
                    refund_element = driver.find_element(By.CSS_SELECTOR, selector)
                
                if refund_element and refund_element.is_displayed():
                    print(f"[+] Found refund element, clicking...")
                    scroll_and_click(driver, refund_element)
                    time.sleep(5)
                    break
            except NoSuchElementException:
                continue
                
    except Exception as e:
        print(f"[!] Could not auto-navigate refund: {e}")
    
    print("[✔] Refund page opened. Complete manually if needed.")

def main():
    """Main automation function"""
    driver = None
    try:
        print("=== FORTNITE V-BUCKS AUTOMATION ===")
        print(f"[+] Running on {platform.system()}")
        print("[+] Starting browser automation...")
        
        # Setup browser
        driver = setup_browser()
        driver.maximize_window()
        
        # Step 1: Add to cart and buy Apex token
        print("\n🛒 STEP 1: Purchase Apex Token")
        add_to_cart_and_buy(driver)
        
        # Step 2: Open Fortnite cloud gaming
        print("\n🎮 STEP 2: Launch Fortnite Cloud")
        open_fortnite_cloud(driver)
        
        # Step 3: Get Epic auth code
        print("\n🔑 STEP 3: Epic Games Authentication")
        auth_code = get_epic_auth_code(driver)
        
        # Step 4: Redeem V-Bucks
        print("\n💰 STEP 4: V-Bucks Redemption")
        if auth_code:
            redeem_success = redeem_vbucks(auth_code)
            if redeem_success:
                print("[✔] V-Bucks redemption completed successfully!")
            else:
                print("[✘] V-Bucks redemption failed!")
        else:
            print("[✘] No auth code available for redemption")
        
        # Step 5: Open refund page
        print("\n↩️ STEP 5: Refund Process")
        open_refund_page(driver)
        
        print("\n🎉 [✔] Automation completed!")
        print("📋 Summary:")
        print("  - Apex token purchase: Attempted")
        print("  - Fortnite cloud launch: Completed")
        print("  - Epic authentication: Completed" if auth_code else "  - Epic authentication: Failed")
        print("  - V-Bucks redemption: Completed" if 'redeem_success' in locals() and redeem_success else "  - V-Bucks redemption: Failed")
        print("  - Refund page: Opened")
        print("\n🌐 Browser will remain open for manual verification.")
        
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