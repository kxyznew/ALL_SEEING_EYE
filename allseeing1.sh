#!/bin/bash
# PRESIDENTIAL_ALL_SEEING.sh - v1.0 FINAL
# 🔒 LOCKED: THE COMPLETE ADB TAP
# 🧠 Designed for: Full passive mobile situational awareness via USB (no rooting assumptions, but enhanced if rooted)

echo "=== 🟡 PRESIDENTIAL :: ULTIMATE ANDROID INTELLIGENCE TAP 🟡 ==="
echo "[*] Starting data retrieval... Hold tight."

## 0. VERIFY DEVICE CONNECTION
adb get-state 1>/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "[!] No ADB device connected or unauthorized."
  exit 1
fi

echo "[+] Device Connected: $(adb shell getprop ro.product.model)"

## 1. BASIC INFO
echo -e "\n[+] SYSTEM INFO"
adb shell getprop ro.product.manufacturer
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release
adb shell getprop gsm.version.baseband
adb shell uptime

## 2. NETWORK OPERATORS AND IDENTIFIERS
echo -e "\n[+] NETWORK & CARRIER INFO"
adb shell getprop gsm.operator.alpha
adb shell getprop gsm.operator.numeric
adb shell getprop gsm.sim.operator.numeric
adb shell getprop gsm.sim.operator.alpha
adb shell getprop telephony.lteOnCdmaDevice

## 3. CELLULAR / RADIO DATA
echo -e "\n[+] SIGNAL STRENGTH + CELL LOCATION"
adb shell dumpsys telephony.registry | grep -i -E "mSignalStrength|mCellLocation|mServiceState"

## 4. NEIGHBORING CELLS (May not work on all Android versions)
echo -e "\n[+] NEIGHBORING CELL INFO"
adb shell dumpsys telephony.registry | grep -i neighbor

## 5. IP & INTERFACES
echo -e "\n[+] NETWORK INTERFACES"
adb shell ip addr show
adb shell netstat

## 6. SMS MESSAGES
echo -e "\n[+] SMS INBOX"
adb shell content query --uri content://sms/inbox --projection "address,date,body" --sort "date DESC" 2>/dev/null

echo -e "\n[+] SMS SENT"
adb shell content query --uri content://sms/sent --projection "address,date,body" --sort "date DESC" 2>/dev/null

## 7. CALL LOGS
echo -e "\n[+] CALL HISTORY"
adb shell content query --uri content://call_log/calls --projection "number,date,duration,type,name" --sort "date DESC" 2>/dev/null

## 8. CONTACTS
echo -e "\n[+] CONTACTS"
adb shell content query --uri content://contacts/phones/ --projection "display_name,number" 2>/dev/null

## 9. CONNECTED WIFI
echo -e "\n[+] CONNECTED WIFI INFO"
adb shell dumpsys wifi | grep -i "SSID\|BSSID\|RSSI\|Link speed"

## 10. APP INVENTORY
echo -e "\n[+] INSTALLED APPS (User + System)"
adb shell pm list packages -f

## 11. RECENTLY USED APPS (If usage stats are exposed)
echo -e "\n[+] RECENT APP USAGE"
adb shell dumpsys usagestats | grep -A 10 "PackageUsageStats"

## 12. LOCATION SERVICES
echo -e "\n[+] LOCATION SERVICES STATUS"
adb shell settings get secure location_providers_allowed
adb shell settings get secure location_mode

## 13. ACTIVE SENSORS (Gyro, Accel, etc.)
echo -e "\n[+] ACTIVE SENSORS"
adb shell dumpsys sensorservice | grep -i "active\|sensor\|name"

## 14. LIVE LOGCAT (Short burst)
echo -e "\n[+] LIVE LOGCAT SNAPSHOT (20 lines)"
adb logcat -d | tail -n 20

## 15. RECENT FILESYSTEM MODIFICATIONS (requires shell access)
echo -e "\n[+] RECENT FILE ACCESS (DCIM, Downloads, WhatsApp if present)"
adb shell ls -lt /sdcard/DCIM | head
adb shell ls -lt /sdcard/Download | head
adb shell ls -lt /sdcard/WhatsApp/Media/WhatsApp\ Images/ | head

## 16. RUNNING PROCESSES
echo -e "\n[+] CURRENT RUNNING PROCESSES"
adb shell ps -A | head -n 20

echo -e "\n=== ✅ PRESIDENTIAL SCAN COMPLETE ==="
