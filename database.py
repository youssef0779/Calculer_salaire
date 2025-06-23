import sqlite3

def create_connection():
  connection=sqlite3.connect('calcul_salaire.db')
  connection.execute("PRAGMA foreign_keys = ON")
  return connection

connection=create_connection()
curs= connection.cursor()

 
curs.execute("""
 CREATE TABLE IF NOT EXISTS postes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nom_poste TEXT ,
  catrgorie TEXT,
  nom_ind TEXT ,
  ind TEXT ,
  nom_indda TEXT,
  indda TEXT,
  p_indda TEXT,
  nom_poste_s TEXT,
  indice_poste TEXT)
  
""")

curs.execute("""
 CREATE TABLE IF NOT EXISTS employe (
  id_e INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT ,
  echelon TEXT,
  nom_poste TEXT NOT NULL,
  nom_poste_s TEXT NOT NULL ,
  marie TEXT NOT NULL,
  enfant TEXT NOT NULL,
  enfant10 TEXT NOT NULL,
  poste_id INTEGER,
  autre_indda_name TEXT,
  autre_indda TEXT,
  autre_indda_p TEXT,
  date_nai TEXT,
  date_en TEXT,
  nss TEXT,
  ccp TEXT,
  num_emp TEXT, 
  FOREIGN KEY (poste_id) REFERENCES postes(id))
""")


connection.commit()

connection.close()

def save_user():
  print("")


def save_employe(name,echelon ,nom_poste,nom_poste_s,marie,enfant,enfant10,poste_id,
autre_indda_name,autre_indda,autre_indda_p,date_nai,date_en,nss,ccp,num_emp):
    connection = create_connection()
    cursor = connection.cursor()

    # Save user
    cursor.execute("INSERT INTO employe (name,echelon ,nom_poste,nom_poste_s,marie,enfant,enfant10,poste_id,autre_indda_name,autre_indda,autre_indda_p,date_nai,date_en,nss,ccp,num_emp) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (name,echelon ,nom_poste,nom_poste_s,marie,enfant,enfant10,poste_id,
                     autre_indda_name,autre_indda,autre_indda_p,date_nai,date_en,nss,ccp,num_emp))
    connection.commit()
    connection.close()


def save_poste(nom_poste,catrgorie,nom_ind,ind,nom_indda,indda,p_indda,nom_poste_s,indice_poste):
    connection = create_connection()
    cursor = connection.cursor()

    # Save user
    cursor.execute("INSERT INTO postes (nom_poste,catrgorie,nom_ind,ind,nom_indda,indda,p_indda,nom_poste_s,indice_poste) VALUES (?,?,?,?,?,?,?,?,?)",
                   (nom_poste,catrgorie,nom_ind,ind,nom_indda,indda,p_indda,nom_poste_s,indice_poste))
    connection.commit()
    connection.close()


    
