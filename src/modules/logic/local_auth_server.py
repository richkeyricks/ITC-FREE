# src/modules/logic/local_auth_server.py
"""
Local HTTP Server for OAuth Callback
Handles Google OAuth callback on localhost to preserve PKCE code_verifier.

Flow:
1. App starts local server on random port
2. OAuth redirect URL is http://localhost:PORT/callback
3. User completes Google OAuth
4. Browser redirects to localhost with code/tokens
5. SAME app instance handles callback (code_verifier preserved)
6. Authentication completes, server stops
"""
import http.server
import socketserver
import threading
import webbrowser
import os
from urllib.parse import urlparse, parse_qs


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    """HTTP Request Handler for OAuth Callbacks"""
    
    # Shared callback data
    auth_data = None
    server_ready = threading.Event()
    auth_complete = threading.Event()
    
    def log_message(self, format, *args):
        """Suppress default logging to keep console clean"""
        pass
    
    def do_GET(self):
        """Handle GET requests (OAuth callback)"""
        try:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            # Check for OAuth code or error
            code = params.get('code', [None])[0]
            error = params.get('error', [None])[0]
            error_description = params.get('error_description', ['Unknown error'])[0]
            
            if code:
                # Store the code for the main app to use
                OAuthCallbackHandler.auth_data = {"code": code, "success": True}
                self._send_success_response()
            elif error:
                OAuthCallbackHandler.auth_data = {
                    "success": False, 
                    "error": error,
                    "error_description": error_description
                }
                self._send_error_response(error_description)
            else:
                # Check for tokens in fragment (implicit flow)
                # Note: Fragment (#) is not sent to server, so we need a different approach
                # For now, assume PKCE flow with code
                self._send_waiting_response()
                return
            
            # Signal that authentication is complete
            OAuthCallbackHandler.auth_complete.set()
            
        except Exception as e:
            print(f"// OAuth Callback Error: {e}")
            self._send_error_response(str(e))
    
    def _send_success_response(self):
        """Send success HTML page"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Login Berhasil!</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    color: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .card {
                    background: rgba(255,255,255,0.1);
                    padding: 40px 60px;
                    border-radius: 20px;
                    text-align: center;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.2);
                }
                .success-icon { font-size: 64px; margin-bottom: 20px; }
                h1 { color: #4ade80; margin-bottom: 10px; }
                p { color: #94a3b8; margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="success-icon">✅</div>
                <h1>Login Berhasil!</h1>
                <p>Kembali ke aplikasi ITC +AI...</p>
                <p style="font-size: 12px;">Anda dapat menutup tab ini.</p>
            </div>
            <script>
                // Auto-close after 2 seconds
                setTimeout(() => { window.close(); }, 2000);
            </script>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def _send_error_response(self, error_msg):
        """Send error HTML page"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Login Gagal</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    color: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .card {{
                    background: rgba(255,255,255,0.1);
                    padding: 40px 60px;
                    border-radius: 20px;
                    text-align: center;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.2);
                }}
                .error-icon {{ font-size: 64px; margin-bottom: 20px; }}
                h1 {{ color: #f87171; margin-bottom: 10px; }}
                p {{ color: #94a3b8; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="error-icon">❌</div>
                <h1>Login Gagal</h1>
                <p>{error_msg}</p>
                <p style="font-size: 12px;">Silakan coba lagi dari aplikasi.</p>
            </div>
        </body>
        </html>
        """
        self.send_response(200)  # Still 200 so browser displays the page
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def _send_waiting_response(self):
        """Send waiting HTML page (for fragment handling)"""
        html = """
        <!DOCTYPE html>
        <html><head><title>Processing...</title></head>
        <body><p>Processing authentication...</p></body></html>
        """
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


class LocalAuthServer:
    """
    Manages a local HTTP server for OAuth callbacks.
    Ensures the same app instance handles the callback to preserve PKCE code_verifier.
    """
    
    DEFAULT_PORT = 8765
    
    def __init__(self, port=None):
        self.port = port or self.DEFAULT_PORT
        self.server = None
        self.server_thread = None
        self._running = False
    
    def get_callback_url(self):
        """Returns the OAuth callback URL for localhost"""
        return f"http://localhost:{self.port}/callback"
    
    def start(self):
        """Start the local auth server in a background thread"""
        try:
            # Reset state
            OAuthCallbackHandler.auth_data = None
            OAuthCallbackHandler.auth_complete.clear()
            
            # Create server with SO_REUSEADDR to avoid "address already in use" errors
            socketserver.TCPServer.allow_reuse_address = True
            self.server = socketserver.TCPServer(("127.0.0.1", self.port), OAuthCallbackHandler)
            
            # Run server in background thread
            self.server_thread = threading.Thread(target=self._serve, daemon=True)
            self.server_thread.start()
            self._running = True
            
            print(f"// Local Auth Server started on port {self.port}")
            return True
            
        except OSError as e:
            if "address already in use" in str(e).lower():
                # Try next port
                self.port += 1
                return self.start()
            print(f"// Failed to start auth server: {e}")
            return False
        except Exception as e:
            print(f"// Auth Server Error: {e}")
            return False
    
    def _serve(self):
        """Server loop (runs in background thread)"""
        try:
            self.server.serve_forever()
        except Exception as e:
            if self._running:  # Only log if not intentionally stopped
                print(f"// Auth Server stopped unexpectedly: {e}")
    
    def wait_for_auth(self, timeout=300):
        """
        Wait for authentication to complete.
        Returns: dict with 'success' and 'code' or 'error'
        """
        completed = OAuthCallbackHandler.auth_complete.wait(timeout=timeout)
        
        if completed and OAuthCallbackHandler.auth_data:
            return OAuthCallbackHandler.auth_data
        else:
            return {"success": False, "error": "timeout", "error_description": "Authentication timed out"}
    
    def stop(self):
        """Stop the local auth server"""
        self._running = False
        if self.server:
            try:
                self.server.shutdown()
                self.server.server_close()
                print("// Local Auth Server stopped")
            except:
                pass
        self.server = None
        self.server_thread = None


# Singleton instance for easy access
_auth_server = None

def get_auth_server():
    """Get or create the singleton auth server instance"""
    global _auth_server
    if _auth_server is None:
        _auth_server = LocalAuthServer()
    return _auth_server
