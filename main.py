import requests
import os
import json
import time

gift_rec = 'violence69.'

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

    # Check if 'access_token' key exists in the response data
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

        # Extract and print deviceId, accountId, and secret
        if 'deviceId' in device_auth_response_data:
            device_id = device_auth_response_data['deviceId']
            print("Device ID:", device_id)
        else:
            print("Device ID not found in deviceAuth response")
            return None, None
        if 'secret' in device_auth_response_data:
            secret = device_auth_response_data['secret']
            print("Secret:", secret)
        else:
            print("Secret not found in deviceAuth response")
            return None, None
        return device_id, secret
    return None, None

def update_config(account_id, device_id, secret):
    new_config = {
        "account_id": account_id,
        "device_id": device_id,
        "secret": secret
    }
    # Check if config file exists
    if os.path.exists('config.json'):
        with open('config.json', 'r') as file:
            existing_config = json.load(file)
        # Check if the accountId already exists in the existing config
        already_exists = False
        for config in existing_config:
            if config['account_id'] == new_config['account_id']:
                already_exists = True
                print("Account already in config")
                break
        if not already_exists:
            existing_config.append(new_config)
            with open('config.json', 'w') as file:
                json.dump(existing_config, file, indent=4)
                print("Added account to config")
    else:
        with open('config.json', 'w') as file:
            json.dump([new_config], file, indent=4)
            print("Added account to config")

def get_access_token_with_device_auth(device_id, account_id, secret):
    url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    headers = {
        "Authorization": "basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU=",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "device_auth",
        "device_id": device_id,
        "account_id": account_id,
        "secret": secret
    }

    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()

    if 'access_token' in response_data:
        return response_data['access_token']
    else:
        return None

def get_offers():
    url = "https://mewtwos.xyz/offers/shop"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch offers")
        return []

def get_display_name(access_token):
    url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/displayName/{gift_rec}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get('id', None)
    else:
        print("Failed to retrieve display name.")
        return None

def send_friend_request(account_id, access_token):
    friend_id = get_display_name(access_token)
    if friend_id:
        url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/friends/{friend_id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.post(url, headers=headers)
        return response.status_code == 200
    return False

def send_gift_request(account_id, access_token, offer_id, final_price, user_id):
    url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/GiftCatalogEntry?profileId=common_core"
    payload = {
        "offerId": offer_id,
        "currency": "MtxCurrency",
        "currencySubType": "",
        "expectedTotalPrice": final_price,
        "gameContext": "Frontend.CatabaScreen",
        "receiverAccountIds": [user_id],
        "giftWrapTemplateId": "",
        "personalMessage": ""
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print(f"[{account_id}] Sent cosmetic gift to {user_id}")
        return True
    else:
        print(f"[{account_id}] Failed to send gift to {user_id}")
        return False

def main():
    choice = input("""
Made & Developed by @caledb

[1] Add account to config

[2] Gift entire item-shop

[3] Send friend request

[4] Exchange BP Tokens

Choice: """)
    
    if choice == '1':
        access_token, account_id = get_access_token()
        if access_token and account_id:
            device_id, secret = get_device_info(access_token, account_id)
            if account_id and device_id and secret:
                update_config(account_id, device_id, secret)
        else:
            print("Failed to get access token or account ID")
            
    elif choice == '2':
        if os.path.exists('config.json'):
            with open('config.json', 'r') as file:
                account_data = json.load(file)

            while True:  # Infinite loop for continuous gifting
                for account_info in account_data:
                    device_id = account_info['device_id']
                    secret = account_info['secret']
                    account_id = account_info['account_id']
                    access_token = get_access_token_with_device_auth(device_id, account_id, secret)

                    if access_token:
                        display_name = get_display_name(access_token)
                        if display_name:
                            print(f"[{account_id}] Gift Receiver : {display_name}")
                            offers = get_offers()
                            for offer in offers:
                                offer_id = offer["offerId"]
                                final_price = offer["price"]
                                send_gift_request(account_id, access_token, offer_id, final_price, display_name)
                                time.sleep(1)
                        else:
                            print(f"[{account_id}] Failed to retrieve gift receiver id")
                    else:
                        print(f"[{account_id}] Failed to obtain access token")
                    
                    time.sleep(2)  # Small delay between accounts
                print("Completed one full cycle, starting over...")
        else:
            print("No accounts found in config.")
            
    elif choice == '3':
        if os.path.exists('config.json'):
            with open('config.json', 'r') as file:
                account_data = json.load(file)
            for account_info in account_data:
                device_id = account_info['device_id']
                secret = account_info['secret']
                account_id = account_info['account_id']
                access_token = get_access_token_with_device_auth(device_id, account_id, secret)
                if access_token:
                    if send_friend_request(account_id, access_token):
                        print(f"[{account_id}] Sent friend request to gift receiver")
                    else:
                        print(f"[{account_id}] Failed to send friend request")
                else:
                    print(f"Failed to obtain access token for {account_id}")
        else:
            print("No accounts found in config.")

    elif choice == '4':
        # Always ask for new authorization code for BP token exchange
        access_token, account_id = get_access_token()
        if access_token and account_id:
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
                    # Ask for new authorization code for next iteration
                    time.sleep(1)
                    print("\nGet new authorization code for next exchange...")
                    access_token, account_id = get_access_token()
                    if not access_token or not account_id:
                        print("Failed to get new authorization code, exiting...")
                        break
                else:
                    print("Failed to exchange BP token")
                    time.sleep(10)
                    break
        else:
            print("Failed to get initial access token")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()