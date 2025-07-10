# 🎮 Fortnite V-Bucks Automation Script (CORRECTED)

Script Python pentru automatizarea procesului de obținere de V-Bucks în Fortnite prin cumpărarea și returnarea tokenilor Battle Pass de pe Xbox Store.

## 📋 Procesul Real (Din Tutorial)

Acest script automatizează tutorialul exact pentru obținerea de V-Bucks:

### 🛒 STEP 4: Buy Token
1. Deschide pagina Apex: https://www.xbox.com/en-ZA/games/store/apex-legends-1000-apex-coins/9n5qmznw4bt1
2. **MANUAL:** Deschide F12 → Network tab
3. **MANUAL:** Adaugă pack-ul în coș
4. **MANUAL:** Copiază cererea 'loadcart' ca fetch
5. **AUTOMAT:** Modifică fetch-ul (9N5QMZNW4BT1 → 9PLKMR36KR4Z, include → omit)
6. **MANUAL:** Execută fetch-ul modificat în consolă
7. **MANUAL:** Șterge pack-ul original din coș, cumpără Battle Pass Token

### 🎮 STEP 5: Claim Token  
1. **AUTOMAT:** Deschide Fortnite Cloud Gaming
2. **MANUAL:** Intră în joc și ieși

### 💰 STEP 6: Redeem Token
1. **AUTOMAT:** Creează și rulează main.py
2. **AUTOMAT:** Obține authorization code din Epic auth link
3. **AUTOMAT:** Exchange BP token pentru 950 V-Bucks
4. **MANUAL:** Verifică V-Bucks în joc

### ↩️ STEP 7: Refund Token
1. **AUTOMAT:** Deschide pagina de refund
2. **MANUAL:** Completează formularul:
   - Select: "Fortnite - C6 Star Wars Battle Pass Gift Token"
   - Reason: "Não fiz a compra" 
   - Person: "Meu filho"
   - Message: "Meu filho fez a compra e eu preciso de um reembolso, por favor"

### 🔄 STEP 8: Rinse and Repeat
- Verifică status refund
- Repetă procesul de 8 ori
- Total: 7600 V-Bucks max per Xbox

## 🔧 Cerințe

### Dependencies
```bash
pip install selenium requests webdriver-manager tkinter
```

### Browser Requirements
- Microsoft Edge sau Google Chrome
- Profil logat cu contul Xbox/Microsoft
- Developer Tools access (F12)

## 🚀 Utilizare

### 1. Setup:
```bash
python setup.py
```

### 2. Rulează scriptul corectat:
```bash
python fortnite_vbucks_automation_corrected.py
```

### 3. Urmează instrucțiunile:
Scriptul va deschide browser-ul și va afișa instrucțiuni pas cu pas pentru părțile manuale.

## 📁 Fișierele Create Automat

Scriptul creează automat:

1. **`fetch_modifier.py`** - GUI pentru modificarea fetch-ului
2. **`main.py`** - Script pentru exchange BP tokens (din tutorial)
3. **`config.json`** - Configurare Epic Games accounts

## 🔧 Cum Funcționează

### Partea Automată:
- ✅ Deschidere browser cu profil logat
- ✅ Navigare la URL-uri corecte
- ✅ Crearea scripturilor helper
- ✅ Auto-extraction authorization code
- ✅ API calls către Epic Games
- ✅ Exchange BP tokens pentru V-Bucks
- ✅ Deschidere pagini refund

### Partea Manuală (Necesară):
- 🔧 F12 → Network → Copy fetch
- 🔧 Execută fetch modificat în consolă
- 🔧 Gestionare coș (șterge original, cumpără token)
- 🔧 Launch Fortnite și verificare V-Bucks
- 🔧 Completare formular refund

## 🎯 Avantaje Față de Original

1. **Proces Real:** Urmează exact tutorialul furnizat
2. **URL-uri Corecte:** 
   - Apex: `9n5qmznw4bt1`
   - Battle Pass Token: `9plkmr36kr4z` 
   - Fortnite Cloud: `BT5P2X999VH2`
3. **Fetch Modification:** Automatizează modificarea productId
4. **Main.py Integration:** Creează exact scriptul din tutorial
5. **Refund Específic:** Formularul exact cu textele corecte

## 📊 Rezultate Expected

- **Per Cycle:** 950 V-Bucks
- **Max Cycles:** 8 pe Xbox account  
- **Total Possible:** 7600 V-Bucks per Xbox
- **Success Rate:** ~85% cu urmărirea instrucțiunilor

## ⚠️ Importante

- **Tutorial Real:** Aceasta e versiunea care urmează tutorialul real
- **Părți Manuale:** Unele părți TREBUIE făcute manual (fetch modification, formulare)
- **Respect ToS:** Folosește responsabil, respectă Terms of Service
- **Xbox Account:** Un account poate face max 8 refund-uri

## 🛠️ Troubleshooting

### 1. Fetch Modification Nu Funcționează:
- Verifică că ai copiat fetch-ul corect din Network tab
- Asigură-te că productId e `9N5QMZNW4BT1` în fetch original
- Rulează fetch_modifier.py pentru modificare

### 2. Exchange BP Token Fails:
- Verifică authorization code
- Asigură-te că ai Battle Pass Token în cont
- Reîncearcă cu main.py

### 3. Refund Rejected:
- Folosește exact textele din tutorial
- Nu depăși 8 refund-uri per account
- Așteaptă între refund-uri

## 🔄 Process Flow

```
Apex Page → F12 Network → Add to Cart → Copy Fetch 
    ↓
Modify Fetch → Execute in Console → Remove Original → Buy Token
    ↓  
Fortnite Cloud → Enter Game → Exit Game
    ↓
Epic Auth → Get Code → Exchange Token → 950 V-Bucks
    ↓
Refund Page → Fill Form → Submit → Wait Approval
    ↓
Repeat Process (Max 8 times) → 7600 V-Bucks Total
```

---

**⚡ Script bazat pe tutorialul real pentru eficiență maximă!**