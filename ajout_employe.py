import tkinter as tk
import tkinter.ttk as ttk

from ajout_poste1 import ajout_poste1
from database import create_connection
from database import save_employe
from tkinter import messagebox
 
def ajout_employe():
 window = tk.Toplevel()
 window.title("ajout d'employe")
 window.geometry("550x630")
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

 
 i = None
 postes_noms = []
 postes_s_noms = []
 postes_map = {}

 def poste_menu_f():
    nonlocal i, postes_noms, postes_s_noms, postes_map
    connection = create_connection()
    curs = connection.cursor()

    curs.execute("SELECT * FROM postes")
    items = curs.fetchall()

    postes_noms = []
    postes_s_noms = []
    postes_map = {}

    for i in items:
        nom = i[1]
        nom_s_list = [ s.strip() for s in i[8].split(',') if s.strip()]
        postes_noms.append(nom)
        postes_s_noms.extend(nom_s_list)

        if nom not in postes_map:
            postes_map[nom] = []
        postes_map[nom].extend(nom_s_list)

   

 poste_menu_f()

 

 if not postes_noms:
    messagebox.showerror("Erreur", "Veuillez d'abord ajouter un poste.")
    window.destroy()
    return 

 tk.Label(scrollable_frame, text="Nome et Prenom :", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", padx=5, pady=5)
 nom_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR,width=28)
 nom_entry.grid(row=0, column=1, padx=5, pady=5)

 tk.Label(scrollable_frame, text="Echelon :", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", padx=5, pady=5)
 echelon_choix = [str(i) for i in range(0,13)]
 selected_echelon = tk.StringVar(value=0)
 echelon_menu = tk.OptionMenu(scrollable_frame, selected_echelon, *echelon_choix)
 echelon_menu.grid(row=1, column=1, padx=5, pady=5)
 echelon_menu.config(bg="white", fg=FG_COLOR, highlightbackground=BG_COLOR)
 echelon_menu["menu"].config(bg="white", fg=FG_COLOR)

 tk.Label(scrollable_frame, text="Poste :", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e", padx=5, pady=5)
 poste_choix = [nom_poste for nom_poste in postes_noms]
 selected_poste = tk.StringVar(value="")
 poste_menu = tk.OptionMenu(scrollable_frame, selected_poste, *poste_choix)
 poste_menu.grid(row=2, column=1, padx=5, pady=5)
 poste_menu.config(bg="white", fg=FG_COLOR, highlightbackground=BG_COLOR)
 poste_menu["menu"].config(bg="white", fg=FG_COLOR)

 tk.Label(scrollable_frame, text="Poste superieur :", bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=0, sticky="e", padx=5, pady=5)
 selected_poste_s = tk.StringVar(value="Aucun")
 poste_s_menu = tk.OptionMenu(scrollable_frame, selected_poste_s, "")
 poste_s_menu.grid(row=3, column=1, padx=5, pady=5)
 poste_s_menu.config(bg="white", fg=FG_COLOR, highlightbackground=BG_COLOR)
 poste_s_menu["menu"].config(bg="white", fg=FG_COLOR)

# ✅ This is the only logic added to update poste_s_menu when poste is selected
 def update_poste_s(*args):
    poste = selected_poste.get()
    menu = poste_s_menu["menu"]
    menu.delete(0, "end")

    # Add "Aucun" as the first option
    menu.add_command(label="Aucun", command=tk._setit(selected_poste_s, "Aucun"))

    for poste_s in postes_map.get(poste, []):
        menu.add_command(label=poste_s, command=tk._setit(selected_poste_s, poste_s))

    selected_poste_s.set("Aucun")


 selected_poste.trace("w", update_poste_s)  # Only this line binds the update

 tk.Label(scrollable_frame, text="Situation familliale :", bg=BG_COLOR, fg=FG_COLOR).grid(row=4, column=0, sticky="e", padx=5, pady=5)
 marie_choix = ["Marié et salaire unique" ,"Marié avec deux salaires", "Celibataire"]
 selected_marie = tk.StringVar(value="Celibataire")
 marie_menu = tk.OptionMenu(scrollable_frame, selected_marie, *marie_choix)
 marie_menu.grid(row=4, column=1, padx=5, pady=5)
 marie_menu.config(bg="white", fg=FG_COLOR, highlightbackground=BG_COLOR)
 marie_menu["menu"].config(bg="white", fg=FG_COLOR)

 tk.Label(scrollable_frame, text="Nombre d'enfant :", bg=BG_COLOR, fg=FG_COLOR).grid(row=5, column=0, sticky="e", padx=5, pady=5)
 enfant_choix = [i for i in range (0,20)]
 selected_enfant = tk.StringVar(value="0")
 enfant_menu = tk.OptionMenu(scrollable_frame, selected_enfant, *enfant_choix)
 enfant_menu.grid(row=5, column=1, padx=5, pady=5)
 enfant_menu.config(bg="white", fg=FG_COLOR, highlightbackground=BG_COLOR)
 enfant_menu["menu"].config(bg="white", fg=FG_COLOR)

 tk.Label(scrollable_frame, text="Nombre d'enfant > 10 :", bg=BG_COLOR, fg=FG_COLOR).grid(row=6, column=0, sticky="e", padx=5, pady=5)
 enfant10_choix = [i for i in range (0,20)]
 selected_enfant10 = tk.StringVar(value="0")
 enfant10_menu = tk.OptionMenu(scrollable_frame, selected_enfant10, *enfant10_choix)
 enfant10_menu.grid(row=6, column=1, padx=5, pady=5)
 enfant10_menu.config(bg="white", fg=FG_COLOR, highlightbackground=BG_COLOR)
 enfant10_menu["menu"].config(bg=BG_COLOR, fg=FG_COLOR)

 def update_enfant10_menu(*args):
    try:
        max_value = int(selected_enfant.get())
    except ValueError:
        max_value = 0

    menu = enfant10_menu["menu"]
    menu.delete(0, "end")

    for i in range(max_value + 1):
        menu.add_command(label=i, command=tk._setit(selected_enfant10, i))

    selected_enfant10.set(0)

    # Disable if no children
    if max_value == 0:
        enfant10_menu.config(state="disabled")
    else:
        enfant10_menu.config(state="normal")

   
 selected_enfant.trace("w", update_enfant10_menu)
 update_enfant10_menu()



 tk.Label(scrollable_frame, text="N° d'employé :", bg=BG_COLOR, fg=FG_COLOR).grid(row=7, column=0, sticky="e", padx=5, pady=5)
 num_emp_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR)
 num_emp_entry.grid(row=7, column=1, padx=5, pady=5)

 tk.Label(scrollable_frame, text="Date de naissance (j/m/a) :", bg=BG_COLOR, fg=FG_COLOR).grid(row=8, column=0, sticky="e", padx=5, pady=5)
 date_nai_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR)
 date_nai_entry.grid(row=8, column=1, padx=5, pady=5)
 


 tk.Label(scrollable_frame, text="Date d'entrée (j/m/a) :", bg=BG_COLOR, fg=FG_COLOR).grid(row=9, column=0, sticky="e", padx=5, pady=5)
 date_en_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR)
 date_en_entry.grid(row=9, column=1, padx=5, pady=5) 


 tk.Label(scrollable_frame, text="NSS :", bg=BG_COLOR, fg=FG_COLOR).grid(row=10, column=0, sticky="e", padx=5, pady=5)
 nss_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR)
 nss_entry.grid(row=10, column=1, padx=5, pady=5)

 
 tk.Label(scrollable_frame, text="N° de compte :", bg=BG_COLOR, fg=FG_COLOR).grid(row=11, column=0, sticky="e", padx=5, pady=5)
 ccp_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR)
 ccp_entry.grid(row=11, column=1, padx=5, pady=5)





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



    
 n=12
 name_ind = []
 ind = []
 autre_name_indda = []
 autre_indda = []
 autre_indda_p = []
 global_row_index = n +1

 def autre_ind():
     nonlocal global_row_index,autre_name_indda,autre_indda,autre_indda_p

     block_widgets = []  # Store widgets of this block
     block_rows = []     # Store the rows this block occupies

     def remove_block():
        nonlocal global_row_index,autre_name_indda,autre_indda,autre_indda_p

        for widget in block_widgets:
            widget.destroy()
            if isinstance(widget, tk.Entry):
             if widget in name_ind:
                name_ind.remove(widget)
             elif widget in ind:
                ind.remove(widget)
             elif widget in autre_name_indda:
                autre_name_indda.remove(widget)
             elif widget in autre_indda:
                autre_indda.remove(widget)
             elif widget in autre_indda_p:
                autre_indda_p.remove(widget)
        # Shift all widgets below this block up
        for child in scrollable_frame.winfo_children():
            info = child.grid_info()
            row = info["row"]
            if row > block_rows[-1]:
                child.grid(row=row - len(block_rows))  # Shift up

        global_row_index -= len(block_rows)

    

     row = global_row_index
     label_nom = tk.Label(scrollable_frame, bg=BG_COLOR, fg=FG_COLOR, text="Nom :")
     label_nom.grid(row=row, column=0, pady=5, sticky="e")
     block_widgets.append(label_nom)
     block_rows.append(row)

     name_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR, width=20)
     name_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
     autre_name_indda.append(name_entry)
     block_widgets.append(name_entry)

     btn_del = ttk.Button(
      scrollable_frame,
      text="Supprimer",
      command=remove_block,
      style="Supprimer.TButton")


     btn_del.grid(row=row, column=2, padx=5)
     block_widgets.append(btn_del)

     row += 1
     label_da = tk.Label(scrollable_frame, bg=BG_COLOR, fg=FG_COLOR, text="DA")
     label_da.grid(row=row, column=0, pady=5, sticky="e")
     block_widgets.append(label_da)
     block_rows.append(row)

     da_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR, width=8)
     da_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
     autre_indda.append(da_entry)
     block_widgets.append(da_entry)

     row += 1
     label_pct = tk.Label(scrollable_frame, bg=BG_COLOR, fg=FG_COLOR, text="% :")
     label_pct.grid(row=row, column=0, pady=5, sticky="e")
     block_widgets.append(label_pct)
     block_rows.append(row)

     pct_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR, width=8)
     pct_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
     autre_indda_p.append(pct_entry)
     block_widgets.append(pct_entry)

     global_row_index = row + 1

     sauvgarder_button.grid_forget()
     sauvgarder_button.grid(row=global_row_index, column=0, sticky="nsew", padx=5, pady=5)    
   



   
 tk.Label(scrollable_frame, text="Autre idemnitées :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)


 style = ttk.Style()
 style.configure("ajouter.TButton",
    font=("Segoe UI", 12, "bold"),
    foreground="white",
    background="#347433",
    padding=3,
    relief="groove"
 )
 style.map("ajouter.TButton",
    background=[("active", "#FF9A9A")],
    foreground=[("active", "white")]
 )

 ajouter_button = ttk.Button(
    scrollable_frame,
    text="Ajouter",
    command=autre_ind,
    style="ajouter.TButton"
 )
 ajouter_button.grid(row=n, column=1, sticky="nsew", padx=5, pady=5)
 n+=1
 def get_indemnite_values():
    connection = create_connection()
    curs = connection.cursor()

    curs.execute("SELECT id FROM postes where nom_poste=?",(selected_poste.get(),))
    id_poste = curs.fetchall()
    

    autre_name_indda_val=",".join([entry.get() for entry in autre_name_indda])
    autre_indda_val=  ",".join([entry.get() for entry in autre_indda])
    autre_indda_p_val= ",".join([entry.get() for entry in autre_indda_p])
    name=nom_entry.get()
    enfant10=selected_enfant10.get()
    enfant=selected_enfant.get()
    nom_poste=selected_poste.get()
    nom_poste_s=selected_poste_s.get()
    marie=selected_marie.get()
    echelon=selected_echelon.get()
    date_nai=date_nai_entry.get()
    date_en=date_en_entry.get()
    nss=nss_entry.get()
    ccp=ccp_entry.get()
    num_emp=num_emp_entry.get()



    if nom_poste=="" :
     window_error = tk.Toplevel()
     window_error.title("Erreur")
     window_error.geometry("340x50")
     BG_COLOR = "#D3D3D3" # Light Gray
     FG_COLOR = "black"   # Black
     window_error.configure(bg=BG_COLOR)
     tk.Label(window_error, text="Selectionner un poste s'il vous plait", bg=BG_COLOR, fg="red",font=("sans-serif", 12, "bold"),anchor="center",justify="center").grid(row=0, column=0, sticky="e", padx=5, pady=5)

    else:
    
     save_employe(name,echelon,nom_poste,nom_poste_s,marie,enfant,
      enfant10,id_poste[0][0],autre_name_indda_val,autre_indda_val,autre_indda_p_val,
       date_nai,date_en,nss,ccp,num_emp)
     window.destroy()   




 style = ttk.Style()
 style.configure("sauvgarder.TButton",
    font=("Segoe UI", 12, "bold"),
    foreground="white",
    background="#FFC107",
    padding=3,
    relief="groove"
 )
 style.map("sauvgarder.TButton",
    background=[("active", "#B6F500")],
    foreground=[("active", "white")]
 )

 sauvgarder_button = ttk.Button(
    scrollable_frame,
    text="Sauvgarder",
    command=get_indemnite_values,
    style="sauvgarder.TButton"
 )
 sauvgarder_button.grid(row=n+1, column=0, sticky="nsew", padx=5, pady=5)

  





































