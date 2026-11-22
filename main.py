# Not Defteri (tkinter GUI)
# Notları JSON dosyasında saklar. Oluşturma, düzenleme, silme ve arama yapılabilir.

import json
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "notlar.json"


def load_notes():
    # Notları dosyadan okur
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_notes():
    # Notları dosyaya yazar
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=2)


def refresh_list():
    # Sol listedeki başlıkları arama kutusuna göre yeniler
    note_list.delete(0, tk.END)
    visible_indexes.clear()
    keyword = search_var.get().lower()
    for i, note in enumerate(notes):
        if keyword in note["title"].lower() or keyword in note["content"].lower():
            note_list.insert(tk.END, note["title"])
            visible_indexes.append(i)  # Listedeki sıra -> notes içindeki gerçek index


def get_selected_index():
    # Listede seçili notun notes içindeki index'ini döndürür
    selection = note_list.curselection()
    if not selection:
        return None
    return visible_indexes[selection[0]]


def show_note(event=None):
    # Seçilen notu sağdaki alanlara yükler
    index = get_selected_index()
    if index is None:
        return
    title_entry.delete(0, tk.END)
    title_entry.insert(0, notes[index]["title"])
    content_text.delete("1.0", tk.END)
    content_text.insert("1.0", notes[index]["content"])


def clear_form():
    # Yeni not için alanları temizler
    note_list.selection_clear(0, tk.END)
    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)
    title_entry.focus()


def save_note():
    # Seçili not varsa günceller, yoksa yeni not ekler
    title = title_entry.get().strip()
    content = content_text.get("1.0", tk.END).strip()
    if title == "":
        messagebox.showwarning("Uyarı", "Başlık boş olamaz.")
        return
    index = get_selected_index()
    if index is None:
        notes.append({"title": title, "content": content})
    else:
        notes[index] = {"title": title, "content": content}
    save_notes()
    refresh_list()
    status_var.set("Not kaydedildi.")


def delete_note():
    # Seçili notu onay alarak siler
    index = get_selected_index()
    if index is None:
        messagebox.showinfo("Bilgi", "Silmek için bir not seçin.")
        return
    if messagebox.askyesno("Onay", f"'{notes[index]['title']}' silinsin mi?"):
        notes.pop(index)
        save_notes()
        refresh_list()
        clear_form()
        status_var.set("Not silindi.")


# --- Arayüz ---
notes = load_notes()
visible_indexes = []

window = tk.Tk()
window.title("Not Defteri")
window.geometry("700x450")

# Sol taraf: arama kutusu ve not listesi
left = tk.Frame(window, padx=8, pady=8)
left.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(left, text="Ara:").pack(anchor="w")
search_var = tk.StringVar()
search_var.trace_add("write", lambda *args: refresh_list())  # Her harfte listeyi yenile
tk.Entry(left, textvariable=search_var).pack(fill=tk.X)

note_list = tk.Listbox(left, width=25)
note_list.pack(fill=tk.Y, expand=True, pady=5)
note_list.bind("<<ListboxSelect>>", show_note)

# Sağ taraf: başlık, içerik ve butonlar
right = tk.Frame(window, padx=8, pady=8)
right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(right, text="Başlık:").pack(anchor="w")
title_entry = tk.Entry(right)
title_entry.pack(fill=tk.X)

tk.Label(right, text="İçerik:").pack(anchor="w", pady=(5, 0))
content_text = tk.Text(right, wrap=tk.WORD)
content_text.pack(fill=tk.BOTH, expand=True)

buttons = tk.Frame(right)
buttons.pack(fill=tk.X, pady=5)
tk.Button(buttons, text="Yeni Not", command=clear_form).pack(side=tk.LEFT)
tk.Button(buttons, text="Kaydet", command=save_note).pack(side=tk.LEFT, padx=5)
tk.Button(buttons, text="Sil", command=delete_note).pack(side=tk.LEFT)

status_var = tk.StringVar(value=f"{len(notes)} not yüklendi.")
tk.Label(right, textvariable=status_var, fg="gray").pack(anchor="w")

refresh_list()
window.mainloop()
