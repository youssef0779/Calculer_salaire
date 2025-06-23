from docxtpl import DocxTemplate
from database import create_connection

# Load your .docx template
def imprimer(employe,salaire_base,al_fam,brute1,brute,css,imposable,impots,sal,jrs,mois,ans):
 

 connection=create_connection()
     
 curs= connection.cursor()

 curs.execute("SELECT * FROM employe")
 db_employe= curs.fetchall()



 curs.execute("SELECT * FROM postes where id=?",(employe[8],))
 db_poste= curs.fetchall()
 name_ind_list=db_poste[0][3].split(",")

 ind_list=db_poste[0][4].split(",")
 sal_ind_list=[]

 sa_ind_list=[]
 base=[]
 if len(db_poste[0][4])>0:
  for i in ind_list:
    sal_ind=(int(i)/100) * salaire_base
    sa_ind_list.append(sal_ind)
    base.append(salaire_base)

 
 
 name_indda_list=db_poste[0][5].split(",")
 indda_list=db_poste[0][6].split(",")
 inddap_p_list=db_poste[0][7].split(",")

 sa_indda_list=[]
 sal_indda=[]
 

 if len(db_poste[0][6])>0 or len(db_poste[0][7])>0:
  for i,j in zip(indda_list,inddap_p_list):
    sal_indda=(int(j)/100) * int(i)
    sa_indda_list.append(sal_indda)

 print("name_ind_list :",name_indda_list)
 print("str(sa_ind_list) :",sa_ind_list)
 
 name_indda_autre_list=employe[9].split(",")
 indda_autre_list=employe[10].split(",")
 inddap_p_autre_list=employe[11].split(",")

 sa_indda_autre_list=[]
 sal_indda_autre=[]
 sa_indda_autre=[]
 if len(employe[9])>0 or len(employe[10])>0 or len(employe[11])>0:
  for i,j in zip(indda_autre_list,inddap_p_autre_list):
    sal_indda_autre=(int(j)/100) * int(i)
    sa_indda_autre.append(sal_indda_autre)

 ind_s_exists = len(db_poste[0][3]) > 0 or len(db_poste[0][4]) > 0
 ind_da_exists = len(db_poste[0][5]) > 0 or len(db_poste[0][6]) > 0 or len(db_poste[0][7]) > 0
 ind_da_autre_exists = len(employe[9]) > 0 or len(employe[10]) > 0 or len(employe[11]) > 0

# Case 0: Only specific indices
 if ind_s_exists and not ind_da_exists and not ind_da_autre_exists:
    doc = DocxTemplate("fiche_0.docx")

# Case 1: Specific + internal additional
 elif ind_s_exists and ind_da_exists and not ind_da_autre_exists:
    doc = DocxTemplate("fiche_1.docx")

# Case 2: Specific + external additional
 elif ind_s_exists and not ind_da_exists and ind_da_autre_exists:
    doc = DocxTemplate("fiche_2.docx")

# Case 3: All present
 else:
    doc = DocxTemplate("fiche_3.docx")

 if (jrs==""):
   jrs="0"


 sal_jrs=sal/30
 salary=sal_jrs*int(jrs)


 context = {
    'name'   : employe[1],
    'name_ind_list': name_ind_list,
    'poste': employe[3],
    'ind_list': ind_list,
    'sa_ind_list': [round(val, 2) for val in sa_ind_list],
    'name_indda_list': name_indda_list,
    'indda_list':indda_list,
    'inddap_p_list': inddap_p_list,
    'sa_indda_list': [round(val, 2) for val in sa_indda_list],
    'base': base,
    'ccp'   : employe[15],
    'num_emp': employe[16],
    'nss' : employe[14],
    'date_en': employe[13],
    'date_nai': employe[12],
    'enfant': employe[6],
    'enfant10': employe[7],
    'marie': employe[5],
    'nom_poste': employe[3], 
    'indda_autre': indda_autre_list, 
    'name_indda_autre': name_indda_autre_list,   
    'indda_autre_p':inddap_p_autre_list,
    'sa_indda_autre': [round(val, 2) for val in sa_indda_autre],
    'brute1': round(brute1,2),
    'al_fam': al_fam,
    'css': round(css,2),
    'imposable': imposable,
    'impots': round(impots,2),
    'salary': round(salary,2),
    'brute': round(brute+al_fam,2),
    'retenue_t': round(css+impots,2),
    'jrs':jrs,
    'mois': mois,
    'ans': ans,  
    }
  
# Render the document with the data
 doc.render(context)

# Save final document
 doc.save("fiche"+f"_{employe[1]}"+".docx")
