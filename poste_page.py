import tkinter as tk
from database import create_connection
from database import save_user
import list_poste
from tkinter import messagebox
import tkinter.ttk as ttk


def poste_page(postes):  # user is a tuple like (id, name, grade, ...)
    window = tk.Toplevel()
    window.title(f"Page de poste - {postes[1]}")
    window.geometry("520x600")
    BG_COLOR = "#D3D3D3"
    FG_COLOR = "black"

    window.configure(bg=BG_COLOR)

    # ========== Scroll Setup ==========
    main_canvas = tk.Canvas(window, bg=BG_COLOR)
    main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    main_canvas.configure(yscrollcommand=scrollbar.set)

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

    
    # Now using user tuple directly
    tk.Label(scrollable_frame, text="NOM :", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=28, bg="white", fg=FG_COLOR)
    nom_box.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, postes[1])
    nom_box.config(state="readonly")

    tk.Label(scrollable_frame, text="Categorie :", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=10, bg="white", fg=FG_COLOR)
    nom_box.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, postes[2])
    nom_box.config(state="readonly") 



    nom_list = postes[3].split(",") 
    ind_list = postes[4].split(",") 
    n=2
    if (len(postes[3])>0) and (len(postes[4])>0) :
     tk.Label(scrollable_frame, text="Indemnités % :", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="w", padx=5, pady=5)

     for  nom, ind in zip(nom_list, ind_list) :
        n+=1
        tk.Label(scrollable_frame, text="Nom :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=28, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, nom)
        nom_box.config(state="readonly")
        
        tk.Label(scrollable_frame, text="% :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=4, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=3, padx=5, pady=5, sticky="w")
        nom_box.insert(0, ind)
        nom_box.config(state="readonly")
        n+=1
   


    nom_list = postes[5].split(",") 
    indda_list = postes[6].split(",")
    indda_p_list = postes[7].split(",")
    if (len(postes[5])>0) and (len(postes[6])>0) and (len(postes[7])>0) :
     tk.Label(scrollable_frame, text="Indemnités en DA :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)

     for  nom, indda,p_indda in zip(nom_list, indda_list,indda_p_list) :
        n+=1
        tk.Label(scrollable_frame, text="Nom :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=28, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, nom)
        nom_box.config(state="readonly")

        n+=1
        tk.Label(scrollable_frame, text="DA :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, indda)
        nom_box.config(state="readonly")
        
        tk.Label(scrollable_frame, text="% :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=4, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=3, padx=5, pady=5, sticky="w")
        nom_box.insert(0, p_indda)
        nom_box.config(state="readonly")
        n+=1
    



    nom_poste = postes[8].split(",") 
    indice_poste = postes[9].split(",") 
    if (len(postes[8])>0) and (len(postes[9])>0):
     tk.Label(scrollable_frame, text="Poste superieurs:", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
   
     for  nom, indice in zip(nom_poste, indice_poste) :
        n+=1
        tk.Label(scrollable_frame, text="Nom :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=28, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, nom)
        nom_box.config(state="readonly")
        
        tk.Label(scrollable_frame, text="Indice :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=4, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=3, padx=5, pady=5, sticky="w")
        nom_box.insert(0, indice)
        nom_box.config(state="readonly")
        n+=1

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
        curs.execute("DELETE FROM postes WHERE id=?", (postes[0],))
        connection.commit()
        connection.close()
        window.destroy()
        if list_poste.window:
            list_poste.window.destroy()
        list_poste.list_postes()
    
     except Exception as e:
        connection.rollback()
        connection.close()
        messagebox.showerror("Erreur", "Impossible de supprimer ce poste.\nVeuillez d'abord supprimer les employés qui l'utilisent.")

   


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


    btn_del.grid(row=n, column=1, sticky="w",padx=5, pady=10)
