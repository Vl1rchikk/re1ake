from customtkinter import * #неререрреререререрререререререр отпрака блблбл
from socket import *
import threading

init_nickname = "User (change yr nick)"
init_font_family = "Arial"
init_font_size = 16
init_is_bold = False
init_theme = "Dark"

setup_window = CTk()
setup_window.title("logigram - Налаштування")
setup_window.geometry("380x420")
set_appearance_mode("Dark")
set_default_color_theme("blue")

lbl_welcome = CTkLabel(setup_window, text="Давайте почнемо!", font=CTkFont(size=20, weight="bold"))
lbl_welcome.pack(pady=10)

lbl_subtitle = CTkLabel(setup_window, text="Налаштуйте все під себе перед входом", font=CTkFont(size=12), text_color="gray")
lbl_subtitle.pack(pady=(0, 10))

lbl_s_nick = CTkLabel(setup_window, text="Нікнейм:")
lbl_s_nick.pack(anchor="w", padx=30)
entry_s_nick = CTkEntry(setup_window, width=320)
entry_s_nick.insert(0, init_nickname)
entry_s_nick.pack(pady=5)

lbl_s_font = CTkLabel(setup_window, text="Шрифт:")
lbl_s_font.pack(anchor="w", padx=30)
menu_s_font = CTkOptionMenu(setup_window, values=["Arial", "Calibri", "Tahoma", "Verdana"], width=320)
menu_s_font.set(init_font_family)
menu_s_font.pack(pady=5)

lbl_s_size = CTkLabel(setup_window, text="Розмір шрифту:")
lbl_s_size.pack(anchor="w", padx=30)
menu_s_size = CTkOptionMenu(setup_window, values=["12", "14", "16", "18", "20", "22"], width=320)
menu_s_size.set(str(init_font_size))
menu_s_size.pack(pady=5)

lbl_s_theme = CTkLabel(setup_window, text="Тема:")
lbl_s_theme.pack(anchor="w", padx=30)
menu_s_theme = CTkOptionMenu(setup_window, values=["Dark", "Light"], command=lambda t: set_appearance_mode(t), width=320)
menu_s_theme.set(init_theme)
menu_s_theme.pack(pady=5)

def start_chat():
    global init_nickname, init_font_family, init_font_size, init_theme
    init_nickname = entry_s_nick.get().strip() or "Анонім"
    init_font_family = menu_s_font.get()
    init_font_size = int(menu_s_size.get())
    
    setup_window.quit()    
    setup_window.destroy() 

btn_start = CTkButton(setup_window, text="Почати чат", width=320, fg_color="#2ECC71", hover_color="#27AE60", command=start_chat)
btn_start.pack(pady=15)

setup_window.mainloop()

client_socket = socket(AF_INET, SOCK_STREAM)
is_connected = False
HOST = "localhost" #================ PORT HOST ======================
PORT = 22

try:
    client_socket.connect((HOST, PORT))
    print("ты на серваке")
    is_connected = True
except:
    print("не смог")
    is_connected = False

window = CTk()
window.title("logigram")
window.geometry("580x420") 

menu_open = False
text_settings_open = False
MENU_WIDTH = 175

user_nickname = init_nickname
current_font_family = init_font_family
current_font_size = init_font_size
is_bold = init_is_bold

def receive_messages():
    global is_connected
    while is_connected:
        try:
            message = client_socket.recv(4096)
            if not message:
                is_connected = False
                window.after(0, update_status_ui)
                break
            message = message.decode()
            window.after(0, lambda m=message: add_message(m, align="left"))
        except:
            print("З'єднання з сервером розірвано")
            is_connected = False
            window.after(0, update_status_ui)
            break

def ShowLeftMenu():
    global menu_open
    menu_open = not menu_open
    if menu_open:
        btn_menu.configure(text="◀")
    else:
        btn_menu.configure(text="▶")
    adaptive_ui()

def toggle_text_settings():
    global text_settings_open
    text_settings_open = not text_settings_open
    if text_settings_open:
        text_settings_frame.pack(after=btn_text_settings, padx=10, pady=(0, 5), anchor="w")
        btn_text_settings.configure(text="▲ Налаштування тексту")
    else:
        text_settings_frame.pack_forget()
        btn_text_settings.configure(text="▼ Налаштування тексту")

def toggle_theme():
    if get_appearance_mode() == "Dark":
        set_appearance_mode("Light")
        btn_theme.configure(text="🌙 Темна")
    else:
        set_appearance_mode("Dark")
        btn_theme.configure(text="☀️ Світла")

def update_nickname(event=None):
    global user_nickname
    user_nickname = entry_nick.get().strip() or "Анонім"

def change_font_family(choice):
    global current_font_family
    current_font_family = choice
    update_input_font()

def change_font_size(choice):
    global current_font_size
    current_font_size = int(choice)
    update_input_font()

def toggle_bold():
    global is_bold
    is_bold = not is_bold
    update_input_font()

def update_input_font():
    weight_val = "bold" if is_bold else "normal"
    new_font = CTkFont(family=current_font_family, size=current_font_size, weight=weight_val)
    message_entry.configure(font=new_font)

def update_status_ui():
    if is_connected:
        lbl_status.configure(text="Статус: Підключено", text_color="#2ECC71")
    else:
        lbl_status.configure(text="Статус: Відключено", text_color="#E74C3C")

def clear_chat():
    for widget in chat.winfo_children():
        widget.destroy()
    add_message("Історія чату очищена", align="left")

def send_quick_emoji(emoji):
    message_entry.delete(0, "end")
    message_entry.insert(0, emoji)
    sendMsg()

# --- БОКОВОЕ МЕНЮ ---
left_menu = CTkFrame(window, width=MENU_WIDTH, corner_radius=0)

lbl_nick = CTkLabel(left_menu, text="Нікнейм")
lbl_nick.pack(anchor="w", padx=10, pady=(10, 2))

entry_nick = CTkEntry(left_menu, width=155, placeholder_text="...")
entry_nick.insert(0, user_nickname)
entry_nick.pack(padx=10, pady=(0, 10))
entry_nick.bind("<KeyRelease>", update_nickname)

# Кнопка настройки текста
btn_text_settings = CTkButton(left_menu, text="▼ Налаштування тексту", width=155, command=toggle_text_settings)
btn_text_settings.pack(padx=10, pady=(0, 5))

# Блок настроек текста (скрыт по умолчанию)
text_settings_frame = CTkFrame(left_menu, width=155, fg_color="transparent")

lbl_font_fam = CTkLabel(text_settings_frame, text="Шрифт:", font=CTkFont(size=12))
lbl_font_fam.pack(anchor="w", padx=2, pady=(0, 2))
font_menu = CTkOptionMenu(text_settings_frame, values=["Arial", "Calibri", "Tahoma", "Verdana"], command=change_font_family, width=155)
font_menu.set(current_font_family)
font_menu.pack(pady=(0, 5))

lbl_font_sz = CTkLabel(text_settings_frame, text="Розмір:", font=CTkFont(size=12))
lbl_font_sz.pack(anchor="w", padx=2, pady=(0, 2))
size_menu = CTkOptionMenu(text_settings_frame, values=["12", "14", "16", "18", "20", "22"], command=change_font_size, width=155)
size_menu.set(str(current_font_size))
size_menu.pack(pady=(0, 5))

btn_bold = CTkButton(text_settings_frame, text="Жирний: Викл", width=155, fg_color="#444444", hover_color="#555555", command=lambda: [toggle_bold(), btn_bold.configure(text=f"Жирний: {'Вкл' if is_bold else 'Викл'}", fg_color="#2980B9" if is_bold else "#444444")])
btn_bold.pack(pady=(0, 5))

btn_theme = CTkButton(left_menu, text="☀️ Світла" if get_appearance_mode()=="Dark" else "🌙 Темна", width=155, command=toggle_theme)
btn_theme.pack(padx=10, pady=5)

lbl_status = CTkLabel(
    left_menu, 
    text="Статус: Підключено" if is_connected else "Статус: Відключено", 
    text_color="#2ECC71" if is_connected else "#E74C3C", 
    font=CTkFont(size=12, weight="bold")
)
lbl_status.pack(anchor="w", padx=10, pady=5)

btn_clear = CTkButton(left_menu, text="🗑️ Очистити чат", width=155, fg_color="#C0392B", hover_color="#962D22", command=clear_chat)
btn_clear.pack(padx=10, pady=5)

lbl_emojis = CTkLabel(left_menu, text="Швидкі емодзі:")
lbl_emojis.pack(anchor="w", padx=10, pady=(5, 2))

emoji_frame = CTkFrame(left_menu, fg_color="transparent")
emoji_frame.pack(padx=10, pady=(0, 10))

emojis = ["👍", "🔥", "😂", "❤️"]
for i, em in enumerate(emojis):
    btn_em = CTkButton(emoji_frame, text=em, width=32, height=30, command=lambda e=em: send_quick_emoji(e))
    btn_em.grid(row=0, column=i, padx=1)

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
btn_menu = CTkButton(window, width=30, text="▶", command=ShowLeftMenu)
chat = CTkScrollableFrame(window, width=335, height=250)

def scroll_to_bottom():
    try:
        chat._parent_canvas.yview_moveto(1.0)
    except:
        pass

def add_message(message_text, align="right"):
    weight_val = "bold" if is_bold and align == "right" else "normal"
    msg_label = CTkLabel(
        chat, 
        text=message_text, 
        corner_radius=8, 
        fg_color="#0CAAC9" if align == "right" else "#333333",
        text_color="white",
        font=CTkFont(family=current_font_family, size=current_font_size, weight=weight_val),
        wraplength=280
    )
    anchor = "e" if align == "right" else "w"
    msg_label.pack(anchor=anchor, pady=5, padx=10)
    window.after(50, scroll_to_bottom)

def sendMsg(event=None):
    global is_connected
    message = message_entry.get()
    if message.strip():
        add_message(f"{user_nickname}: {message}", align="right")
        if is_connected:
            try:
                full_message = f"{user_nickname}: {message}"
                client_socket.sendall(full_message.encode())
            except Exception as e:
                print(f"Ошибка отправки: {e}")
                is_connected = False
                update_status_ui()
        message_entry.delete(0, "end")

add_message("TEST", align="left")

message_entry = CTkEntry(
    window, 
    width=350, 
    height=35, 
    placeholder_text="написати...",
    font=CTkFont(family=current_font_family, size=current_font_size)
)
message_entry.bind("<Return>", sendMsg)
chatBTN = CTkButton(window, width=40, height=35, text="send", command=sendMsg)

def adaptive_ui(event=None):
    win_w = window.winfo_width()
    win_h = window.winfo_height()

    if win_w < 50:
        return

    menu_w = btn_menu.winfo_width()
    btn_w = chatBTN.winfo_width()
    btn_h = chatBTN.winfo_height()

    offset = MENU_WIDTH if menu_open else 0

    if menu_open:
        left_menu.place(x=0, y=0, relheight=1.0)
    else:
        left_menu.place_forget()

    btn_menu.place(x=offset, y=0)
    total_x_offset = offset + menu_w + 5

    chat.configure(width=win_w - total_x_offset - 25, height=win_h - btn_h - 20)
    chat.place(x=total_x_offset + 5, y=0)

    message_entry.configure(width=win_w - total_x_offset - btn_w - 20)
    message_entry.place(x=total_x_offset + 5, y=win_h - btn_h - 5)

    chatBTN.place(x=win_w - btn_w - 5, y=win_h - btn_h - 5)

window.bind("<Configure>", adaptive_ui)
window.after(50, adaptive_ui)

def on_closing():
    global is_connected
    is_connected = False
    try:
        client_socket.close()
    except:
        pass
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

if is_connected == True:
    receive_thread = threading.Thread(target=receive_messages, daemon=True)
    receive_thread.start()

window.mainloop()