import threading
import http.server
import socketserver
import urllib.parse
import webbrowser
import json
import os
from CTkMessagebox import CTkMessagebox

class OAuthHandler:
    """
    Handles Google OAuth via Localhost Redirect.
    Restores the 'Sign in with Google' feature for Desktop.
    """
    
    server = None
    
    @staticmethod
    def initiate_google_login(parent):
        """Starts the local server and opens browser"""
        try:
            # 0. Kill existing server if any
            if OAuthHandler.server:
                try:
                    OAuthHandler.server.shutdown()
                    OAuthHandler.server.server_close()
                    OAuthHandler.server = None
                    parent.log("INFO", "Previous server instance verified stopped.")
                except Exception as e:
                     print(f"// Warning: Could not stop old server: {e}")

            # 1. Use Fixed Port 3000 (as seen in Supabase Config)
            port = 3000
            
            # Use EXACT URL from Supabase list if possible
            redirect_uri = f"http://localhost:{port}/auth-callback.html"
            
            # 2. Get Auth URL from Supabase
            if not parent.db_manager or not parent.db_manager.client:
                CTkMessagebox(title="Error", message="Database not connected.", icon="cancel")
                return

            # Explicitly request Google Auth URL with correct redirect_to parameter
            # NOTE: We must issue ONE call to avoid overwriting PKCE code verifier
            res = parent.db_manager.client.auth.sign_in_with_oauth({
                "provider": "google",
                "options": {
                    "redirectTo": redirect_uri
                }
            })
            
            auth_url = res.url if hasattr(res, 'url') else str(res)
            
            # FORCE APPEND redirect_to if missing (This fixes the Supabase ignoring it issue)
            # This is safer than making a second call because it preserves the PKCE verifier state
            if "redirect_to=" not in auth_url and "redirectTo=" not in auth_url:
                import urllib.parse
                # Check for query params existing
                separator = "&" if "?" in auth_url else "?"
                auth_url = f"{auth_url}{separator}redirect_to={urllib.parse.quote(redirect_uri)}"
            
            print(f"// DEBUG: Auth URL Generated: {auth_url}")
            
            # 3. Start Server Thread (Pass current language)
            lang = "ID"
            if hasattr(parent, 'translator') and parent.translator:
                lang = parent.translator.lang_code
                
            threading.Thread(target=OAuthHandler._start_server, args=(port, parent, lang), daemon=True).start()
            
            # 4. Open Browser
            webbrowser.open(auth_url)
            
        except Exception as e:
            parent.log("ERROR", f"Google Login Init Failed: {e}")
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    @staticmethod
    def _start_server(port, parent, lang="ID"):
        """Runs a temporary server to catch the callback"""
        
        # Localized strings for the browser page
        TEXTS = {
            "ID": {
                "success_title": "Login Berhasil | ITC",
                "success_header": "Login Berhasil!",
                "success_body": "Autentikasi selesai. Anda bisa menutup jendela ini sekarang dan kembali ke aplikasi.",
                "closing": "Menutup dalam",
                "seconds": "detik",
                "verifying_title": "Autentikasi | ITC",
                "verifying_header": "Memproses Login...",
                "verifying_body": "Mohon tunggu sebentar selagi kami mengalihkan Anda kembali ke aplikasi.",
                "waiting_header": "Menunggu...",
                "waiting_body": "Jika tidak terjadi apa-apa, silakan coba login kembali."
            },
            "EN": {
                "success_title": "Login Successful | ITC",
                "success_header": "Login Successful!",
                "success_body": "Authentication complete. You can close this window now and return to the application.",
                "closing": "Closing in",
                "seconds": "seconds",
                "verifying_title": "Authentication | ITC",
                "verifying_header": "Processing Login...",
                "verifying_body": "Please wait while we redirect you back to the application.",
                "waiting_header": "Waiting...",
                "waiting_body": "If nothing happens, please try to login again."
            }
        }
        
        t = TEXTS.get(lang, TEXTS["ID"])

        class CallbackHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                return # Silence logs
                
            def do_GET(self):
                # 1. Root: Handle PKCE Code Exchange or Serve JS
                parsed_path = urllib.parse.urlparse(self.path)
                
                # Check if path is root or our callback
                if parsed_path.path == "/" or parsed_path.path == "/auth-callback.html" or parsed_path.path == "/callback":
                    # Check for PKCE 'code' query param first
                    query = urllib.parse.parse_qs(parsed_path.query)
                    code = query.get('code', [None])[0]
                    
                    if code:
                        print(f"// PKCE Code Received: {code}")
                        # Immediately Exchange Code for Session
                        parent.after(100, lambda: OAuthHandler._exchange_pkce(parent, code))
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        
                        success_html = """
                        <!DOCTYPE html>
                        <html lang="id">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>{t[success_title]}</title>
                            <style>
                                :root {{ --primary: #4285F4; --success: #34A853; --danger: #EA4335; --bg: #0f172a; --card-bg: rgba(30, 41, 59, 0.85); }}
                                body {{ margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: radial-gradient(circle at center, #1e1b4b 0%, #0f172a 100%); color: #f8fafc; font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; }}
                                .bg-grid {{ position: fixed; top: -50%; left: -50%; width: 200%; height: 200%; background-image: linear-gradient(rgba(66, 133, 244, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(66, 133, 244, 0.05) 1px, transparent 1px); background-size: 40px 40px; transform: perspective(500px) rotateX(60deg); animation: moveGrid 20s linear infinite; z-index: -1; }}
                                @keyframes moveGrid {{ from {{ transform: perspective(500px) rotateX(60deg) translateY(0); }} to {{ transform: perspective(500px) rotateX(60deg) translateY(40px); }} }}
                                .container {{ text-align: center; padding: 3.5rem; background: var(--card-bg); backdrop-filter: blur(20px); border-radius: 32px; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 0 80px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(66, 133, 244, 0.1); max-width: 420px; width: 90%; animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1); position: relative; overflow: hidden; }}
                                @keyframes slideUp {{ from {{ opacity: 0; transform: translateY(40px); }} to {{ opacity: 1; transform: translateY(0); }} }}
                                .icon-wrapper {{ width: 90px; height: 90px; background: rgba(52, 168, 83, 0.15); border-radius: 28px; display: flex; justify-content: center; align-items: center; margin: 0 auto 2rem; color: var(--success); box-shadow: 0 0 30px rgba(52, 168, 83, 0.2); }}
                                .icon-error {{ background: rgba(234, 67, 53, 0.1); color: var(--danger); }}
                                h1 {{ font-size: 1.875rem; font-weight: 700; margin: 0 0 0.5rem; }}
                                p {{ color: #94a3b8; line-height: 1.6; margin-bottom: 2rem; }}
                                .itc-logo {{ font-weight: 800; font-size: 1.2rem; letter-spacing: 2px; color: #fff; margin-bottom: 2rem; display: block; opacity: 0.6; }}
                                .countdown {{ font-size: 0.875rem; color: #64748b; }}
                                .progress-bar {{ height: 4px; background: rgba(52, 168, 83, 0.1); width: 100%; position: absolute; bottom: 0; left: 0; }}
                                .progress-fill {{ height: 100%; background: var(--success); width: 100%; animation: drain 3s linear forwards; }}
                                @keyframes drain {{ from {{ width: 100%; }} to {{ width: 0%; }} }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <span class="itc-logo">ITC SYSTEM</span>
                                <div class="icon-wrapper">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                </div>
                                <h1>{t[success_header]}</h1>
                                <p>{t[success_body]}</p>
                                <div class="countdown">{t[closing]} <span id="timer">3</span> {t[seconds]}...</div>
                                <div class="progress-bar"><div class="progress-fill"></div></div>
                            </div>
                            <script>
                                let timeLeft = 3;
                                const timerElement = document.getElementById('timer');
                                const interval = setInterval(() => {{
                                    timeLeft--;
                                    if (timerElement) timerElement.innerText = timeLeft;
                                    if (timeLeft <= 0) {{ clearInterval(interval); window.close(); }}
                                }}, 1000);
                                setTimeout(() => {{ window.close(); }}, 3500);
                            </script>
                        </body>
                        </html>
                        """.format(t=t)
                        self.wfile.write(success_html.encode())
                        
                        # Stop Server
                        threading.Thread(target=self.server.shutdown, daemon=True).start()
                        return

                    # 2. Check for ERRORS from Supabase
                    error_msg = query.get('error', [None])[0]
                    if error_msg:
                        error_desc = query.get('error_description', ["Unknown error during authentication."])[0]
                        print(f"// [AUTH ERROR] Supabase returned: {error_msg} - {error_desc}")
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        
                        error_html = """
                        <!DOCTYPE html>
                        <html lang="id">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Error | ITC</title>
                            <style>
                                :root {{ --danger: #EA4335; --bg: #0f172a; --card-bg: rgba(30, 41, 59, 0.7); }}
                                body {{ margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); color: #f8fafc; font-family: sans-serif; }}
                                .container {{ text-align: center; padding: 3rem; background: var(--card-bg); backdrop-filter: blur(12px); border-radius: 24px; border: 1px solid rgba(234, 67, 53, 0.3); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); max-width: 400px; width: 90%; }}
                                .icon-wrapper {{ width: 80px; height: 80px; background: rgba(234, 67, 53, 0.1); border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto 1.5rem; color: var(--danger); }}
                                h1 {{ font-size: 1.875rem; font-weight: 700; margin: 0 0 0.5rem; }}
                                p {{ color: #94a3b8; line-height: 1.6; margin-bottom: 2rem; }}
                                .itc-logo {{ font-weight: 800; font-size: 1.2rem; letter-spacing: 2px; color: #fff; margin-bottom: 2rem; display: block; opacity: 0.6; }}
                                .btn {{ background: var(--danger); color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; text-decoration: none; font-weight: 600; display: inline-block; }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <span class="itc-logo">ITC SYSTEM</span>
                                <div class="icon-wrapper">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                                </div>
                                <h1>Autentikasi Gagal</h1>
                                <p>{desc}</p>
                                <a href="javascript:window.close()" class="btn">Tutup Jendela</a>
                            </div>
                        </body>
                        </html>
                        """.format(desc=error_desc)
                        self.wfile.write(error_html.encode())
                        return

                    # Only serve JS for Implicit Flow (fallback) if NO code
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    # HTML that grabs hash and sends it to /token
                    html = """
                    <!DOCTYPE html>
                    <html lang="id">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>{t[verifying_title]}</title>
                        <style>
                            :root {{ --primary: #4285F4; --bg: #0f172a; --card-bg: rgba(30, 41, 59, 0.7); }}
                            body {{ margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); color: #f8fafc; font-family: sans-serif; overflow: hidden; }}
                            .container {{ text-align: center; padding: 3rem; background: var(--card-bg); backdrop-filter: blur(12px); border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); max-width: 400px; width: 90%; animation: fadeIn 0.6s ease-out; }}
                            @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
                            .spinner {{ width: 50px; height: 50px; border: 3px solid rgba(255, 255, 255, 0.1); border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1.5rem; }}
                            @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
                            h2 {{ font-size: 1.5rem; font-weight: 700; margin: 0 0 0.5rem; }}
                            p {{ color: #94a3b8; line-height: 1.6; }}
                            .itc-logo {{ font-weight: 800; font-size: 1.2rem; border-bottom: 2px solid var(--primary); padding-bottom: 5px; margin-bottom: 2rem; display: inline-block; opacity: 0.8; }}
                        </style>
                    </head>
                    <body>
                        <div class="container" id="status-card">
                            <span class="itc-logo">ITC SYSTEM</span>
                            <div class="spinner" id="spinner"></div>
                            <h2 id="header">{t[verifying_header]}</h2>
                            <p id="subtext">{t[verifying_body]}</p>
                        </div>
                        <script>
                            const hash = window.location.hash.substring(1);
                            if(hash) {{
                                fetch('/token', {{
                                    method: 'POST',
                                    headers: {{'Content-Type': 'application/json'}},
                                    body: JSON.stringify({{hash: hash}})
                                }}).then(() => {{
                                    // Show Success State manually for implicit
                                    document.getElementById('spinner').style.display = 'none';
                                    document.getElementById('header').innerText = "{t[success_header]}";
                                    document.getElementById('subtext').innerText = "{t[success_body]}";
                                    setTimeout(window.close, 3000);
                                }}).catch(err => {{
                                    document.getElementById('spinner').style.display = 'none';
                                    document.getElementById('header').innerText = 'Error';
                                    document.getElementById('subtext').innerText = err;
                                }});
                            }} else {{
                               document.getElementById('header').innerText = "{t[waiting_header]}";
                               document.getElementById('subtext').innerText = "{t[waiting_body]}";
                            }}
                        </script>
                    </body>
                    </html>
                    """.format(t=t)
                    self.wfile.write(html.encode())
                    
                # 2. Token Handler
                elif self.path == "/token":
                   # This is irrelevant for GET usually, but fetch might use GET? No POST.
                   pass

            def do_POST(self):
                if self.path == '/token':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data)
                    hash_str = data.get('hash', '')
                    
                    # Parse Hash
                    params = urllib.parse.parse_qs(hash_str)
                    access_token = params.get('access_token', [None])[0]
                    refresh_token = params.get('refresh_token', [None])[0]
                    
                    if access_token:
                        parent.after(100, lambda: OAuthHandler._finalize_login(parent, access_token, refresh_token))
                        
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"OK")
                    
                    # Stop Server (in a thread to allow response to finish)
                    threading.Thread(target=self.server.shutdown, daemon=True).start()

        try:
            with socketserver.TCPServer(("127.0.0.1", port), CallbackHandler) as httpd:
                OAuthHandler.server = httpd
                print(f"// Local OAuth Server running on port {port}...")
                httpd.serve_forever()
        except Exception as e:
            print(f"Auth Server Error: {e}")

    @staticmethod
    def _exchange_pkce(parent, code):
        """Exchanges PKCE code for session"""
        try:
             parent.log("INFO", f"Exchanging PKCE Code: {code[:10]}...")
             res = parent.db_manager.client.auth.exchange_code_for_session({
                 "auth_code": code
             })
             
             if res.user:
                 parent.log("SUCCESS", f"Google Login Success: {res.user.email}")
                 
                 # Save Session
                 from dotenv import set_key
                 set_key(".env", "USER_AUTH_ID", res.user.id)
                 set_key(".env", "USER_EMAIL", res.user.email)
                 
                 # CRITICAL FIX: Force update DbManager state immediately
                 if hasattr(parent, 'db_manager') and parent.db_manager:
                     parent.db_manager.user_id = res.user.id
                     parent.db_manager.user_email = res.user.email
                     # Force re-fetch profile to correct the UI
                     try: parent.db_manager.get_user_profile(force=True)
                     except: pass
                 
                 # Reload UI
                 parent.show_main_interface()
        except Exception as e:
             parent.log("ERROR", f"PKCE Exchange Failed: {e}")
             CTkMessagebox(title="Login Error", message=f"Failed to exchange token: {e}", icon="cancel")

    @staticmethod
    def _finalize_login(parent, access_token, refresh_token):
        """Sets the session in Supabase Client"""
        try:
            parent.log("INFO", "Google Token Received. Setting Session...")
            res = parent.db_manager.client.auth.set_session(access_token, refresh_token)
            
            if res.user:
                 parent.log("SUCCESS", f"Google Login Success: {res.user.email}")
                 
                 # --- GHOST REGISTRATION ---
                 # Automatically sync profile data from Google Metadata
                 parent.db_manager.user_id = res.user.id
                 parent.db_manager.user_email = res.user.email
                 parent.db_manager.ensure_profile_exists()
                 
                 # Save Session
                 from dotenv import set_key
                 set_key(".env", "USER_AUTH_ID", res.user.id)
                 set_key(".env", "USER_EMAIL", res.user.email)
                 
                 # Reload UI
                 parent.show_main_interface()
            else:
                 parent.log("ERROR", "Session Set Failed")
                 
        except Exception as e:
            parent.log("ERROR", f"Finalize Error: {e}")
            CTkMessagebox(title="Error", message=f"Login Validation Failed: {e}", icon="cancel")
