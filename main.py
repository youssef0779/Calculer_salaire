import tkinter as tk
from ajout_poste import ajout_poste
from list_poste import list_postes
from ajout_employe import ajout_employe
from list_employe import list_employe
import tkinter.ttk as ttk
import requests
from tkinter import messagebox


from ttkthemes import ThemedTk

root = ThemedTk(theme="equilux") 


root.title("Calculer")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("260x600")

BG_COLOR = "#D3D3D3"
FG_COLOR = "black"
root.configure(bg=BG_COLOR)

# ========== Scroll Setup ==========
main_canvas = tk.Canvas(root, bg=BG_COLOR)
main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=main_canvas.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

main_canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar_x.set)

scrollable_frame = tk.Frame(main_canvas, bg=BG_COLOR)
canvas_root = main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")


def on_configure(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_configure)


def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

main_canvas.bind("<Enter>", lambda e: main_canvas.bind("<MouseWheel>", _on_mousewheel))
main_canvas.bind("<Leave>", lambda e: main_canvas.unbind("<MouseWheel>"))

main_canvas.bind("<Enter>", lambda e: (
    main_canvas.bind("<Button-4>", lambda event: main_canvas.yview_scroll(-1, "units")),
    main_canvas.bind("<Button-5>", lambda event: main_canvas.yview_scroll(1, "units"))
))
main_canvas.bind("<Leave>", lambda e: (
    main_canvas.unbind("<Button-4>"),
    main_canvas.unbind("<Button-5>")
))

# ========== Styles ==========
style = ttk.Style()
style.configure("employe.TButton",
                font=("Segoe UI", 14, "bold"),
                foreground="white",
                background="#123524",
                padding=3,
                relief="groove")
style.map("employe.TButton",
          background=[("active", "#FF3F33")],
          foreground=[("active", "white")])

style.configure("poste.TButton",
                font=("Segoe UI", 14, "bold"),
                foreground="white",
                background="#85A947",
                padding=3,
                relief="groove")
style.map("poste.TButton",
          background=[("active", "#16C47F")],
          foreground=[("active", "white")])

style.configure("upload.TButton",
                font=("Segoe UI", 8, "bold"),
                foreground="white",
                background="#16423C",
                padding=3,
                relief="groove")
style.map("upload.TButton",
          background=[("active", "#6A9C89")],
          foreground=[("active", "white")])

style.configure("download.TButton",
                font=("Segoe UI", 8, "bold"),
                foreground="white",
                background="#191919",
                padding=3,
                relief="groove")
style.map("download.TButton",
          background=[("active", "#750E21")],
          foreground=[("active", "white")])

# ========== Buttons ==========
list_employe = ttk.Button(scrollable_frame, text="List des employés", command=list_employe, style="employe.TButton")
list_employe.pack(anchor="center", padx=10, pady=(10, 5),ipady=20)

list_poste = ttk.Button(scrollable_frame, text="List des postes", command=list_postes, style="poste.TButton")
list_poste.pack(anchor="center", padx=10, pady=(0, 50),ipady=20)

ajout_employe = ttk.Button(scrollable_frame, text="Ajouter un employé", command=ajout_employe, style="employe.TButton")
ajout_employe.pack(anchor="center", padx=10, pady=(5, 5),ipady=20)

ajout_poste = ttk.Button(scrollable_frame, text="Ajouter un poste", command=ajout_poste, style="poste.TButton")
ajout_poste.pack(anchor="center", padx=10, pady=(0, 50),ipady=20)

# ========== Upload/Download Logic ==========
ip_add = "192.168.1.101:10101"
http_ip_add_port_file = f"http://{ip_add}/calcul_salaire.db"

def upload_db():

    confirm = messagebox.askyesno(
        title="Confirmation",
        message="Êtes‑vous sure de envoyer la base des données ?",
        parent=root          # facultatif mais conseillé
    )
    if not confirm:           # L’utilisateur a cliqué « Non » : on annule.
        return

    try:
        with open("calcul_salaire.db", "rb") as f:
            response = requests.put(http_ip_add_port_file, data=f)
        if response.status_code in (200, 201, 204):
            messagebox.showinfo("Succès", "Base envoyée avec succès.")
        else:
            messagebox.showerror("Erreur", f"Échec de l'envoi : {response.status_code}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def download_db():

    confirm = messagebox.askyesno(
        title="Confirmation",
        message="Êtes‑vous sure de telecharger la base des données?",
        parent=root          # facultatif mais conseillé
    )
    if not confirm:           # L’utilisateur a cliqué « Non » : on annule.
        return

    try:
        response = requests.get(http_ip_add_port_file)
        if response.status_code == 200:
            with open("calcul_salaire.db", "wb") as f:
                f.write(response.content)
            messagebox.showinfo("Succès", "Base téléchargée avec succès.")
        else:
            messagebox.showerror("Erreur", f"Échec du téléchargement : {response.status_code}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

upload = ttk.Button(scrollable_frame, text="Upload DB", command=upload_db, style="upload.TButton", width=20)
upload.pack(anchor="center", padx=10, pady=(5, 5))



download = ttk.Button(scrollable_frame, text="Télécharger DB", command=download_db, style="download.TButton", width=20)
download.pack(anchor="center", padx=10, pady=(5, 10))


# Server Entry
server_frame = tk.Frame(scrollable_frame, bg=BG_COLOR)
server_frame.pack(anchor="w", padx=10, pady=5)

tk.Label(server_frame, text="Serveur :", bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
poste_s_box = tk.Entry(server_frame, state="normal", width=18, bg="white", fg=FG_COLOR)
poste_s_box.pack(side="left", padx=(5, 0))
poste_s_box.insert(0, ip_add)
poste_s_box.config(state="readonly")

root.mainloop()
