import tkinter as tk
from database import create_connection
from database import save_user
import list_employe
import employe_page
from tkinter import messagebox
from imprimer import imprimer

import tkinter.ttk as ttk

import math



def calculer(employe,reduction,rendement_p):  # user is a tuple like (id, name, grade, ...)
    window = tk.Toplevel()
    window.title(f"Calcul de salaire de - {employe[1]}- {employe[16]}")

    # ✅ Make window size dynamic with screen resolution
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry("620x600")

    BG_COLOR = "#D3D3D3"
    FG_COLOR = "black"

    window.configure(bg=BG_COLOR)

    # ========== Scroll Setup ==========
    main_canvas = tk.Canvas(window, bg=BG_COLOR)
    main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ✅ Add horizontal scrollbar (nothing else changed)
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



    connection=create_connection()
     
    curs= connection.cursor()

    curs.execute("SELECT * FROM employe")
    db_employe= curs.fetchall()

    curs.execute("SELECT * FROM postes where id=?",(employe[8],))
    db_poste= curs.fetchall() 

    


    c="0"
    index_p=0
    index_po=0
    poste_s_list=db_poste[0][8].split(",") 
    for i in range(0,len(poste_s_list)):
        if (employe[4]==poste_s_list[i]):
         c=i
         index_po=db_poste[0][9].split(",")
         index_p=int(index_po[c])
         break
   

        
    echelon=int(employe[2])
    categorie=db_poste[0][2]
    ind_s_s=0
    ind_enfant=0
    ind_enfant10=0

    if (employe[5]=="Marié") and (int(employe[6])==0):
      ind_s_s=5.5
    elif (employe[5]=="Marié") and (int(employe[6])>0):
      ind_s_s=800
    
    if (int(employe[6])>0):
      ind_enfant=300*int(employe[6])
    
    if (int(employe[7])>0):
      ind_enfant10=11.25*int(employe[7])

    ind_enfant_t=ind_enfant+ind_enfant10
    ifc=1500
    if (categorie=="1") :
       index_echelon=[0,20,40,60,80,100,120,140,160,180,200,220,240]
       index=400
       ifc=7700
       iemad=1800
    elif (categorie=="2") :
       index_echelon=[0,21,42,63,84,105,126,147,168,189,210,230,251]
       index=419
       ifc=7400
       iemad=1980
    elif (categorie=="3") :
       index_echelon=[0,22,44,66,88,110,132,154,176,198,220,242,264]
       index=440
       ifc=6900
       iemad=2160
    elif (categorie=="4") :
       index_echelon=[0,23,46,69,93,116,139,162,185,208,232,255,278]
       index=463
       ifc=6400
       iemad=2340
    elif (categorie=="5") :
       index_echelon=[0,24,49,73,98,122,146,171,195,220,244,268,293]
       index=488
       ifc=5700
       iemad=2700
    elif (categorie=="6") :
       index_echelon=[0,26,52,77,103,129,155,180,206,232,258,283,309]
       index=515
       ifc=5000
       iemad=2880
    elif (categorie=="7") :
       index_echelon=[0,27,55,82,110,137,164,192,219,247,274,301,329]
       index=548
       ifc=3800
       iemad=3150
    elif (categorie=="8") :
       index_echelon=[0,29,58,87,116,145,174,203,232,261,290,318,347]
       index=579
       ifc=3800
       iemad=3330

    elif (categorie=="9") :
       index_echelon=[0,31,62,93,124,155,185,216,247,278,309,340,371]
       index=618
       ifc=3100
       iemad=3600
    elif (categorie=="10"):
       index_echelon=[0,33,65,98,131,163,196,229,261,294,327,359,392]
       index=653
       ifc=3100
       iemad=3780
 
    elif (categorie=="11") :
       index_echelon=[0,35,70,105,140,175,209,244,279,314,349,384,419]
       index=698
       iemad=3600
       
    elif (categorie=="12"):
       index_echelon=[0,37,74,111,147,184,221,258,295,332,369,405,442]
       index=737
       iemad=3780
     
    elif (categorie=="13"):
       index_echelon=[0,39,78,117,156,195,233,272,311,350,389,428,467]
       index=778
       iemad=3960
    elif (categorie=="14"):
       index_echelon=[0,41,82,123,164,205,246,287,328,369,411,452,493]
       index=821
       iemad=4140
  
    elif (categorie=="15"):
       index_echelon=[0,43,87,130,173,217,260,303,346,390,433,476,520]
       index=866
       iemad=4320
      
    elif (categorie=="16"):
       index_echelon=[0,46,91,137,183,228,274,320,365,411,457,502,548]
       index=913 

    elif (categorie=="17"):
       index_echelon=[0,48,96,144,192,241,289,337,385,433,481,529,577]
       index=962


    ind=[]
    ind_list = db_poste[0][4].split(",")
    for i in range (0,len(ind_list)):
      if (len(db_poste[0][4])>0) :
       ind.append(int(ind_list[i]))
      else :
         ind=[0] 

    indda_list = db_poste[0][6].split(",")
    indda=[]
    for i in range (0,len(indda_list)):
      if (len(db_poste[0][6])>0):
       indda.append(int(indda_list[i]))      
      else :
         indda=[0] 


    indda_p_list = db_poste[0][7].split(",")
    indda_p=[]
    for i in range (0,len(indda_p_list)):
      if (len(db_poste[0][7])>0 ):
       indda_p.append(int(indda_p_list[i]))
      else :
         indda_p=[0] 


    autre_name_indda_list = employe[9].split(",")
    autre_name_indda=[]
    for i in range (0,len(autre_name_indda_list)):
       autre_name_indda.append(autre_name_indda_list[i])
  
    autre_indda_list = employe[10].split(",")
    autre_indda=[]
    for i in range (0,len(autre_indda_list)):
      if (len(employe[10])>0) :
       autre_indda.append(int(autre_indda_list[i]))
      else :
         autre_indda=[0] 

    autre_indda_p_list = employe[11].split(",")
    autre_indda_p=[]
    for i in range (0,len(autre_indda_p_list)):
      if (len(employe[11])>0) :
       autre_indda_p.append(int(autre_indda_p_list[i]))
      else :
         autre_indda_p=[0]  
     

    expe=(index_echelon[echelon]+index_p)*45
    salaire_base=index*45
    salaire_base_expe=salaire_base+expe

    rendement_t=(salaire_base_expe-index_p*45)*int(rendement_p)/100
    rendement_imposable=rendement_t-rendement_t*0.09
    rendement_impot=rendement_imposable*0.1
    rendement_par_mois=rendement_imposable-rendement_impot
    rendement=rendement_par_mois*3


    salaire_base_expe_ind_f=0
    
    for i in range (0,len(ind)):
      
      salaire_base_expe_ind=salaire_base_expe*ind[i]/100
      salaire_base_expe_ind_f=salaire_base_expe_ind_f+salaire_base_expe_ind

    indda_x_p=1
    indda_val=0
    for i in range (0,len(indda)):
      indda_x_p=indda[i]*indda_p[i]/100
      indda_val=indda_val+indda_x_p

    autre_indda_x_p=1
    autre__indda_val=0

    for i in range (0,len(autre_indda)):
      autre_indda_x_p=autre_indda[i]*autre_indda_p[i]/100
      autre__indda_val=autre__indda_val+autre_indda_x_p


    

    brute1=salaire_base_expe+salaire_base_expe_ind_f+indda_val+ifc+autre__indda_val+ind_s_s+ind_enfant_t
    brute=salaire_base_expe+salaire_base_expe_ind_f+indda_val+ifc+autre__indda_val
    imposable=brute-brute*0.09
    css=brute*0.09
    al_fam=ind_s_s+ind_enfant_t


 

    if (imposable>0) and (imposable<=30000) :
     sal=imposable
     impots=0
    else :
     x1=20000
     if (imposable-x1<20000) :
      x2=imposable-x1
   
     else :
      x2=20000
  
  
     if (imposable-x1-x2<40000):
      x3=imposable-x1-x2
   
     else :
      x3=40000
   
   
     if (imposable-x1-x2-x3<80000):
      x4=imposable-x1-x2-x3

     else :
      x4=80000
   

     if (imposable-x1-x2-x3-x4<160000):
      x5=imposable-x1-x2-x3-x4
   
     else :
      x5=160000
   
     x6=imposable-x1-x2-x3-x4-x5  
   
     imp=10*((math.floor(x2/10)*0.23)+(math.floor(x3/10)*0.27)+(math.floor(x4/10)*0.3)
      +(math.floor(x5/10)*0.33)+(math.floor(x6/10)*0.35))
     red=0.4*imp
     if (imp*0.4>=1500) :
      red=1500
     elif (imp*0.4<=1000):
       red=1000
     impot=imp-red 

     if (imposable>30000) and  (imposable<=35000) :
      impot=impot*(137/51)-(27925/8)

      
     impots=impot-impot*int(reduction)/100
     sal=imposable-impots+ind_s_s+ind_enfant_t
     



     

    def delete_employe():

      confirm = messagebox.askyesno(
        title="Confirmation",
        message="Êtes‑vous sur de vouloir supprimer cet employé ?",
        parent=window          # facultatif mais conseillé
    )
      if not confirm:           # L’utilisateur a cliqué « Non » : on annule.
        return

      connection = create_connection()
      curs = connection.cursor()
      
      curs.execute("DELETE FROM employe WHERE id_e=?", (employe[0],))
      connection.commit()
      connection.close()
      window.destroy()


      if list_employe.window:
        list_employe.window.destroy()
      list_employe.list_employe()
      if employe_page.window:
        employe_page.window.destroy()
     

      



      
    tk.Label(scrollable_frame, text="NOM :", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=24, bg="white", fg=FG_COLOR)
    nom_box.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, employe[1])
    nom_box.config(state="readonly")

    

      
    tk.Label(scrollable_frame, text="N° d'employé :", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    num_emp_box = tk.Entry(scrollable_frame, state="normal", width=24, bg="white", fg=FG_COLOR)
    num_emp_box.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    num_emp_box.insert(0, employe[16])
    num_emp_box.config(state="readonly")    

      
    tk.Label(scrollable_frame, text="Date de naissance  :", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="w", padx=5, pady=5)
    date_nai_box = tk.Entry(scrollable_frame, state="normal", width=24, bg="white", fg=FG_COLOR)
    date_nai_box.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    date_nai_box.insert(0, employe[12])
    date_nai_box.config(state="readonly")    

      
    tk.Label(scrollable_frame, text="Date  d'entrée  :", bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=0, sticky="w", padx=5, pady=5)
    date_en_box = tk.Entry(scrollable_frame, state="normal", width=24, bg="white", fg=FG_COLOR)
    date_en_box.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    date_en_box.insert(0, employe[13])
    date_en_box.config(state="readonly") 


      
    tk.Label(scrollable_frame, text="NSS :", bg=BG_COLOR, fg=FG_COLOR).grid(row=4, column=0, sticky="w", padx=5, pady=5)
    nss_box = tk.Entry(scrollable_frame, state="normal", width=24, bg="white", fg=FG_COLOR)
    nss_box.grid(row=4, column=1, padx=5, pady=5, sticky="w")
    nss_box.insert(0, employe[14])
    nss_box.config(state="readonly") 


    tk.Label(scrollable_frame, text="N° de compte :", bg=BG_COLOR, fg=FG_COLOR).grid(row=5, column=0, sticky="w", padx=5, pady=5)
    ccp_box = tk.Entry(scrollable_frame, state="normal", width=20, bg="white", fg=FG_COLOR)
    ccp_box.grid(row=5, column=1, padx=5, pady=5, sticky="w")
    ccp_box.insert(0, employe[15])
    ccp_box.config(state="readonly")






    
    c="0"
    index_p=0
    index_po=0
    poste_s_list=db_poste[0][8].split(",") 
    for i in range(0,len(poste_s_list)):
        if (employe[4]==poste_s_list[i]):
         c=i
         index_po=db_poste[0][9].split(",")
         index_p=int(index_po[c])
         
         break
  

    
    tk.Label(scrollable_frame, text="Poste superieur :", bg=BG_COLOR, fg=FG_COLOR).grid(row=7, column=0, sticky="w", padx=5, pady=5)
    poste_s_box = tk.Entry(scrollable_frame, state="normal", width=24, bg="white", fg=FG_COLOR)
    poste_s_box.grid(row=7, column=1, padx=5, pady=5, sticky="w")
    poste_s_box.insert(0,employe[4])
    poste_s_box.config(state="readonly")

    tk.Label(scrollable_frame, text="Indice du poste superieur :", bg=BG_COLOR, fg=FG_COLOR).grid(row=8, column=0, sticky="w", padx=5, pady=5)
    poste_s_box = tk.Entry(scrollable_frame, state="normal", width=8, bg="white", fg=FG_COLOR)
    poste_s_box.grid(row=8, column=1, padx=5, pady=5, sticky="w")
    poste_s_box.insert(0,index_p)
    poste_s_box.config(state="readonly")

   
    nom_ind_list = db_poste[0][3].split(",") 
    ind_list = db_poste[0][4].split(",") 
    n=9
    if (len(db_poste[0][3])>0) or (len(db_poste[0][4])>0) :
     tk.Label(scrollable_frame, text="Indemnités % :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
     
     for  nom, ind in zip(nom_ind_list, ind_list) :
        n+=1
        tk.Label(scrollable_frame, text="Nom :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=24, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, nom)
        nom_box.config(state="readonly")


      
        n+=1
        tk.Label(scrollable_frame, text="Base :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, salaire_base_expe)
        nom_box.config(state="readonly")

        
        tk.Label(scrollable_frame, text="% :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=5, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=3, padx=5, pady=5, sticky="w")
        nom_box.insert(0, ind)
        nom_box.config(state="readonly")
        n+=1
    
        tk.Label(scrollable_frame, text="Valeur :", bg="#5dbea3", fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, int(ind)*salaire_base_expe/100)
        nom_box.config(state="readonly")

        tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)

        


    n+=1
    nom_indda_list = db_poste[0][5].split(",") 
    indda_list = db_poste[0][6].split(",")
    indda_p_list = db_poste[0][7].split(",")
    if (len(db_poste[0][5])>0) or (len(db_poste[0][6])>0) or (len(db_poste[0][7])>0) :
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
        nom_box = tk.Entry(scrollable_frame, state="normal", width=5, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=3, padx=5, pady=5, sticky="w")
        nom_box.insert(0, p_indda)
        nom_box.config(state="readonly")
        n+=1

        tk.Label(scrollable_frame, text="valeur :", bg="#5dbea3", fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=10, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, int(p_indda)*int(indda)/100)
        nom_box.config(state="readonly")
        
       
        tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)
    n+=1

    tk.Label(scrollable_frame, text="Allocations familiales :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=8, bg="white", fg=FG_COLOR)
    nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, ind_s_s+ind_enfant_t)
    nom_box.config(state="readonly")
    tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)
    n+=1

    tk.Label(scrollable_frame, text="IFC :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=8, bg="white", fg=FG_COLOR)
    nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, ifc)
    nom_box.config(state="readonly")
    tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)
    n+=1
    
    if (len(employe[9])>0) or (len(employe[10])>0) or (len(employe[11])>0) :
     tk.Label(scrollable_frame, text="Autre indemnités :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
     
     for  autre_nom, autre_indda,autre_p_indda in zip(autre_name_indda_list, autre_indda_list,autre_indda_p_list) :
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
        
        tk.Label(scrollable_frame, text="% :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=5, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=3, padx=5, pady=5, sticky="w")
        nom_box.insert(0, autre_p_indda)
        nom_box.config(state="readonly")
        n+=1

        tk.Label(scrollable_frame, text="valeur :", bg="#5dbea3", fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
        nom_box = tk.Entry(scrollable_frame, state="normal", width=10, bg="white", fg=FG_COLOR)
        nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
        nom_box.insert(0, int(autre_p_indda)*int(autre_indda)/100)
        nom_box.config(state="readonly")
        
       
        tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)
        

    n+=1
    tk.Label(scrollable_frame, text="Salaire brute :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
    nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, round(brute,2))
    nom_box.config(state="readonly")
    tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)


    n+=1

    tk.Label(scrollable_frame, text="Salaire brute + Allocation familiales :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
    nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, round(brute+ind_s_s+ind_enfant_t,2))
    nom_box.config(state="readonly")
    tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)

    n+=1

    tk.Label(scrollable_frame, text="Retenues de sécurité sociale :", bg="black", fg="white",font=("sans-serif", 11, "bold")).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
    nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, round(brute*0.09,2))
    nom_box.config(state="readonly")
    tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)

    n+=1

    tk.Label(scrollable_frame, text="Salaire imposable :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
    nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, round(imposable,2))
    nom_box.config(state="readonly")
    tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)

    n+=1

    tk.Label(scrollable_frame, text="IRG :", bg="#B22222", fg="white",font=("sans-serif", 11, "bold")).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
    nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, round(impots,2))
    nom_box.config(state="readonly",highlightbackground="#B22222")
    tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)

    n+=1

    tk.Label(scrollable_frame, text="Net à payer :", bg="#16610E", fg="white",font=("sans-serif", 11, "bold")).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
    nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, round(sal,2))
    nom_box.config(state="readonly", highlightbackground="#16610E")
    tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)

    n+=1


    tk.Label(scrollable_frame, text="Rendement de 3 mois :", bg="#075B5E", fg="white",font=("sans-serif", 11, "bold")).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
    nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, round(rendement,2))
    nom_box.config(state="readonly", highlightbackground="#075B5E")
    tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)

    n+=1



    tk.Label(scrollable_frame, text="Rendement de 1 mois :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
    nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, round(rendement_par_mois,2))
    nom_box.config(state="readonly")
    tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)

    n+=1



    tk.Label(scrollable_frame, text="Salaire Net + Rendement :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    nom_box = tk.Entry(scrollable_frame, state="normal", width=15, bg="white", fg=FG_COLOR)
    nom_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")
    nom_box.insert(0, round(rendement_par_mois+sal,2))
    nom_box.config(state="readonly")
    tk.Label(scrollable_frame, text="DA", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=2, sticky="w", padx=5, pady=5)

    n+=1




    style = ttk.Style()
    style.configure("Supprimer.TButton",
     font=("Segoe UI", 10, "bold"),
     foreground="white",
     background="#B22222",
     padding=3,
     relief="groove",
     width=15
      )
    style.map("Supprimer.TButton",
     background=[("active", "#E07A5F")],
     foreground=[("active", "white")]
 )


    btn_del = ttk.Button(
      scrollable_frame,
      text="Supprimer",
      command=delete_employe,
      style="Supprimer.TButton") 


    btn_del.grid(row=n, column=1, sticky="w",padx=5, pady=10)
    

    n+=1
        
    tk.Label(scrollable_frame, text="Imprimer BULLETIN DE PAIE :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    n+=1

    tk.Label(scrollable_frame, text="Num de jrs travailés :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    jrs_box = tk.Entry(scrollable_frame, state="normal", width=10, bg="white", fg=FG_COLOR)
    jrs_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")


    n+=1

    tk.Label(scrollable_frame, text="Mois :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)

    mois_choix = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", 
              "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]

    selected_mois = tk.StringVar(value="Janvier")
    mois_menu = ttk.Combobox(scrollable_frame, textvariable=selected_mois, values=mois_choix,state="readonly")
    mois_menu.grid(row=n, column=1, padx=5, pady=5, sticky="w")
    mois_menu.configure(width=15)
    mois_menu.set("Janvier")


    n+=1

    tk.Label(scrollable_frame, text="Année :", bg=BG_COLOR, fg=FG_COLOR).grid(row=n, column=0, sticky="w", padx=5, pady=5)
    ans_box = tk.Entry(scrollable_frame, state="normal", width=10, bg="white", fg=FG_COLOR)
    ans_box.grid(row=n, column=1, padx=5, pady=5, sticky="w")

   


    def get_val():
     ans=ans_box.get()
     jrs=jrs_box.get()
     mois=selected_mois.get()
     imprimer(employe,salaire_base_expe,al_fam,brute1,brute,css,imposable,impots,sal,jrs,mois,ans)

    style.configure("imp.TButton",
     font=("Segoe UI", 10, "bold"),
     foreground="white",
     background="#347433",
     padding=3,
     relief="groove",
     width=20
      )
    style.map("imp.TButton",
     background=[("active", "#FF9A9A")],
     foreground=[("active", "white")]
 )


    imprimer_b = ttk.Button(
      scrollable_frame,
      text="BULLETIN DE PAIE",
      command=get_val ,
      style="imp.TButton") 


    imprimer_b.grid(row=n+1, column=1, sticky="w",padx=5, pady=10)