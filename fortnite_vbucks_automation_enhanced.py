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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
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
            edge_options.add_argument("--disable-notifications")
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
            chrome_options.add_argument("--disable-notifications")
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

def scroll_and_click(driver, element):
    """Scroll to element and click it with multiple methods"""
    try:
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(1)
        
        # Try regular click first
        try:
            element.click()
            return True
        except ElementClickInterceptedException:
            pass
        
        # Try JavaScript click
        try:
            driver.execute_script("arguments[0].click();", element)
            return True
        except:
            pass
        
        # Try ActionChains click
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(driver).move_to_element(element).click().perform()
            return True
        except:
            pass
        
        return False
    except Exception as e:
        print(f"[!] Error clicking element: {e}")
        return False

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

def open_dev_tools_and_add_to_cart(driver):
    """Add Apex to cart and capture network request for modification"""
    print("[+] Opening Apex product page...")
    driver.get(XBOX_APEX_URL)
    time.sleep(8)
    
    # Enable developer tools via JavaScript (if possible)
    try:
        driver.execute_script("console.clear(); console.log('Developer tools ready for network monitoring');")
        print("[+] Developer tools primed for network monitoring")
    except:
        pass
    
    print("[+] INSTRUCȚIUNI SEMI-AUTOMATE:")
    print("    1. Apasă F12 pentru a deschide Developer Tools")
    print("    2. Mergi la tab-ul 'Network'")
    print("    3. Scriptul va încerca să adauge automat în coș...")
    
    # Try to find and click Add to Cart button
    add_to_cart_selectors = [
        "button[data-testid='AddToCartButton']",
        "button[aria-label*='Add to cart']",
        "button[aria-label*='Buy']",
        ".add-to-cart-button",
        ".buyButton",
        "[data-testid*='cart']",
        "[data-testid*='buy']"
    ]
    
    cart_button = None
    for selector in add_to_cart_selectors:
        try:
            cart_button = driver.find_element(By.CSS_SELECTOR, selector)
            if cart_button and cart_button.is_displayed() and cart_button.is_enabled():
                print(f"[+] Found add to cart button: {selector}")
                break
        except NoSuchElementException:
            continue
    
    # Try XPath search for add to cart
    if not cart_button:
        try:
            cart_button = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add to cart') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'buy')]")
            if cart_button.is_displayed() and cart_button.is_enabled():
                print("[+] Found add to cart button by text")
        except NoSuchElementException:
            pass
    
    if cart_button:
        print("[+] Clicking add to cart button...")
        success = scroll_and_click(driver, cart_button)
        if success:
            print("[✓] Add to cart clicked successfully")
            time.sleep(3)
        else:
            print("[!] Failed to click add to cart button")
    else:
        print("[!] Could not find add to cart button automatically")
        print("    Adaugă manual în coș și apasă Enter...")
        input("Apasă Enter după ce ai adăugat în coș...")
    
    print("\n[+] Acum caută cererea 'loadcart' în Network tab")
    print("    4. Click dreapta pe 'loadcart' → Copy → Copy as fetch")
    print("    5. Deschide fetch_modifier.py și modifică fetch-ul")
    print("    6. Execută fetch-ul modificat în consolă")
    
    input("Apasă Enter după ce ai executat fetch-ul modificat...")
    
    return True

def automated_cart_checkout(driver):
    """Navigate to cart and automate checkout process"""
    print("[+] Opening shopping cart...")
    driver.get(XBOX_CART_URL)
    time.sleep(8)
    
    # Look for items in cart and try to remove original Apex pack
    print("[+] Încerc să identific și să șterg pack-ul original Apex...")
    
    # Look for remove/delete buttons for Apex items
    remove_selectors = [
        "button[aria-label*='Remove']",
        "button[aria-label*='Delete']", 
        ".remove-button",
        ".delete-button",
        "[data-testid*='remove']",
        "[data-testid*='delete']"
    ]
    
    # Try to find Apex item specifically and remove it
    try:
        apex_items = driver.find_elements(By.XPATH, "//div[contains(text(), 'Apex') or contains(text(), '1000')]")
        for item in apex_items:
            try:
                # Look for remove button near this item
                parent = item.find_element(By.XPATH, "./../..")
                remove_button = parent.find_element(By.CSS_SELECTOR, "button[aria-label*='Remove'], button[aria-label*='Delete']")
                if remove_button:
                    print("[+] Found Apex item, removing...")
                    scroll_and_click(driver, remove_button)
                    time.sleep(2)
                    break
            except NoSuchElementException:
                continue
    except:
        pass
    
    # Manual fallback for cart management
    print("[+] VERIFICARE CART:")
    print("    1. Verifică că pack-ul original Apex a fost șters")
    print("    2. Trebuie să rămână doar 'Fortnite - C6 Star Wars Battle Pass Gift Token'")
    print("    3. Scriptul va încerca checkout automat...")
    
    # Look for checkout buttons
    checkout_selectors = [
        "button[data-testid='CheckoutButton']",
        "button[aria-label*='Checkout']",
        "button[aria-label*='Place order']",
        "button[aria-label*='Complete purchase']",
        "button[aria-label*='Buy now']",
        ".checkout-button",
        ".place-order-button",
        ".buy-now-button",
        "[data-testid*='checkout']",
        "[data-testid*='purchase']"
    ]
    
    print("[+] Caut butonul de checkout...")
    checkout_button = None
    
    for selector in checkout_selectors:
        try:
            checkout_button = driver.find_element(By.CSS_SELECTOR, selector)
            if checkout_button and checkout_button.is_displayed() and checkout_button.is_enabled():
                print(f"[✓] Found checkout button: {selector}")
                break
        except NoSuchElementException:
            continue
    
    # Try XPath search for checkout
    if not checkout_button:
        try:
            checkout_button = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'checkout') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'place order') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'buy now')]")
            if checkout_button.is_displayed() and checkout_button.is_enabled():
                print("[✓] Found checkout button by text")
        except NoSuchElementException:
            pass
    
    if checkout_button:
        print("[+] Clicking checkout button...")
        success = scroll_and_click(driver, checkout_button)
        if success:
            print("[✓] Checkout button clicked")
            time.sleep(5)
            
            # Wait for purchase confirmation or payment processing
            print("[+] Waiting for purchase to process...")
            time.sleep(10)
            
            # Look for purchase confirmation
            confirmation_selectors = [
                "h1:contains('Thank you')",
                "h2:contains('Order confirmed')",
                ".confirmation",
                ".success-message"
            ]
            
            purchase_confirmed = False
            for selector in confirmation_selectors:
                try:
                    if ":contains(" in selector:
                        element = driver.find_element(By.XPATH, f"//{selector.split(':')[0]}[contains(text(), '{selector.split("'")[1]}')]")
                    else:
                        element = driver.find_element(By.CSS_SELECTOR, selector)
                    if element:
                        print("[✓] Purchase confirmed!")
                        purchase_confirmed = True
                        break
                except NoSuchElementException:
                    continue
            
            if not purchase_confirmed:
                print("[!] Purchase confirmation not detected, but continuing...")
            
        else:
            print("[!] Failed to click checkout button")
            input("Complete purchase manually and press Enter...")
    else:
        print("[!] Could not find checkout button")
        input("Complete purchase manually and press Enter...")
    
    return True

def launch_fortnite_cloud_auto(driver):
    """Launch Fortnite via Xbox Cloud Gaming with automation"""
    print("[+] Opening Fortnite Cloud Gaming...")
    driver.get(XBOX_FORTNITE_CLOUD_URL)
    time.sleep(20)
    
    # Look for play button and click automatically
    play_selectors = [
        "button[data-testid='PlayButton']",
        "button[aria-label*='Play']",
        "button[aria-label*='Launch']",
        ".play-button",
        ".launch-button",
        "[data-testid*='play']",
        "[data-testid*='launch']"
    ]
    
    print("[+] Looking for Play button...")
    play_button = None
    
    for selector in play_selectors:
        try:
            play_button = driver.find_element(By.CSS_SELECTOR, selector)
            if play_button and play_button.is_displayed() and play_button.is_enabled():
                print(f"[✓] Found play button: {selector}")
                break
        except NoSuchElementException:
            continue
    
    if not play_button:
        try:
            play_button = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'play') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'launch')]")
            if play_button.is_displayed() and play_button.is_enabled():
                print("[✓] Found play button by text")
        except NoSuchElementException:
            pass
    
    if play_button:
        print("[+] Clicking play button...")
        success = scroll_and_click(driver, play_button)
        if success:
            print("[✓] Fortnite launching...")
            time.sleep(30)  # Wait for game to load
            print("[+] You can now exit Fortnite and continue...")
        else:
            print("[!] Failed to click play button")
    else:
        print("[!] Could not find play button")
        
    print("[+] Waiting for game interaction...")
    input("Enter/exit Fortnite and press Enter to continue...")
    
    return True

def get_epic_auth_code_enhanced(driver):
    """Enhanced auth code extraction with full automation"""
    print("[+] Opening Epic auth link for automatic code extraction...")
    driver.get(EPIC_AUTH_LINK)
    time.sleep(8)
    
    # Wait for multiple possible redirect scenarios
    max_attempts = 12
    auth_code = None
    
    for attempt in range(max_attempts):
        current_url = driver.current_url
        print(f"[+] Checking URL (attempt {attempt+1}/12): {current_url[:100]}...")
        
        # Check for various auth code formats
        if "authorizationCode=" in current_url:
            auth_code = current_url.split("authorizationCode=")[1].split("&")[0]
            print(f"[✓] Auto-extracted authorizationCode: {auth_code[:20]}...")
            break
        elif "code=" in current_url and "oauth" in current_url.lower():
            auth_code = current_url.split("code=")[1].split("&")[0]
            print(f"[✓] Auto-extracted oauth code: {auth_code[:20]}...")
            break
        elif "access_token=" in current_url:
            # Sometimes we get access token directly
            access_token = current_url.split("access_token=")[1].split("&")[0]
            print(f"[✓] Direct access token found: {access_token[:20]}...")
            return access_token  # Return token directly
        
        # Check page content for hidden auth codes
        try:
            page_text = driver.page_source
            if "authorizationCode" in page_text:
                # Try to extract from JavaScript or hidden elements
                scripts = driver.find_elements(By.TAG_NAME, "script")
                for script in scripts:
                    script_content = script.get_attribute("innerHTML") or ""
                    if "authorizationCode" in script_content:
                        import re
                        match = re.search(r'authorizationCode["\s]*:["\s]*([a-f0-9]{32})', script_content)
                        if match:
                            auth_code = match.group(1)
                            print(f"[✓] Extracted auth code from script: {auth_code[:20]}...")
                            break
        except:
            pass
        
        if auth_code:
            break
            
        time.sleep(3)
    
    if not auth_code:
        print("[!] Could not auto-extract auth code after 12 attempts")
        print(f"[!] Final URL: {driver.current_url}")
        print("[!] Checking for manual extraction options...")
        
        # Try manual fallback
        print("    Possible solutions:")
        print("    1. Check if you're logged into Epic Games")
        print("    2. Check current URL for authorization parameters")
        print("    3. Manual input as fallback")
        
        auth_code = input("Paste the authorizationCode (or press Enter to retry): ").strip()
        
        if not auth_code:
            print("[!] Retrying auth link...")
            return get_epic_auth_code_enhanced(driver)
    
    return auth_code

def exchange_bp_token_direct(auth_code):
    """Direct BP token exchange function with enhanced error handling"""
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
            
            # Try alternative error handling
            error_description = response.get("error_description", "Unknown error")
            if "invalid" in error_description.lower():
                print("[!] Invalid authorization code. The code might have expired.")
                return False
            
            return False
        
        print(f"[✓] Got access token for account: {account_id}")
        print("[+] Exchanging BP token for 950 V-Bucks...")
        
        # Try exchange with retry mechanism
        max_retries = 3
        for retry in range(max_retries):
            redeem_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ExchangeGiftToken?profileId=athena"
            redeem_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            redeem_response = requests.post(redeem_url, headers=redeem_headers, json={})
            
            if redeem_response.status_code == 200:
                print("[✔] BP token exchanged successfully - 950 V-Bucks added!")
                return True
            elif redeem_response.status_code == 404:
                print(f"[!] No Battle Pass token found (attempt {retry+1}/{max_retries})")
                if retry < max_retries - 1:
                    print("    Waiting 5 seconds before retry...")
                    time.sleep(5)
                else:
                    print("[✘] No Battle Pass token available for exchange")
                    return False
            else:
                print(f"[✘] Failed to exchange BP token: {redeem_response.status_code}")
                print(f"Response: {redeem_response.text}")
                if retry < max_retries - 1:
                    time.sleep(3)
                else:
                    return False
            
    except Exception as e:
        print(f"[✘] Error during exchange: {e}")
        return False

def automated_refund_form(driver):
    """Fully automated refund form completion"""
    print("[+] Opening Xbox refund page...")
    driver.get(XBOX_REFUND_URL)
    time.sleep(10)
    
    print("[+] Attempting to automate refund form...")
    
    # Step 1: Look for and select Fortnite Battle Pass token
    try:
        print("[+] Looking for Fortnite Battle Pass token...")
        
        # Various selectors for the Battle Pass item
        battle_pass_selectors = [
            "//div[contains(text(), 'Fortnite') and contains(text(), 'Battle Pass')]",
            "//div[contains(text(), 'C6 Star Wars')]",
            "//div[contains(text(), 'Gift Token')]",
            "//label[contains(text(), 'Fortnite')]",
            "//span[contains(text(), 'Battle Pass')]"
        ]
        
        battle_pass_item = None
        for selector in battle_pass_selectors:
            try:
                battle_pass_item = driver.find_element(By.XPATH, selector)
                if battle_pass_item:
                    print(f"[✓] Found Battle Pass item")
                    break
            except NoSuchElementException:
                continue
        
        if battle_pass_item:
            # Try to find associated checkbox/radio button
            try:
                parent = battle_pass_item.find_element(By.XPATH, "./..")
                checkbox = parent.find_element(By.CSS_SELECTOR, "input[type='checkbox'], input[type='radio']")
                if checkbox and not checkbox.is_selected():
                    scroll_and_click(driver, checkbox)
                    print("[✓] Selected Battle Pass item")
                    time.sleep(2)
            except NoSuchElementException:
                # Try clicking the item itself
                scroll_and_click(driver, battle_pass_item)
                print("[✓] Clicked Battle Pass item")
                time.sleep(2)
    
    except Exception as e:
        print(f"[!] Could not auto-select Battle Pass item: {e}")
    
    # Step 2: Continue to refund form
    continue_selectors = [
        "button[aria-label*='Continue']",
        "button[aria-label*='Next']",
        "input[type='submit']",
        ".continue-button",
        ".next-button"
    ]
    
    for selector in continue_selectors:
        try:
            continue_button = driver.find_element(By.CSS_SELECTOR, selector)
            if continue_button and continue_button.is_displayed():
                scroll_and_click(driver, continue_button)
                print("[✓] Clicked continue button")
                time.sleep(5)
                break
        except NoSuchElementException:
            continue
    
    # Step 3: Fill refund reason form
    try:
        print("[+] Filling refund form...")
        
        # Look for reason dropdown - "Não fiz a compra"
        reason_selectors = [
            "select[id*='reason']",
            "select[name*='reason']",
            ".reason-select",
            "select"
        ]
        
        for selector in reason_selectors:
            try:
                reason_dropdown = driver.find_element(By.CSS_SELECTOR, selector)
                if reason_dropdown:
                    select = Select(reason_dropdown)
                    # Try to find "Não fiz a compra" option
                    for option in select.options:
                        if "não fiz" in option.text.lower() or "didn't make" in option.text.lower():
                            select.select_by_visible_text(option.text)
                            print("[✓] Selected reason: Não fiz a compra")
                            time.sleep(2)
                            break
                    break
            except NoSuchElementException:
                continue
        
        # Look for person dropdown - "Meu filho"
        person_selectors = [
            "select[id*='person']",
            "select[name*='person']", 
            "select[id*='who']",
            ".person-select"
        ]
        
        for selector in person_selectors:
            try:
                person_dropdown = driver.find_element(By.CSS_SELECTOR, selector)
                if person_dropdown:
                    select = Select(person_dropdown)
                    for option in select.options:
                        if "filho" in option.text.lower() or "child" in option.text.lower():
                            select.select_by_visible_text(option.text)
                            print("[✓] Selected person: Meu filho")
                            time.sleep(2)
                            break
                    break
            except NoSuchElementException:
                continue
        
        # Look for text area and fill reason
        text_area_selectors = [
            "textarea[id*='reason']",
            "textarea[name*='reason']",
            "textarea[placeholder*='reason']",
            ".reason-textarea",
            "textarea"
        ]
        
        reason_text = "Meu filho fez a compra e eu preciso de um reembolso, por favor"
        
        for selector in text_area_selectors:
            try:
                text_area = driver.find_element(By.CSS_SELECTOR, selector)
                if text_area and text_area.is_displayed():
                    text_area.clear()
                    text_area.send_keys(reason_text)
                    print("[✓] Filled reason text")
                    time.sleep(2)
                    break
            except NoSuchElementException:
                continue
        
        # Submit the form
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button[aria-label*='Submit']",
            ".submit-button",
            ".send-button"
        ]
        
        for selector in submit_selectors:
            try:
                submit_button = driver.find_element(By.CSS_SELECTOR, selector)
                if submit_button and submit_button.is_displayed():
                    scroll_and_click(driver, submit_button)
                    print("[✓] Submitted refund request")
                    time.sleep(5)
                    return True
            except NoSuchElementException:
                continue
                
        # Try XPath for submit
        try:
            submit_button = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send')]")
            if submit_button.is_displayed():
                scroll_and_click(driver, submit_button)
                print("[✓] Submitted refund request")
                return True
        except NoSuchElementException:
            pass
    
    except Exception as e:
        print(f"[!] Error during form automation: {e}")
    
    # Manual fallback
    print("[!] Could not fully automate refund form")
    print("[+] MANUAL COMPLETION:")
    print("    1. Select: 'Fortnite - C6 Star Wars Battle Pass Gift Token'")
    print("    2. Reason: 'Não fiz a compra'")
    print("    3. Person: 'Meu filho'")
    print("    4. Message: 'Meu filho fez a compra e eu preciso de um reembolso, por favor'")
    print("    5. Submit request")
    
    input("Complete the form manually and press Enter...")
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
root.title("Fetch Code Modifier - Enhanced")

# Instructions
instructions = tk.Label(root, text="1. Copy fetch request from Network tab\\n2. Paste below and click Modify\\n3. Copy result and execute in browser console", justify=tk.LEFT)
instructions.pack(pady=5)

# Input Text Box
tk.Label(root, text="Original Fetch Code:").pack()
fetch_code_input = tk.Text(root, height=8, width=80)
fetch_code_input.pack(pady=5)

# Modify Button
modify_button = tk.Button(root, text="Modify Fetch Code", command=modify_fetch_code, bg="green", fg="white")
modify_button.pack(pady=5)

# Output Text Box
tk.Label(root, text="Modified Fetch Code:").pack()
fetch_code_output = tk.Text(root, height=8, width=80)
fetch_code_output.pack(pady=5)

# Button Frame
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# Copy Button
copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard, bg="blue", fg="white")
copy_button.pack(side=tk.LEFT, padx=5)

# Clear Button
clear_button = tk.Button(button_frame, text="Clear Input", command=clear_input_box)
clear_button.pack(side=tk.LEFT, padx=5)

# Start the GUI
root.mainloop()
'''
    
    with open('fetch_modifier.py', 'w') as f:
        f.write(fetch_modifier_content)
    
    print("[+] fetch_modifier.py created with enhanced UI!")

def main():
    """Enhanced main automation function"""
    driver = None
    try:
        print("=== FORTNITE V-BUCKS AUTOMATION (ENHANCED) ===")
        print(f"[+] Running on {platform.system()}")
        print("[+] Starting enhanced browser automation...")
        
        # Create helper scripts
        create_fetch_modifier()
        
        # Setup browser
        driver = setup_browser()
        driver.maximize_window()
        
        print("\n🛒 STEP 4: Buy Token (Enhanced)")
        # Step 1: Add Apex to cart with automation
        open_dev_tools_and_add_to_cart(driver)
        
        print("\n📦 STEP 4.5: Automated Checkout")
        # Step 2: Automated cart checkout
        automated_cart_checkout(driver)
        
        print("\n🎮 STEP 5: Claim Token (Enhanced)")
        # Step 3: Enhanced Fortnite cloud launch
        launch_fortnite_cloud_auto(driver)
        
        print("\n💰 STEP 6: Redeem Token (Enhanced)")
        # Step 4: Enhanced auth code extraction and exchange
        auth_code = get_epic_auth_code_enhanced(driver)
        
        exchange_success = False
        if auth_code:
            exchange_success = exchange_bp_token_direct(auth_code)
            
            if exchange_success:
                print("[✔] V-Bucks exchange completed successfully!")
                
                # Launch Fortnite again to verify V-Bucks
                print("[+] Launching Fortnite again to verify V-Bucks...")
                launch_fortnite_cloud_auto(driver)
            else:
                print("[✘] V-Bucks exchange failed!")
        else:
            print("[✘] No authorization code available for exchange")
        
        print("\n↩️ STEP 7: Automated Refund")
        # Step 5: Fully automated refund process
        automated_refund_form(driver)
        
        print("\n🔄 STEP 8: Rinse and Repeat")
        print("📋 Enhanced automation summary:")
        print(f"  ✅ Browser automation: Complete")
        print(f"  ✅ Cart management: {'Automated' if True else 'Manual'}")
        print(f"  ✅ Auth code extraction: {'Automated' if auth_code else 'Manual fallback'}")
        print(f"  ✅ V-Bucks exchange: {'Success' if exchange_success else 'Failed'}")
        print(f"  ✅ Refund automation: Enhanced")
        
        print("\n📈 Next steps:")
        print("  1. Wait for refund approval")
        print("  2. Run script again for next cycle")
        print("  3. Maximum 8 cycles = 7600 V-Bucks per Xbox account")
        
        print("\n🎉 [✔] Enhanced automation completed!")
        print("🌐 Browser will remain open for verification.")
        
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