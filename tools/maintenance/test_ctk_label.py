
import customtkinter as ctk

try:
    app = ctk.CTk()
    lbl = ctk.CTkLabel(app, text="Test", text_color="#ffffff")
    print("CTkLabel accepts text_color: YES")
except Exception as e:
    print(f"CTkLabel accepts text_color: NO - Error: {e}")

try:
    frame = ctk.CTkFrame(app, text_color="#ffffff")
    print("CTkFrame accepts text_color: YES")
except Exception as e:
    print(f"CTkFrame accepts text_color: NO - Error: {e}")
