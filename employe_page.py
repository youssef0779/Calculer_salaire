import tkinter as tk
from database import create_connection
from database import save_user
import list_employe
from calculer import calculer 
import tkinter.ttk as ttk

window=None
def employe__page(employe):
    global window  # user is a tuple like (id, name, grade, ...)
    window = tk.Toplevel()
    window.title(f"Page d'employé  - {employe[1]}- {employe[16]}")
    #  Make window size dynamic with screen resolution
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{int(screen_width * 0.6)}x{int(screen_height * 0.8)}")

    BG_COLOR = "#D3D3D3"
    FG_COLOR = "black"

    window.configure(bg=BG_COLOR)

    # ========== Scroll Setup ==========
    main_canvas = tk.Canvas(window, bg=BG_COLOR)
    main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #  Add horizontal scrollbar (nothing else changed)
    scrollbar_x = tk.Scrollbar(window, orient="horizontal", command=main_canvas.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

    main_canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar_x.set)

    scrollable_frame = tk.Frame(main_canvas, bg=BG_COLOR)
    canvas_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_configure(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        # Optional: make canvas_window wider if content grows
        # comment this line if you want free horizontal scrolling:
        # main_canvas.itemconfig(canvas_window, width=event.width)

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
    def calcul(): 
     
     connection=create_connection()
     
     curs= connection.cursor()

     curs.execute("SELECT * FROM employe")
     db_employe= curs.fetchall()

     curs.execute("SELECT * FROM postes where id=?",(employe[8],))



     reduction=reduction_entry.get()
     if (reduction_entry.get()==""):
       reduction="0"

     rendement_p=rendement_p_entry.get()
     if (rendement_p_entry.get()==""):
       rendement_p="30"
     
     calculer(employe,reduction,rendement_p)


   
    
    connection=create_connection()
     
    curs= connection.cursor()

    curs.execute("SELECT * FROM employe")
    db_employe= curs.fetchall()

    curs.execute("SELECT * FROM postes where id=?",(employe[8],))
    db_poste= curs.fetchall() 
    
   







    def delete_employe():
      connection = create_connection()
      curs = connection.cursor()
      
      curs.execute("DELETE FROM employe WHERE id_e=?", (employe[0],))
      connection.commit()
      connection.close()
      window.destroy()
      if list_employe.window:
        list_employe.window.destroy()
      list_employe.list_employe()
    
      
    tk.Label(scrollable_frame, text="NOM :", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=24, bg="white", fg=FG_COLOR)
    nom_box.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, employe[1])
    nom_box.config(state="readonly")

    tk.Label(scrollable_frame, text="Situation familliale :", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    marie_box = tk.Entry(scrollable_frame, state="normal", width=20, bg="white", fg=FG_COLOR)
    marie_box.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    marie_box.insert(0, employe[5])
    marie_box.config(state="readonly")   

    tk.Label(scrollable_frame, text="Nombre d'enfant :", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="w", padx=5, pady=5)
    enfant_box = tk.Entry(scrollable_frame, state="normal", width=20, bg="white", fg=FG_COLOR)
    enfant_box.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    enfant_box.insert(0, employe[6])
    enfant_box.config(state="readonly") 

    tk.Label(scrollable_frame, text="Nombre d'enfant agé > 10 :", bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=0, sticky="w", padx=5, pady=5)
    enfant10_box = tk.Entry(scrollable_frame, state="normal", width=20, bg="white", fg=FG_COLOR)
    enfant10_box.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    enfant10_box.insert(0, employe[7])
    enfant10_box.config(state="readonly")

    tk.Label(scrollable_frame, text="Poste :", bg=BG_COLOR, fg=FG_COLOR).grid(row=4, column=0, sticky="w", padx=5, pady=5)
    poste_box = tk.Entry(scrollable_frame, state="normal", width=20, bg="white", fg=FG_COLOR)
    poste_box.grid(row=4, column=1, padx=5, pady=5, sticky="w")
    poste_box.insert(0, employe[3])
    poste_box.config(state="readonly" ) 

    tk.Label(scrollable_frame, text="Categorie :", bg=BG_COLOR, fg=FG_COLOR).grid(row=5, column=0, sticky="w", padx=5, pady=5)
    categorie_box = tk.Entry(scrollable_frame, state="normal", width=20, bg="white", fg=FG_COLOR)
    categorie_box.grid(row=5, column=1, padx=5, pady=5, sticky="w")
    categorie_box.insert(0, db_poste[0][2])
    categorie_box.config(state="readonly" ) 

    tk.Label(scrollable_frame, text="Echelon :", bg=BG_COLOR, fg=FG_COLOR).grid(row=6, column=0, sticky="w", padx=5, pady=5)
    categorie_box = tk.Entry(scrollable_frame, state="normal", width=20, bg="white", fg=FG_COLOR)
    categorie_box.grid(row=6, column=1, padx=5, pady=5, sticky="w")
    categorie_box.insert(0, employe[2])
    categorie_box.config(state="readonly" ) 

    tk.Label(scrollable_frame, text="Poste superieur :", bg=BG_COLOR, fg=FG_COLOR).grid(row=7, column=0, sticky="w", padx=5, pady=5)
    poste_s_box = tk.Entry(scrollable_frame, state="normal", width=24, bg="white", fg=FG_COLOR)
    poste_s_box.grid(row=7, column=1, padx=5, pady=5, sticky="w")
    poste_s_box.insert(0, employe[4])
    poste_s_box.config(state="readonly")
    
    c = None

    poste_s_list=db_poste[0][8].split(",") 
    for i in range(0,len(poste_s_list)):
        if (employe[4]==poste_s_list[i]):
         c=i
         break
    indice=db_poste[0][9].split(",") 
    
    tk.Label(scrollable_frame, text="Indice du poste superieur :", bg=BG_COLOR, fg=FG_COLOR).grid(row=8, column=0, sticky="w", padx=5, pady=5)
    poste_s_box = tk.Entry(scrollable_frame, state="normal", width=10, bg="white", fg=FG_COLOR)
    poste_s_box.grid(row=8, column=1, padx=5, pady=5, sticky="w")
    poste_s_box.insert(0,indice[c] if c is not None and c < len(indice) else "0")
    poste_s_box.config(state="readonly")



    tk.Label(scrollable_frame, text="N° d'employé :", bg=BG_COLOR, fg=FG_COLOR).grid(row=9, column=0, sticky="w", padx=5, pady=5)
    num_emp_box = tk.Entry(scrollable_frame, state="normal", width=20, bg="white", fg=FG_COLOR)
    num_emp_box.grid(row=9, column=1, padx=5, pady=5, sticky="w")
    num_emp_box.insert(0, employe[16])    
    num_emp_box.config(state="readonly")



    tk.Label(scrollable_frame, text="Date de naissance :", bg=BG_COLOR, fg=FG_COLOR).grid(row=10, column=0, sticky="w", padx=5, pady=5)
    date_nai_box = tk.Entry(scrollable_frame, state="normal", width=20, bg="white", fg=FG_COLOR)
    date_nai_box.grid(row=10, column=1, padx=5, pady=5, sticky="w")
    date_nai_box.insert(0, employe[12])
    date_nai_box.config(state="readonly")


    tk.Label(scrollable_frame, text="Date d'entrée :", bg=BG_COLOR, fg=FG_COLOR).grid(row=11, column=0, sticky="w", padx=5, pady=5)
    date_en_box = tk.Entry(scrollable_frame, state="normal", width=20, bg="white", fg=FG_COLOR)
    date_en_box.grid(row=11, column=1, padx=5, pady=5, sticky="w")
    date_en_box.insert(0, employe[13])
    date_en_box.config(state="readonly")
    

    tk.Label(scrollable_frame, text="NSS :", bg=BG_COLOR, fg=FG_COLOR).grid(row=12, column=0, sticky="w", padx=5, pady=5)
    nss_box = tk.Entry(scrollable_frame, state="normal", width=20, bg="white", fg=FG_COLOR)
    nss_box.grid(row=12, column=1, padx=5, pady=5, sticky="w")
    nss_box.insert(0, employe[14])
    nss_box.config(state="readonly")


    tk.Label(scrollable_frame, text="N° de compte :", bg=BG_COLOR, fg=FG_COLOR).grid(row=13, column=0, sticky="w", padx=5, pady=5)
    ccp_box = tk.Entry(scrollable_frame, state="normal", width=20, bg="white", fg=FG_COLOR)
    ccp_box.grid(row=13, column=1, padx=5, pady=5, sticky="w")
    ccp_box.insert(0, employe[15])
    ccp_box.config(state="readonly")



    nom_ind_list = db_poste[0][3].split(",") 
    ind_list = db_poste[0][4].split(",") 
    n=14
    if (len(db_poste[0][3])>0) and (len(db_poste[0][4])>0) :
     tk.Label(scrollable_frame, text="Indemnités % :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)

     for  nom, ind in zip(nom_ind_list, ind_list) :
        n+=1
        tk.Label(scrollable_frame, text="Nom :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=24, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, nom)
        nom_box.config(state="readonly")
        
        tk.Label(scrollable_frame, text="% :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=4, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=3, padx=5, pady=5, sticky="w")
        nom_box.insert(0, ind)
        nom_box.config(state="readonly")
        n+=1
    
    nom_indda_list = db_poste[0][5].split(",") 
    indda_list = db_poste[0][6].split(",")
    indda_p_list = db_poste[0][7].split(",")
    if (len(db_poste[0][5])>0) and (len(db_poste[0][6])>0) and (len(db_poste[0][7])>0) :
     tk.Label(scrollable_frame, text="Indemnités en DA :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)

     for  nom, indda,p_indda in zip(nom_indda_list, indda_list,indda_p_list) :
        n+=1
        tk.Label(scrollable_frame, text="Nom :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=24, bg="white", fg=FG_COLOR)
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



    nom_autre_indda_list = employe[9].split(",") 
    autre_indda_list = employe[10].split(",")
    autre_indda_p_list = employe[11].split(",")
    if (len(employe[9])>0) or (len(employe[10])>0) or (len(employe[11])>0) :
     tk.Label(scrollable_frame, text="Autre indemnités :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
     
     for  autre_nom, autre_indda,autre_p_indda in zip(nom_autre_indda_list, autre_indda_list,autre_indda_p_list) :
        n+=1
        tk.Label(scrollable_frame, text="Nom :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=24, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, autre_nom)
        nom_box.config(state="readonly")

        n+=1

        tk.Label(scrollable_frame, text="DA :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, autre_indda)
        nom_box.config(state="readonly")

        n+=1

        tk.Label(scrollable_frame, text="% :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=4, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, autre_p_indda)
        nom_box.config(state="readonly")
        n+=1

        
        
       
        tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)  

    n+=1
     
    tk.Label(scrollable_frame, text="Reduction sur IRG (%) :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    reduction_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR)
    reduction_entry.grid(row=n, column=1, padx=5, pady=5,sticky="w")
    tk.Label(scrollable_frame, text="%", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)
    n+=1

    tk.Label(scrollable_frame, text="%"+" de rendement :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    rendement_p_entry = tk.Entry(scrollable_frame, bg="white", fg=FG_COLOR)
    rendement_p_entry.grid(row=n, column=1, padx=5, pady=5,sticky="w")
    tk.Label(scrollable_frame, text="%", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)
   
    n+=1


    style = ttk.Style()
    style.configure("calcul.TButton",
     font=("Segoe UI", 12, "bold"),
     foreground="white",
     background="#075B5E",
     padding=3,
     relief="groove"
 )
    style.map("calcul.TButton",
     background=[("active", "#5A827E")],
     foreground=[("active", "white")]
 )

    calcul_button = ttk.Button(
     scrollable_frame,
     text="Calculer",
     command=calcul,
     style="calcul.TButton"
 )

    calcul_button.grid(row=n, column=1, sticky="nsew",padx=5, pady=10)
