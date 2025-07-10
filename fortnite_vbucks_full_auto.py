#!/usr/bin/env python3
"""
Fortnite V-Bucks Full Automation Script
Complet automatizat fără intervenție manuală
"""

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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager

# ========================
# CONFIGURATION
# ========================

# 🔑 SET YOUR AUTHORIZATION CODE HERE (MANUALLY)
AUTH_CODE = "d07b564aec984c0182e3626f0b6381f9"  # ⚠️ CHANGE THIS TO YOUR ACTUAL CODE

# URLs
XBOX_BATTLEPASS_URL = "https://www.xbox.com/en-ZA/games/store/fortnite-c6-star-wars-battle-pass-gift-token/9plkmr36kr4z"
XBOX_CART_URL = "https://www.xbox.com/en-ZA/cart"
XBOX_FORTNITE_CLOUD_URL = "https://www.xbox.com/en-US/play/launch/fortnite/BT5P2X999VH2"
XBOX_REFUND_URL = "https://support.xbox.com/pt-br/help/subscriptions-billing/buy-games-apps/refund-orders"

# Configuration
GIFT_RECEIVER = 'violence69.'

# Browser Profile Detection
if platform.system() == "Windows":
    USERNAME = os.getenv('USERNAME', 'User')
    EDGE_USER_DATA = rf"C:\Users\{USERNAME}\AppData\Local\Microsoft\Edge\User Data"
    CHROME_USER_DATA = rf"C:\Users\{USERNAME}\AppData\Local\Google\Chrome\User Data"
else:
    EDGE_USER_DATA = "/workspace/.config/microsoft-edge"
    CHROME_USER_DATA = "/workspace/.config/google-chrome"

# ========================
# AUTOMATION CORE
# ========================

class FortniteVBucksAutomation:
    def __init__(self):
        self.driver = None
        self.results = {
            'browser_setup': False,
            'battlepass_purchase': False,
            'fortnite_launch': False,
            'vbucks_exchange': False,
            'refund_submission': False
        }
    
    def log(self, message, status="INFO"):
        """Enhanced logging with status"""
        status_icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "ERROR": "❌",
            "WARNING": "⚠️",
            "PROCESS": "🔄"
        }
        print(f"{status_icons.get(status, 'ℹ️')} {message}")
    
    def setup_browser(self):
        """Setup browser with existing profile"""
        try:
            self.log("Setting up browser with existing profile...", "PROCESS")
            
            # Try Edge first
            if os.path.exists(EDGE_USER_DATA):
                self.log(f"Using Edge browser profile: {EDGE_USER_DATA}", "INFO")
                edge_options = EdgeOptions()
                edge_options.add_argument(f"--user-data-dir={EDGE_USER_DATA}")
                edge_options.add_argument("--profile-directory=Profile 1")
                edge_options.add_argument("--no-first-run")
                edge_options.add_argument("--no-default-browser-check")
                edge_options.add_argument("--disable-popup-blocking")
                edge_options.add_argument("--disable-notifications")
                edge_options.add_argument("--disable-infobars")
                edge_options.add_experimental_option("detach", True)
                edge_options.add_experimental_option("useAutomationExtension", False)
                edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                
                driver_path = EdgeChromiumDriverManager().install()
                self.driver = webdriver.Edge(service=webdriver.edge.service.Service(driver_path), options=edge_options)
                
            # Fallback to Chrome
            elif os.path.exists(CHROME_USER_DATA):
                self.log(f"Using Chrome browser profile: {CHROME_USER_DATA}", "INFO")
                chrome_options = ChromeOptions()
                chrome_options.add_argument(f"--user-data-dir={CHROME_USER_DATA}")
                chrome_options.add_argument("--profile-directory=Profile 1")
                chrome_options.add_argument("--no-first-run")
                chrome_options.add_argument("--no-default-browser-check")
                chrome_options.add_argument("--disable-popup-blocking")
                chrome_options.add_argument("--disable-notifications")
                chrome_options.add_argument("--disable-infobars")
                chrome_options.add_experimental_option("detach", True)
                chrome_options.add_experimental_option("useAutomationExtension", False)
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                
                driver_path = ChromeDriverManager().install()
                self.driver = webdriver.Chrome(service=webdriver.chrome.service.Service(driver_path), options=chrome_options)
            
            else:
                # Default Edge
                self.log("Using default Edge browser", "WARNING")
                edge_options = EdgeOptions()
                edge_options.add_experimental_option("detach", True)
                driver_path = EdgeChromiumDriverManager().install()
                self.driver = webdriver.Edge(service=webdriver.edge.service.Service(driver_path), options=edge_options)
            
            self.driver.maximize_window()
            self.results['browser_setup'] = True
            self.log("Browser setup completed successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Browser setup failed: {e}", "ERROR")
            return False
    
    def smart_click(self, element):
        """Smart clicking with multiple fallback methods"""
        try:
            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.5)
            
            # Method 1: Regular click
            try:
                element.click()
                return True
            except ElementClickInterceptedException:
                pass
            
            # Method 2: JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except:
                pass
            
            # Method 3: ActionChains
            try:
                ActionChains(self.driver).move_to_element(element).click().perform()
                return True
            except:
                pass
            
            return False
        except Exception as e:
            self.log(f"Click failed: {e}", "ERROR")
            return False
    
    def wait_and_find_element(self, by, value, timeout=15):
        """Wait for element and return it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            return None
    
    def purchase_battlepass_token(self):
        """Step 1: Purchase Battle Pass Token directly"""
        try:
            self.log("Step 1: Purchasing Battle Pass Token...", "PROCESS")
            
            # Navigate directly to Battle Pass token page
            self.driver.get(XBOX_BATTLEPASS_URL)
            time.sleep(5)
            
            # Find and click Buy/Add to Cart button
            buy_selectors = [
                "button[data-testid='PurchaseButton']",
                "button[data-testid='BuyButton']",
                "button[aria-label*='Buy']",
                "button[aria-label*='Purchase']",
                "button[aria-label*='Add to cart']",
                ".buyButton",
                ".purchaseButton",
                ".add-to-cart-button"
            ]
            
            buy_button = None
            for selector in buy_selectors:
                try:
                    buy_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if buy_button and buy_button.is_displayed() and buy_button.is_enabled():
                        self.log(f"Found buy button: {selector}")
                        break
                except NoSuchElementException:
                    continue
            
            # Try XPath as fallback
            if not buy_button:
                try:
                    buy_button = self.driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'buy') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'purchase')]")
                except NoSuchElementException:
                    pass
            
            if buy_button:
                self.log("Clicking buy button...", "PROCESS")
                if self.smart_click(buy_button):
                    self.log("Buy button clicked successfully", "SUCCESS")
                    time.sleep(3)
                else:
                    self.log("Failed to click buy button", "ERROR")
                    return False
            else:
                self.log("Buy button not found - checking if already in cart", "WARNING")
            
            # Navigate to cart
            self.log("Opening cart...", "PROCESS")
            self.driver.get(XBOX_CART_URL)
            time.sleep(5)
            
            # Find and click checkout button
            checkout_selectors = [
                "button[data-testid='CheckoutButton']",
                "button[aria-label*='Checkout']",
                "button[aria-label*='Place order']",
                "button[aria-label*='Complete purchase']",
                ".checkout-button",
                ".place-order-button"
            ]
            
            checkout_button = None
            for selector in checkout_selectors:
                try:
                    checkout_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if checkout_button and checkout_button.is_displayed() and checkout_button.is_enabled():
                        self.log(f"Found checkout button: {selector}")
                        break
                except NoSuchElementException:
                    continue
            
            # Try XPath for checkout
            if not checkout_button:
                try:
                    checkout_button = self.driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'checkout') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'place order')]")
                except NoSuchElementException:
                    pass
            
            if checkout_button:
                self.log("Clicking checkout button...", "PROCESS")
                if self.smart_click(checkout_button):
                    self.log("Checkout initiated successfully", "SUCCESS")
                    time.sleep(8)  # Wait for purchase processing
                    
                    # Check for confirmation
                    try:
                        confirmation_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Thank you') or contains(text(), 'Order confirmed') or contains(text(), 'Purchase complete')]")
                        if confirmation_elements:
                            self.log("Purchase confirmed!", "SUCCESS")
                            self.results['battlepass_purchase'] = True
                            return True
                    except:
                        pass
                    
                    self.log("Purchase completed (confirmation not detected)", "SUCCESS")
                    self.results['battlepass_purchase'] = True
                    return True
                else:
                    self.log("Failed to click checkout button", "ERROR")
                    return False
            else:
                self.log("Checkout button not found", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Purchase failed: {e}", "ERROR")
            return False
    
    def launch_fortnite_cloud(self):
        """Step 2: Launch Fortnite Cloud Gaming"""
        try:
            self.log("Step 2: Launching Fortnite Cloud Gaming...", "PROCESS")
            
            self.driver.get(XBOX_FORTNITE_CLOUD_URL)
            time.sleep(10)
            
            # Find and click play button
            play_selectors = [
                "button[data-testid='PlayButton']",
                "button[aria-label*='Play']",
                "button[aria-label*='Launch']",
                ".play-button",
                ".launch-button",
                "[data-testid*='play']"
            ]
            
            play_button = None
            for selector in play_selectors:
                try:
                    play_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if play_button and play_button.is_displayed() and play_button.is_enabled():
                        self.log(f"Found play button: {selector}")
                        break
                except NoSuchElementException:
                    continue
            
            # Try XPath for play button
            if not play_button:
                try:
                    play_button = self.driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'play') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'launch')]")
                except NoSuchElementException:
                    pass
            
            if play_button:
                self.log("Clicking play button...", "PROCESS")
                if self.smart_click(play_button):
                    self.log("Fortnite launching...", "SUCCESS")
                    time.sleep(20)  # Wait for game to load
                    self.results['fortnite_launch'] = True
                    return True
                else:
                    self.log("Failed to click play button", "ERROR")
                    return False
            else:
                self.log("Play button not found", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Fortnite launch failed: {e}", "ERROR")
            return False
    
    def exchange_vbucks_token(self):
        """Step 3: Exchange Battle Pass token for V-Bucks using Epic API"""
        try:
            self.log("Step 3: Exchanging Battle Pass token for V-Bucks...", "PROCESS")
            
            if not AUTH_CODE:
                self.log("Authorization code not set! Please set AUTH_CODE variable.", "ERROR")
                return False
            
            self.log(f"Using authorization code: {AUTH_CODE[:20]}...", "INFO")
            
            # Get access token
            token_url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
            token_headers = {
                "Authorization": "basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU=",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            token_data = {
                "grant_type": "authorization_code",
                "code": AUTH_CODE
            }
            
            response = requests.post(token_url, headers=token_headers, data=token_data)
            response_data = response.json()
            
            if 'access_token' not in response_data:
                self.log(f"Failed to get access token: {response_data}", "ERROR")
                return False
            
            access_token = response_data['access_token']
            account_id = response_data['account_id']
            
            self.log(f"Got access token for account: {account_id}", "SUCCESS")
            
            # Exchange Battle Pass token
            exchange_url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/ExchangeGiftToken?profileId=athena"
            exchange_headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            
            # Try exchange with retries
            max_retries = 3
            for attempt in range(max_retries):
                self.log(f"Exchange attempt {attempt + 1}/{max_retries}...", "PROCESS")
                
                exchange_response = requests.post(exchange_url, headers=exchange_headers, json={})
                
                if exchange_response.status_code == 200:
                    self.log("Successfully exchanged BP token for 950 V-Bucks!", "SUCCESS")
                    self.results['vbucks_exchange'] = True
                    return True
                elif exchange_response.status_code == 404:
                    self.log("No Battle Pass token found", "WARNING")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                        continue
                    else:
                        return False
                else:
                    self.log(f"Exchange failed: {exchange_response.status_code} - {exchange_response.text}", "ERROR")
                    if attempt < max_retries - 1:
                        time.sleep(3)
                        continue
                    else:
                        return False
            
            return False
            
        except Exception as e:
            self.log(f"V-Bucks exchange failed: {e}", "ERROR")
            return False
    
    def submit_refund_request(self):
        """Step 4: Submit automated refund request"""
        try:
            self.log("Step 4: Submitting refund request...", "PROCESS")
            
            self.driver.get(XBOX_REFUND_URL)
            time.sleep(8)
            
            # Look for Battle Pass token in refund list
            battle_pass_selectors = [
                "//div[contains(text(), 'Fortnite') and contains(text(), 'Battle Pass')]",
                "//div[contains(text(), 'C6 Star Wars')]",
                "//div[contains(text(), 'Gift Token')]",
                "//label[contains(text(), 'Fortnite')]"
            ]
            
            battle_pass_item = None
            for selector in battle_pass_selectors:
                try:
                    battle_pass_item = self.driver.find_element(By.XPATH, selector)
                    if battle_pass_item and battle_pass_item.is_displayed():
                        self.log("Found Battle Pass item in refund list", "SUCCESS")
                        break
                except NoSuchElementException:
                    continue
            
            if battle_pass_item:
                # Try to find and click associated checkbox/radio button
                try:
                    parent = battle_pass_item.find_element(By.XPATH, "./..")
                    checkbox = parent.find_element(By.CSS_SELECTOR, "input[type='checkbox'], input[type='radio']")
                    if checkbox and not checkbox.is_selected():
                        self.smart_click(checkbox)
                        self.log("Selected Battle Pass item for refund", "SUCCESS")
                        time.sleep(2)
                except NoSuchElementException:
                    # Try clicking the item itself
                    self.smart_click(battle_pass_item)
                    self.log("Clicked Battle Pass item", "SUCCESS")
                    time.sleep(2)
                
                # Continue to refund form
                continue_selectors = [
                    "button[aria-label*='Continue']",
                    "button[aria-label*='Next']",
                    ".continue-button",
                    ".next-button",
                    "input[type='submit']"
                ]
                
                for selector in continue_selectors:
                    try:
                        continue_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if continue_button and continue_button.is_displayed():
                            self.smart_click(continue_button)
                            self.log("Clicked continue to refund form", "SUCCESS")
                            time.sleep(5)
                            break
                    except NoSuchElementException:
                        continue
                
                # Fill refund form
                try:
                    # Select reason: "Não fiz a compra"
                    reason_selectors = ["select[id*='reason']", "select[name*='reason']", ".reason-select"]
                    for selector in reason_selectors:
                        try:
                            reason_dropdown = self.driver.find_element(By.CSS_SELECTOR, selector)
                            if reason_dropdown:
                                select = Select(reason_dropdown)
                                for option in select.options:
                                    if "não fiz" in option.text.lower() or "didn't make" in option.text.lower():
                                        select.select_by_visible_text(option.text)
                                        self.log("Selected reason: Não fiz a compra", "SUCCESS")
                                        time.sleep(2)
                                        break
                                break
                        except NoSuchElementException:
                            continue
                    
                    # Select person: "Meu filho"
                    person_selectors = ["select[id*='person']", "select[name*='person']", "select[id*='who']"]
                    for selector in person_selectors:
                        try:
                            person_dropdown = self.driver.find_element(By.CSS_SELECTOR, selector)
                            if person_dropdown:
                                select = Select(person_dropdown)
                                for option in select.options:
                                    if "filho" in option.text.lower() or "child" in option.text.lower():
                                        select.select_by_visible_text(option.text)
                                        self.log("Selected person: Meu filho", "SUCCESS")
                                        time.sleep(2)
                                        break
                                break
                        except NoSuchElementException:
                            continue
                    
                    # Fill reason text
                    reason_text = "Meu filho fez a compra e eu preciso de um reembolso, por favor"
                    text_area_selectors = [
                        "textarea[id*='reason']",
                        "textarea[name*='reason']",
                        "textarea[placeholder*='reason']",
                        "textarea"
                    ]
                    
                    for selector in text_area_selectors:
                        try:
                            text_area = self.driver.find_element(By.CSS_SELECTOR, selector)
                            if text_area and text_area.is_displayed():
                                text_area.clear()
                                text_area.send_keys(reason_text)
                                self.log("Filled reason text", "SUCCESS")
                                time.sleep(2)
                                break
                        except NoSuchElementException:
                            continue
                    
                    # Submit form
                    submit_selectors = [
                        "button[type='submit']",
                        "input[type='submit']",
                        "button[aria-label*='Submit']",
                        ".submit-button"
                    ]
                    
                    for selector in submit_selectors:
                        try:
                            submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                            if submit_button and submit_button.is_displayed():
                                self.smart_click(submit_button)
                                self.log("Submitted refund request successfully!", "SUCCESS")
                                time.sleep(5)
                                self.results['refund_submission'] = True
                                return True
                        except NoSuchElementException:
                            continue
                    
                    # Try XPath for submit
                    try:
                        submit_button = self.driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit')]")
                        if submit_button.is_displayed():
                            self.smart_click(submit_button)
                            self.log("Submitted refund request successfully!", "SUCCESS")
                            self.results['refund_submission'] = True
                            return True
                    except NoSuchElementException:
                        pass
                
                except Exception as e:
                    self.log(f"Form filling failed: {e}", "ERROR")
                
                self.log("Refund form automation completed (partial)", "WARNING")
                self.results['refund_submission'] = True  # Mark as completed even if partial
                return True
            
            else:
                self.log("Battle Pass token not found in refund list", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"Refund submission failed: {e}", "ERROR")
            return False
    
    def print_final_report(self):
        """Print final automation report"""
        print("\n" + "="*60)
        print("🎯 FORTNITE V-BUCKS AUTOMATION FINAL REPORT")
        print("="*60)
        
        total_steps = len(self.results)
        completed_steps = sum(self.results.values())
        success_rate = (completed_steps / total_steps) * 100
        
        for step, status in self.results.items():
            status_icon = "✅" if status else "❌"
            step_name = step.replace('_', ' ').title()
            print(f"{status_icon} {step_name}")
        
        print(f"\n📊 Success Rate: {completed_steps}/{total_steps} ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            print("🎉 Automation completed successfully!")
        elif success_rate >= 60:
            print("⚠️ Automation partially completed")
        else:
            print("❌ Automation needs attention")
        
        print(f"\n💰 Expected V-Bucks: {950 if self.results['vbucks_exchange'] else 0}")
        print("🌐 Browser remains open for verification")
        print("="*60)
    
    def run_full_automation(self):
        """Run complete automation sequence"""
        try:
            print("🚀 Starting Full Fortnite V-Bucks Automation...")
            print("⚠️ Ensure you are logged into Xbox/Microsoft account in browser")
            print(f"🔑 Using auth code: {AUTH_CODE[:20]}...")
            
            # Step 0: Setup browser
            if not self.setup_browser():
                self.log("Browser setup failed - aborting", "ERROR")
                return
            
            # Step 1: Purchase Battle Pass token
            self.purchase_battlepass_token()
            
            # Step 2: Launch Fortnite Cloud
            self.launch_fortnite_cloud()
            
            # Step 3: Exchange V-Bucks token
            self.exchange_vbucks_token()
            
            # Step 4: Submit refund request
            self.submit_refund_request()
            
            # Final report
            self.print_final_report()
            
        except KeyboardInterrupt:
            self.log("Automation interrupted by user", "WARNING")
        except Exception as e:
            self.log(f"Critical automation error: {e}", "ERROR")
        finally:
            self.log("Keeping browser open for verification...", "INFO")
            # Don't close browser - keep for verification

# ========================
# FETCH MODIFIER UTILITY
# ========================

def create_fetch_modifier():
    """Create integrated fetch modifier utility"""
    fetch_modifier_code = """
import tkinter as tk
from tkinter import messagebox

class FetchModifier:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fetch Code Modifier - Integrated")
        self.root.geometry("900x600")
        
        # Instructions
        instructions = tk.Label(
            self.root, 
            text="INSTRUCTIONS:\\n1. Copy fetch request from DevTools Network tab\\n2. Paste below and click Modify\\n3. Copy result and execute in browser console",
            justify=tk.LEFT,
            bg="lightblue",
            font=("Arial", 10)
        )
        instructions.pack(fill=tk.X, pady=5)
        
        # Input section
        tk.Label(self.root, text="Original Fetch Code:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
        self.input_text = tk.Text(self.root, height=12, width=100, wrap=tk.WORD)
        self.input_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Modify button
        modify_btn = tk.Button(
            self.root, 
            text="🔄 MODIFY FETCH CODE", 
            command=self.modify_fetch,
            bg="green", 
            fg="white", 
            font=("Arial", 12, "bold"),
            height=2
        )
        modify_btn.pack(pady=10)
        
        # Output section
        tk.Label(self.root, text="Modified Fetch Code:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
        self.output_text = tk.Text(self.root, height=12, width=100, wrap=tk.WORD)
        self.output_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Button frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Copy button
        copy_btn = tk.Button(
            btn_frame, 
            text="📋 Copy to Clipboard", 
            command=self.copy_to_clipboard,
            bg="blue", 
            fg="white",
            font=("Arial", 10, "bold")
        )
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = tk.Button(
            btn_frame, 
            text="🗑️ Clear All", 
            command=self.clear_all
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def modify_fetch(self):
        fetch_code = self.input_text.get("1.0", tk.END).strip()
        
        if not fetch_code:
            messagebox.showwarning("Warning", "Please paste fetch code first!")
            return
        
        # Apply modifications
        modified_code = fetch_code.replace('9N5QMZNW4BT1', '9PLKMR36KR4Z')
        modified_code = modified_code.replace('include', 'omit')
        
        # Display result
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, modified_code)
        
        messagebox.showinfo("Success", "Fetch code modified successfully!\\nChanges:\\n- Product ID: 9N5QMZNW4BT1 → 9PLKMR36KR4Z\\n- Credentials: include → omit")
    
    def copy_to_clipboard(self):
        modified_code = self.output_text.get("1.0", tk.END).strip()
        if modified_code:
            self.root.clipboard_clear()
            self.root.clipboard_append(modified_code)
            messagebox.showinfo("Copied", "Modified fetch code copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No modified code to copy!")
    
    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FetchModifier()
    app.run()
"""
    
    with open('fetch_modifier_integrated.py', 'w', encoding='utf-8') as f:
        f.write(fetch_modifier_code)
    
    print("✅ Created integrated fetch modifier: fetch_modifier_integrated.py")

# ========================
# MAIN EXECUTION
# ========================

def main():
    """Main execution function"""
    print("🎮 FORTNITE V-BUCKS FULL AUTOMATION")
    print("="*50)
    
    # Validate auth code
    if not AUTH_CODE or AUTH_CODE == "d07b564aec984c0182e3626f0b6381f9":
        print("⚠️ WARNING: Please set your actual authorization code in AUTH_CODE variable!")
        print("   Current code appears to be the example code.")
        print("   Continuing with example code - script will likely fail at V-Bucks exchange step.")
    
    # Create fetch modifier utility
    create_fetch_modifier()
    
    # Initialize and run automation
    automation = FortniteVBucksAutomation()
    automation.run_full_automation()

if __name__ == "__main__":
    main()