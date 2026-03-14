# ⚡ Bolt's High-Speed Command Line (SSH) Guide for Termius

This guide fixes the Protocol Mismatch (Port 3389/RDP vs Port 22/SSH) issue and sets up your mobile device for lightning-fast, zero-lag command line access to your Windows 11 machine (`192.168.1.10`).

## 🛠️ Step 1: Prepare the Windows 11 Laptop
1. Open an Administrator PowerShell window.
2. Run the provided setup script:
   ```powershell
   .\windows-setup\scripts\setup-mobile-ssh.ps1
   ```
3. This will install the OpenSSH server, configure the firewall, and prepare the `authorized_keys` file for the user `NUNA`.

## 📱 Step 2: Generate an SSH Key in Termius (Mobile)
1. Open **Termius** on your phone.
2. Go to the **Keychain** tab.
3. Tap the **+** button and select **Generate Key**.
4. Name the key (e.g., `Laptop-SSH-Key`).
5. Tap **Save**.
6. Once the key is generated, tap on it in the list, then tap **Copy Public Key**.

## 🤝 Step 3: Pair the Devices
1. You need to get the Public Key from your phone to your laptop. You can send it via email, a secure message, or Google Drive.
2. On your Windows 11 laptop, navigate to: `C:\Users\NUNA\.ssh\`
3. Open the `authorized_keys` file with Notepad (or your preferred editor).
4. Paste the copied Public Key onto a new line and save the file.

## 🚀 Step 4: Configure the Termius Connection
1. In Termius, go back to the **Hosts** tab.
2. Tap the connection you previously set up for `192.168.1.10`, or create a new one.
3. Apply the following settings:
   - **Alias:** Laptop SSH (or similar)
   - **Hostname/IP:** `192.168.1.10`
   - **Port:** `22` (Crucial: Change this from 3389)
   - **Username:** `NUNA`
   - **Password:** Leave blank!
   - **Keys:** Select the key you generated in Step 2 (`Laptop-SSH-Key`).
4. Tap the checkmark to **Save**.

## 🔋 Termius Performance Hardening (Optional but Recommended)
With your POVA 6 Pro's 12.00 GB + 12.00 GB RAM, you should maximize the Terminal experience:
- **Keep Awake:** Go to Termius Settings -> Terminal -> enable "Keep screen on" and "Terminal Bell."
- **Font Scaling:** In the Terminal settings, set the font size to `12pt`. With your `1080x2436` resolution, this maximizes screen real estate, making it feel like a 13-inch laptop.

## ✅ Final Check
When you tap the connection in Termius, it should securely handshake using the SSH key and instantly drop you into the command line of your Windows 11 machine, ready to run your Python mapping scripts or manage the "Hot Melting Iron" system!
