import tkinter as tk
import tkinter.ttk as ttk

from ajout_poste1 import ajout_poste1


def ajout_poste():
 window = tk.Toplevel()
 window.title("ajout de poste")
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

 

 tk.Label(scrollable_frame, text="Nome de poste :", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", padx=5, pady=5)
 poste_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR)
 poste_entry.grid(row=0, column=1, padx=5, pady=5)

 tk.Label(scrollable_frame, text="Categorie :", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", padx=5, pady=5)
 categorie_choix = [str(i) for i in range(1,18)]
 selected_categorie = tk.StringVar(value=1)
 categorie_menu = tk.OptionMenu(scrollable_frame, selected_categorie, *categorie_choix)
 categorie_menu.grid(row=1, column=1, padx=5, pady=5)
 categorie_menu.config(bg="white", fg=FG_COLOR, highlightbackground=BG_COLOR)
 categorie_menu["menu"].config(bg="white", fg=FG_COLOR)

 tk.Label(scrollable_frame, text="Indemnité en % "+"ou en DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e", padx=5, pady=5)
 indemnite_choix = ["%"+" de salaire de base","en DA"]
 selected_indemnite = tk.StringVar(value="choisir")
 indemnite_menu = tk.OptionMenu(scrollable_frame, selected_indemnite, *indemnite_choix)
 indemnite_menu.grid(row=2, column=1, padx=5, pady=5)
 indemnite_menu.config(bg="white", fg=FG_COLOR, highlightbackground=BG_COLOR)
 indemnite_menu["menu"].config(bg="white", fg=FG_COLOR)


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


 name_ind = []
 ind = []
 name_indda = []
 indda = []
 indda_p = []

 def get_indemnite_values():
    name_ind_val = ",".join([entry.get() for entry in name_ind])
    ind_val =  ",".join([entry.get() for entry in ind])
    name_indda_val =  ",".join([entry.get() for entry in name_indda])
    indda_val =  ",".join([entry.get() for entry in indda])
    indda_p_val =  ",".join([entry.get() for entry in indda_p])
 

    ajout_poste1(poste_entry.get(),selected_categorie.get(),
    name_ind_val, ind_val,name_indda_val, indda_val, indda_p_val,window)

 style = ttk.Style()
 style.configure("Suivant.TButton",
    font=("Segoe UI", 12, "bold"),
    foreground="white",
    background="#FFC107",
    padding=3,
    relief="groove"
 )
 style.map("Suivant.TButton",
    background=[("active", "#B6F500")],
    foreground=[("active", "white")]
 )

 suivant_button = ttk.Button(
    scrollable_frame,
    text="Suivant",
    command=get_indemnite_values,
    style="Suivant.TButton"
 )
 suivant_button.grid(row=4, column=0, sticky="e", padx=5, pady=10)

 global_row_index = 3  # Start after the initial rows

 def add_ind():
    nonlocal global_row_index

    block_widgets = []  # Store widgets of this block
    block_rows = []     # Store the rows this block occupies

    def remove_block():
        nonlocal global_row_index

        for widget in block_widgets:
            widget.destroy()
            if isinstance(widget, tk.Entry):
             if widget in name_ind:
                name_ind.remove(widget)
             elif widget in ind:
                ind.remove(widget)
             elif widget in name_indda:
                name_indda.remove(widget)
             elif widget in indda:
                indda.remove(widget)
             elif widget in indda_p:
                indda_p.remove(widget)
        # Shift all widgets below this block up
        for child in scrollable_frame.winfo_children():
            info = child.grid_info()
            row = info["row"]
            if row > block_rows[-1]:
                child.grid(row=row - len(block_rows))  # Shift up

        global_row_index -= len(block_rows)

    if selected_indemnite.get() == "%"+" de salaire de base":
        row = global_row_index

        label_nom = tk.Label(scrollable_frame, bg=BG_COLOR, fg=FG_COLOR, text="Nom :")
        label_nom.grid(row=row, column=0, pady=5, sticky="e")
        block_widgets.append(label_nom)
        block_rows.append(row)

        name_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR, width=20)
        name_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        name_ind.append(name_entry)
        block_widgets.append(name_entry)



        btn_del = ttk.Button(
         scrollable_frame,
         text="Supprimer",
         command=remove_block,
         style="Supprimer.TButton")

        btn_del.grid(row=row, column=2, padx=5)
        block_widgets.append(btn_del)

        row += 1
        label_pct = tk.Label(scrollable_frame, bg=BG_COLOR, fg=FG_COLOR, text="%")
        label_pct.grid(row=row, column=0, pady=5, sticky="e")
        block_widgets.append(label_pct)
        block_rows.append(row)

        pct_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR, width=5)
        pct_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        ind.append(pct_entry)
        block_widgets.append(pct_entry)

        global_row_index = row + 1

    elif selected_indemnite.get() == "en DA":
        row = global_row_index

        label_nom = tk.Label(scrollable_frame, bg=BG_COLOR, fg=FG_COLOR, text="Nom :")
        label_nom.grid(row=row, column=0, pady=5, sticky="e")
        block_widgets.append(label_nom)
        block_rows.append(row)

        name_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR, width=20)
        name_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        name_indda.append(name_entry)
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

        da_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR, width=5)
        da_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        indda.append(da_entry)
        block_widgets.append(da_entry)

        row += 1
        label_pct = tk.Label(scrollable_frame, bg=BG_COLOR, fg=FG_COLOR, text="% :")
        label_pct.grid(row=row, column=0, pady=5, sticky="e")
        block_widgets.append(label_pct)
        block_rows.append(row)

        pct_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR, width=5)
        pct_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        indda_p.append(pct_entry)
        block_widgets.append(pct_entry)

        global_row_index = row + 1
        # Move "Suivant" button down
    suivant_button.grid_forget()
    suivant_button.grid(row=global_row_index, column=0, sticky="e", padx=5, pady=10)
    
    


 style = ttk.Style()
 style.configure("ajouter.TButton",
    font=("Segoe UI", 12, "bold"),
    foreground="white",
    background="#347433",
    padding=3,
    relief="groove" ,
   
 )
 style.map("ajouter.TButton",
    background=[("active", "#FF9A9A")],
    foreground=[("active", "white")]
 )

 ajouter_button = ttk.Button(
    scrollable_frame,
    text="Ajouter",
    command=add_ind,
    style="ajouter.TButton"
 )

 ajouter_button.grid(row=2, column=2, sticky="e",padx=5, pady=5)






































