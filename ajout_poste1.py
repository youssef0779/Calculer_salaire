import tkinter as tk
from database import save_poste
import tkinter.ttk as ttk

def ajout_poste1(poste_entry,selected_categorie,name_ind_val, ind_val,name_indda_val, indda_val, indda_p_val,window):
   
 window.destroy()   
 window = tk.Toplevel()
 window.title("ajout de poste")
 window.geometry("500x600")
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


 tk.Label(scrollable_frame, text="Les postes superieurs", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e", padx=5, pady=5)
 indemnite_choix = ["Aucun","Ajouter les postes"]
 selected_indemnite = tk.StringVar(value="Aucun")
 poste_menu = tk.OptionMenu(scrollable_frame, selected_indemnite, *indemnite_choix)
 poste_menu.grid(row=2, column=1, padx=5, pady=5)
 poste_menu.config(bg="white", fg=FG_COLOR, highlightbackground=BG_COLOR)
 poste_menu["menu"].config(bg="white", fg=FG_COLOR)

 name_poste=[]
 indice_poste=[]

 def get_indemnite_values():
    name_poste_val = ",".join([entry.get() for entry in name_poste])
    indice_poste_val =  ",".join([entry.get() for entry in indice_poste])
    if selected_indemnite.get()=="Aucun":
     indice_poste_val="0"
     name_poste_val="Aucun"
    else : 
     indice_poste_val =  ",".join([entry.get() for entry in indice_poste])

    window.destroy()
    save_poste(poste_entry,selected_categorie,name_ind_val, ind_val,name_indda_val, indda_val, indda_p_val,name_poste_val,indice_poste_val)
   


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

 
 sauvgarder_button.grid(row=4, column=0, sticky="e", padx=5, pady=13, ipadx=8, ipady=2)

 global_row_index = 5  # Start after the initial rows


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

 name_poste=[]
 indice_poste=[]
 def add_poste_s():
    nonlocal global_row_index

    block_widgets = []  # Store widgets of this block
    block_rows = []     # Store the rows this block occupies

    def remove_block():
     nonlocal global_row_index

     for widget in block_widgets:
        widget.destroy()

        # Clean up from the entry lists if it's an entry
        if isinstance(widget, tk.Entry):
            if widget in name_poste:
                name_poste.remove(widget)
            if widget in indice_poste:
                indice_poste.remove(widget)

    # Shift all widgets below this block up
     for child in scrollable_frame.winfo_children():
        info = child.grid_info()
        row = info["row"]
        if row > block_rows[-1]:
            child.grid(row=row - len(block_rows))

     global_row_index -= len(block_rows)


        

    if selected_indemnite.get() == "Ajouter les postes":
        row = global_row_index

        label_nom = tk.Label(scrollable_frame, bg=BG_COLOR, fg=FG_COLOR, text="Nom de poste :")
        label_nom.grid(row=row, column=0, pady=5, sticky="e")
        block_widgets.append(label_nom)
        block_rows.append(row)

        poste_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR, width=20)
        poste_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        name_poste.append(poste_entry)
        block_widgets.append(poste_entry)


        btn_del = ttk.Button(
         scrollable_frame,
         text="Supprimer",
         command=remove_block,
         style="Supprimer.TButton")

        btn_del.grid(row=row, column=2, padx=5)
        block_widgets.append(btn_del)

        row += 1
        label_indice = tk.Label(scrollable_frame, bg=BG_COLOR, fg=FG_COLOR, text="indice :")
        label_indice.grid(row=row, column=0, pady=5, sticky="e")
        block_widgets.append(label_indice)
        block_rows.append(row)

        indice_poste_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR, width=5)
        indice_poste_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        indice_poste.append(indice_poste_entry)
        block_widgets.append(indice_poste_entry)

        global_row_index = row + 1

    
        # Move "Suivant" button down
    sauvgarder_button.grid_forget()
    sauvgarder_button.grid(row=global_row_index, column=0, sticky="e", padx=5, pady=10)
    
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
    command=add_poste_s,
    style="ajouter.TButton"
 )
    
 ajouter_button.grid(row=2, column=2, sticky="e",padx=5, pady=10)

