import customtkinter as ctk
import time
import write_db
from tkinter import ttk, messagebox
import read_db
# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def update_tree():
    platz = 1
    for item in tree.get_children():
        tree.delete(item)
    for i in read_db.read_from_db():
        tree.insert("", "end", values=(platz, i[0], i[1]))
        platz+=1
    
def open_popup_name(time_user):
    time_user = round(time_user, 2)
    popup = ctk.CTkToplevel(app)
    popup.geometry("400x200")
    popup.title("Automatic")
    label = ctk.CTkLabel(popup, text=f"Zeit: {time_user}s \n Bitte gib deinen Namen ein:", font=("Helvetica", 16))
    label.pack(pady=10)
    entry = ctk.CTkEntry(popup, width=300)
    entry.pack(pady=10)
    
    def submit_text():
        user_input = entry.get()
        popup.destroy()
        write_db.write_to_db(user_input, time_user)
        update_tree()
    submit_button = ctk.CTkButton(popup, text="Submit", command=submit_text)
    submit_button.pack(pady=10)
    popup.grab_set()
    popup.focus_force()
    popup.mainloop()
    
def open_popup_manual_input():
    popup = ctk.CTkToplevel(app)
    popup.geometry("400x200")
    popup.title("Manual")
    
    label = ctk.CTkLabel(popup, text=f"Manuelle Eingabe des Namen und der Zeit:", font=("Helvetica", 16))
    label.pack(pady=10)
    entry_name = ctk.CTkEntry(popup, width=300)
    entry_name.pack(pady=10)
    entry_time = ctk.CTkEntry(popup, width=300)
    entry_time.pack(pady=10)
    
    def submit_text():
        user_name = entry_name.get()
        user_time = entry_time.get()
        popup.destroy()
        write_db.write_to_db(user_name, float(user_time))
        update_tree()
    submit_button = ctk.CTkButton(popup, text="Submit", command=submit_text)
    submit_button.pack(pady=10)
    popup.grab_set()
    popup.focus_force()
    popup.mainloop()



def toggle(event):
    global is_running, start_time, elapsed_time
    if is_running:
        stop()
        open_popup_name(float(elapsed_time))
    else:
        start()
        

def start():
    elapsed_time = 0
    global is_running, start_time
    is_running = True
    start_time = time.time() - elapsed_time
    update_clock()

def stop():
    global is_running, elapsed_time
    is_running = False
    elapsed_time = time.time() - start_time

def update_clock():
    global elapsed_time
    if is_running:
        elapsed_time = time.time() - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    seconds, milliseconds = divmod(seconds, 1)
    milliseconds = int(milliseconds * 1000)
    label.configure(text=f"{int(minutes):02}:{int(seconds):02}:{milliseconds:03}")
    app.after(50, update_clock)
    
def delete_selected_entry():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No item selected")
    else:
        for item in selected_item:
            value = tree.item(item)['values'][1]
            write_db.delete_item(value)
            update_tree()
            
def open_popup_search_results(results):
    popup = ctk.CTkToplevel(app)
    popup.geometry("400x200")
    popup.title("Search")
    
    label = ctk.CTkLabel(popup, text=f"Name: {results[0]} \n Zeit: {results[1]}", font=("Helvetica", 16))
    label.pack(pady=10)
    def submit_text():         
        popup.destroy()
    submit_button = ctk.CTkButton(popup, text="Ok", command=submit_text)
    submit_button.pack(pady=10)
    popup.grab_set()
    popup.focus_force()
    popup.mainloop()

def open_popup_search():
    popup = ctk.CTkToplevel(app)
    popup.geometry("400x200")
    popup.title("Search")
    
    label = ctk.CTkLabel(popup, text=f"Gib den Namen ein: ", font=("Helvetica", 16))
    label.pack(pady=10)
    entry_name = ctk.CTkEntry(popup, width=300)
    entry_name.pack(pady=10)
    
    def submit_text():
        user_name = entry_name.get()
        for item in tree.get_children():
            value = tree.item(item)['values'][1]
            if user_name.lower() in value.lower():
                open_popup_search_results([value, tree.item(item)['values'][2]])
            
        popup.destroy()
    submit_button = ctk.CTkButton(popup, text="Submit", command=submit_text)
    submit_button.pack(pady=10)
    popup.grab_set()
    popup.focus_force()
    popup.mainloop()

is_running = False
start_time = 0
elapsed_time = 0

app = ctk.CTk()
app.geometry("1000x600")
app.title("BobbyCar Ranking")

label = ctk.CTkLabel(app, text="00:00:00:000", font=("Helvetica", 48))
label.pack(pady=20)


bg_color = app._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
text_color = app._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
selected_color = app._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
treestyle = ttk.Style()
treestyle.theme_use('default')
treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
app.bind("<<TreeviewSelect>>", lambda event: app.focus_set())


tree = ttk.Treeview(app, columns=('Platz', 'Name', 'Zeit'), show='headings', height=15)
tree.heading('Platz', text='Platz')
tree.heading('Name', text='Name')
tree.heading('Zeit', text='Zeit')
tree.pack(pady=20)

manual_entry = ctk.CTkButton(app, text="Add Entry Manual", command=open_popup_manual_input)
manual_entry.pack(pady=10)

delete_entry = ctk.CTkButton(app, text="Delete selected Entry", command=delete_selected_entry)
delete_entry.pack(pady=10)

search_entry = ctk.CTkButton(app, text="Search by name", command=open_popup_search)
search_entry.pack(pady=10)

app.bind("<space>", toggle)

update_clock()
update_tree()
app.mainloop()