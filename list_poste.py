import tkinter as tk
from database import create_connection
from poste_page import poste_page
import tkinter.ttk as ttk
from tkinter import messagebox


window=None
def list_postes():
 global window 
 window = tk.Toplevel()
 window.title("Liste des postes")
 window.geometry("520x600")
 BG_COLOR = "#D3D3D3" # Light Gray
 FG_COLOR = "black"   # Black

 window.configure(bg=BG_COLOR)

# ========== Scroll Setup ==========
# Set canvas background
 main_canvas = tk.Canvas(window, bg=BG_COLOR)
 main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

 scrollbar = tk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
 scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

 main_canvas.configure(yscrollcommand=scrollbar.set)

# Set the background of the scrollable frame
 scrollable_frame = tk.Frame(main_canvas, bg=BG_COLOR)
 main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

 def on_configure(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

 scrollable_frame.bind("<Configure>", on_configure)

 def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# Bind mouse wheel only when cursor is inside the canvas
 main_canvas.bind("<Enter>", lambda e: main_canvas.bind("<MouseWheel>", _on_mousewheel))
 main_canvas.bind("<Leave>", lambda e: main_canvas.unbind("<MouseWheel>"))

# For Linux (if you're using Linux Mint)
 main_canvas.bind("<Enter>", lambda e: (
    main_canvas.bind("<Button-4>", lambda event: main_canvas.yview_scroll(-1, "units")),
    main_canvas.bind("<Button-5>", lambda event: main_canvas.yview_scroll(1, "units"))
))
 main_canvas.bind("<Leave>", lambda e: (
    main_canvas.unbind("<Button-4>"),
    main_canvas.unbind("<Button-5>")
))


 def delete_poste():

     confirm = messagebox.askyesno(
        title="Confirmation",
        message="Êtes‑vous sur de vouloir supprimer ce poste ?",
        parent=window          # facultatif mais conseillé
    )
     if not confirm:           # L’utilisateur a cliqué « Non » : on annule.
        return

        
     connection = create_connection()
     curs = connection.cursor()
    
     try:
        curs.execute("DELETE FROM postes WHERE id=?", (i[0],))
        connection.commit()
        connection.close()
        window.destroy()
        if window:
            window.destroy()
        list_postes()
    
     except Exception as e:
        connection.rollback()
        connection.close()
        messagebox.showerror("Erreur", "Impossible de supprimer ce poste.\nVeuillez d'abord supprimer les employés qui l'utilisent.")


 connection=create_connection()
 curs= connection.cursor()


 curs.execute("SELECT * FROM postes")
 item = curs.fetchall()

 row_num = 1 
 for i in item:
    
    tk.Label(scrollable_frame, text=str(i[0])+" NOM :", bg=BG_COLOR, fg=FG_COLOR).grid(row=row_num, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="readonly", width=20, bg="white", fg=FG_COLOR)
    nom_box.grid(row=row_num, column=1, padx=5, pady=5, sticky="w")
    nom_box.config(state="normal")
    nom_box.delete(0, tk.END)
    nom_box.insert(0, i[1])
    nom_box.config(state="readonly")

    style = ttk.Style()
    style.configure("Visiter.TButton",
     font=("Segoe UI", 12, "bold"),
     foreground="white",
     background="#347433",
     padding=3,
     relief="groove"
 )
    style.map("Visiter.TButton",
     background=[("active", "#FF9A9A")],
     foreground=[("active", "white")]
 )

    visiter_button = ttk.Button(
     scrollable_frame,
     text="Visiter",
     command=lambda postes=i: poste_page(postes),
     style="Visiter.TButton"
 )


    visiter_button.grid(row=row_num, column=2, sticky="e",padx=5, pady=10)


    style = ttk.Style()
    style.configure("Supprimer.TButton",
     font=("Segoe UI", 10, "bold"),
     foreground="white",
     background="#B22222",
     padding=3,
     relief="groove"
      )
    style.map("Supprimer.TButton",
     background=[("active", "#E07A5F")],
     foreground=[("active", "white")]
 )


    btn_del = ttk.Button(
      scrollable_frame,
      text="Supprimer",
      command=delete_poste,
      style="Supprimer.TButton")


    btn_del.grid(row=row_num, column=3, sticky="w",padx=5, pady=10)

    row_num += 1  # ✅ increment row number
