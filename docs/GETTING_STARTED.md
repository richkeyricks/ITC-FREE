# Getting Started with ITC +AI Enterprise

Welcome to the institutional trading ecosystem. This guide will help you get your engine running in minutes.

## 1. Quick Installation
1.  **Download:** Grab the latest `ITC_Plus_AI_Enterprise_v1.0.1.zip` from the [Releases](https://github.com/richkeyricks/ITC/releases) page.
2.  **Extract:** Unzip the contents to a dedicated folder (e.g., `C:\Trading\ITC`).
3.  **Launch:** Double-click `ITC_Plus_AI_Enterprise.exe`.

## 2. Configuration (The .env Setup)
The engine requires a `.env` file to store your credentials securely. 
1. Open the `.env` template in a text editor (Notepad++ recommended).
2. Enter your **Telegram API ID** and **Hash** (Get them from [my.telegram.org](https://my.telegram.org)).
3. Enter your **MT5 Account Details**.
4. Save and restart the application.

## 3. Connecting to Channels
- Ensure the channels you wish to monitor are listed in the `TG_CHANNELS` variable (using Channel IDs).
- Use the **Mission Control** tab in the GUI to verify signal parsing.

## 4. Pro Tips
- **Low Latency:** Run the `.exe` on a VPS (Virtual Private Server) for 24/7 uptime and sub-50ms execution.
- **AI Toggle:** If you have an OpenRouter or Gemini API key, enable `USE_AI=True` for hybrid neural parsing.

---
*For detailed troubleshooting, refer to the [FAQ](FAQ.md).*
