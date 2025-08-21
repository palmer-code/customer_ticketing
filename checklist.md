Quick checklist (Windows Surface Book as server)
Install Python 3.8+ and required packages:

pip install flask pyttsx3 pywin32
Install & set up your thermal printer driver in Windows and set it as the Default Printer (or note its exact name).

Connect speakers and test sound in Windows Sound Settings.

Put the Surface Book on the switch and give it a static LAN IP (recommended: e.g. 192.168.0.100).

Make sure operator PCs are on the same subnet and can ping the Surface Book (ping 192.168.0.100).

Allow incoming connections to the Flask port (default 5000) in Windows Firewall so operator PCs can reach the server.

Run the Flask app: python app.py (or create a service/shortcut for automatic start).

Detailed Windows steps & commands
1) Find & set a static IP
To find current IP: open Command Prompt and run:

ipconfig
Note the Ethernet adapter IPv4 address (e.g. 192.168.0.105).

To assign a static IP (recommended via Windows GUI):

Settings → Network & Internet → Ethernet → Change adapter options → Right-click adapter → Properties → Internet Protocol Version 4 (TCP/IPv4) → Properties → Use the following IP address.

Example values:

IP address: 192.168.0.100

Subnet mask: 255.255.255.0

Default gateway: your router (e.g., 192.168.0.1) — not strictly required on isolated LAN but OK to set.

DNS: can be router or public DNS.

2) Allow Flask port through Windows Firewall
Open an admin PowerShell or CMD and run (for port 5000):

netsh advfirewall firewall add rule name="QueueServer5000" dir=in action=allow protocol=TCP localport=5000
If you prefer to allow Python executable:



netsh advfirewall firewall add rule name="PythonServer" dir=in action=allow program="%LOCALAPPDATA%\Programs\Python\Python39\python.exe" enable=yes
(Adjust path to your Python executable.)

3) Test connectivity from operator PC
On operator PC open CMD and:
ping 192.168.0.100
In a browser (operator PC): http://192.168.0.100:5000/operator/1

If you see the operator page, networking and firewall are OK.

4) Make Flask run on startup (two options)
A. Quick & easy — create a .bat and place it in Startup:

run_server.bat:
cd C:\path\to\queue_system
python app.py
Put a shortcut to that .bat in %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup.

B. Robust (recommended for production) — install as a Windows service:

Use a tool like NSSM (Non-Sucking Service Manager) to wrap python.exe app.py into a service so it starts even when no one logs in.

5) Kiosk-mode for the Surface Book (customer screen fullscreen)
Use Microsoft Edge kiosk mode (Assigned access) or launch Chrome/Edge in kiosk:

Chrome:
chrome.exe --kiosk --app=http://localhost:5000/kiosk
Edge (Chromium):
msedge.exe --kiosk http://localhost:5000/kiosk --edge-kiosk-type=fullscreen
For an unattended kiosk, set up Windows Auto-Login and put the kiosk browser in Startup.

6) Printer & TTS testing
Printing: run a small Python snippet to print sample text via win32print to ensure encoding and printer driver work.

TTS: open a Python REPL and:

import pyttsx3
t = pyttsx3.init()
t.say("This is a test")
t.runAndWait()
Confirm it plays via the Surface Book speakers.

7) Optional: make server accessible only on LAN
We used app.run(host="0.0.0.0", port=5000) in app.py. That binds to all interfaces on the Surface Book but only LAN devices can reach it because of firewall & lack of NAT from outside (unless you expose it).

Common pitfalls & fixes
Operator PCs can't reach server: check static IP, switch cabling, firewall rules, and that Flask is running.

Printer prints gibberish: ensure correct encoding and that you're sending raw text compatible with the printer driver; some thermal printers need ESC/POS commands.

TTS silent: check default audio output device, and volume/mute settings for the Windows user account running the Flask app (services may run under SYSTEM which may not have audio access — run as a normal user if you need audio).

App runs but not on startup: verify the Startup shortcut path or use NSSM to create a service.
