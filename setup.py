#!/usr/bin/env python3
"""
Setup script pentru Fortnite V-Bucks Automation
Instalează dependențele și pregătește scriptul pentru rulare
"""

import os
import sys
import platform
import subprocess

def run_command(command):
    """Rulează o comandă și returnează rezultatul"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python_version():
    """Verifică versiunea Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ este necesar!")
        print(f"   Versiunea curentă: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def install_dependencies():
    """Instalează dependențele necesare"""
    print("\n📦 Instalez dependențele...")
    
    success, output = run_command("pip install -r requirements.txt")
    if success:
        print("✅ Dependențele au fost instalate cu succes!")
        return True
    else:
        print("❌ Eroare la instalarea dependențelor:")
        print(output)
        return False

def check_browser_profiles():
    """Verifică dacă profilurile browser există"""
    print("\n🌐 Verific profilurile browser...")
    
    if platform.system() == "Windows":
        username = os.getenv('USERNAME', 'User')
        edge_path = rf"C:\Users\{username}\AppData\Local\Microsoft\Edge\User Data"
        chrome_path = rf"C:\Users\{username}\AppData\Local\Google\Chrome\User Data"
        
        edge_exists = os.path.exists(edge_path)
        chrome_exists = os.path.exists(chrome_path)
        
        if edge_exists:
            print(f"✅ Edge profile găsit: {edge_path}")
        if chrome_exists:
            print(f"✅ Chrome profile găsit: {chrome_path}")
            
        if not edge_exists and not chrome_exists:
            print("⚠️  Nu am găsit profile Edge/Chrome")
            print("   Asigură-te că ai Edge sau Chrome instalat și configurat")
            return False
    else:
        print("ℹ️  Rulezi pe Linux/Mac - verifică manual path-urile profilurilor")
    
    return True

def main():
    """Funcția principală de setup"""
    print("🎮 FORTNITE V-BUCKS AUTOMATION - SETUP")
    print("=" * 50)
    
    # Verifică versiunea Python
    if not check_python_version():
        return False
    
    # Instalează dependențele
    if not install_dependencies():
        return False
    
    # Verifică profilurile browser
    check_browser_profiles()
    
    print("\n🚀 SETUP COMPLET!")
    print("\nCum să rulezi scriptul:")
    if platform.system() == "Windows":
        print("  python fortnite_vbucks_automation_windows.py")
    else:
        print("  python fortnite_vbucks_automation.py")
    
    print("\n📋 Checklist înainte de rulare:")
    print("  ✓ Browser (Edge/Chrome) logat cu contul Xbox")
    print("  ✓ Conexiune stabilă la internet")
    print("  ✓ Cont Epic Games legat de Xbox")
    print("  ✓ Tampermonkey instalat (opțional)")
    
    print("\n⚠️  IMPORTANT:")
    print("  - Utilizează doar cu contul tău personal")
    print("  - Respectă Terms of Service")
    print("  - Nu folosi în exces")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup întrerupt de utilizator")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Eroare în timpul setup-ului: {e}")
        sys.exit(1)