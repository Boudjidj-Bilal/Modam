import pandas as pd

# Récupération des datasets :
df_pays = pd.read_csv("csv_tab/pays.csv")
df_pays_ue = pd.read_csv("csv_tab/pays_ue.csv")
df_categorie_substance = pd.read_csv("csv_tab/categorie_substance.csv")
df_import = pd.read_csv("csv_tab/tab_importation.csv")
df_categorie4 = pd.read_csv("csv_tab/liste_categorie4.csv")
# Liste des chemins des fichiers CSV exportation
fichiers_csv_export = ['csv_tab/tab_exportation/tab_exportation.csv', 'csv_tab/tab_exportation/tab_exportation2.csv', 'csv_tab/tab_exportation/tab_exportation3.csv', 'csv_tab/tab_exportation/tab_exportation4.csv', 'csv_tab/tab_exportation/tab_exportation5.csv']
# Importer tous les DataFrames dans une liste appelée df_export
df_export = [pd.read_csv(fichier) for fichier in fichiers_csv_export]

""" Fonction qui retourne toutes les substances et tous les pays """
def substances_pays():
    substance = df_categorie_substance["Substance"]
    pays = df_pays["Pays"]
    return substance, pays

""" Fonction qui prend une substance en paramètre, et qui retourne sa catégorie """
def categorie_substance(substance_form):
    categorie = df_categorie_substance[df_categorie_substance["Substance"] == substance_form]
    categorie_substance = int(categorie["Catégorie"].drop_duplicates())
    return categorie_substance

""" Fonction qui prend une substance et un pays en paramètre, et qui retourne ae=True si l'utilisateur a besoin d'une autorisation d'exportation, et False sinon. """
def exportation(pays_form, substance_form, ae):
    # Ici on gère les autorisations d'exportations
    # Accès à chaque DataFrame d'exportation dans une boucle
    for i, df_ae in enumerate(df_export):
        # Vérifier si la colonne existe
        if substance_form in df_ae.columns:
            # Vérifier si le pays est présent dans la colonne
            if (df_ae[substance_form].values == "All").any():
                ae = True
                break
            elif pays_form in df_ae[substance_form].values:
                    ae = True
                    break
    return ae

""" Fonction qui prend une substance et un pays en paramètre, ainsi que des variables pour l'affichage du message, elle retourne ai=True si l'utilisateur a besoin d'une autorisation d'importation, et False sinon, ainsi que les variables d'affichage. """
def importation(pays_form, substance_form, import_interdite, ai, ai_general, pas_info):
    # Ici on gère les autorisations d'importations
    # Si le pays existe dans le tableau des imports :
    if pays_form in df_import['Gouvernement'].values:

        df_pays_import = df_import[df_import["Gouvernement"] == pays_form]
        # if la substance existe en tant que colonne
        if substance_form in df_import.columns:
            df_pays_import = df_pays_import[substance_form]
            num_import = str(df_pays_import.iloc[0])
    
            if num_import == "0" or num_import == "1" or num_import == "2": 
                pass # Ne fait rien
            elif num_import == "P":
                import_interdite = True
            #elif num_import == "nan" or num_import == "NULL":
            #    pass
            elif num_import == "3" or num_import == "X" or num_import == "4" or num_import == "Y":
                ai = True
                if num_import == "3" or num_import == "X":
                    ai_general = True
            else: 
                pas_info = True
        else:
            pas_info = True
    return import_interdite, ai, ai_general, pas_info

""" Fonction qui prend un pays en paramètre, et qui retourne ai=True si l'utilisateur a besoin d'une autorisation d'importation, et False sinon.
    Les substances de catégorie 4 ont toujours besoin d'une AE sauf si c'est un pays de l'Union Européenne. Il y a des messages spécifiques pour le Liban et la Suisse.
"""
def categorie4(pays_form, pays_ue_c4, ae, ai, exception_liban, exception_Suisse, pas_info):
    if pays_form in df_pays_ue["Pays"].values:
        pays_ue_c4 = True
    else:
        ae = True # Toujours une autorisation d'exportation pour les catégories 4
        # Vérifier si le pays est le Liban ou la Suisse car il y a une exception pour ces pays.
        if pays_form == "Liban":
            exception_liban = True 
        elif pays_form == "Suisse":
            exception_Suisse = True
        # Vérifier si le pays a une autorisation d'importation
        elif pays_form in df_categorie4['Pays'].values:
            ligne_pays = df_categorie4[df_categorie4['Pays'] == pays_form]
            if ligne_pays["Autorisation d'importation nécessaire"].values[0] == 'x':
                ai = True
            elif ligne_pays["Pas d'information"].values[0] == 'x':
                pas_info = True
    return pays_ue_c4, ae, ai, exception_liban, exception_Suisse, pas_info


""" Fonction qui prend en paramètre toutes les variables pour choisir le bon message en fonction de la substance et du pays. Elle retourne le message."""
def message_final(ae, ai, import_interdite, ai_general, exception_liban, exception_Suisse, pays_ue_c4, pas_info):
    # Message final :
    message = ""
    if exception_liban:
        message =  "Autorisation d'exportation requise. Au Liban, les préparations à base d'éphédrine ou de pseudoéphédrine contenant moins de 120 mg calculés en dose sont exemptées d'autorisation d'importation. "
    elif exception_Suisse:
        message = "Autorisation d'exportation requise. En Suisse les préparations à base de pseudoéphédrine contenant moins de 50 mg calculée en base sont exemptées d'autorisation d'importation."
    elif ai:
        if ai_general:
            if ae:
                message = "Autorisation d'exportation + autorisation d'importation (général valide) nécessaires."
            else:
                message = "Pas d'autorisation d'exportation requise, mais autorisation requise (général valide) à l'importation."
        else:
            if ae:
                    message = "Autorisation d'exportation + autorisation d'importation (spécifique) nécessaires."
            else:
                message = "Pas d'autorisation d'exportation requise, mais autorisation requise (spécifique) à l'importation."
    else:
        if import_interdite:
            if ae:
                message = "Importation interdite à destination + autorisation d'exportation."
            else:
                message = "Importation interdite à destination et pas d'autorisation d'exportation." #
        elif pas_info:
            if ae:
                message = "Autorisation d'exportation requise mais pas d'information à l'importation."
            else:
                message = "Pas d'autorisation d'exportation requise et pas d'information à l'importation."
        else:
            if ae:
                message = "Autorisation d'exportation requise sans autorisation à l'importation."
            else:
                if pays_ue_c4:
                    message = "Pas d'autorisation requise pour la catégorie 4 au sein de L'Union Européenne."
                else:
                    message = "Pas d'autorisation requise au titre de la réglementation sur les précurseurs."
    return message 


def create_csv_rendu(substances, pays, messages):
    # Création d'un DataFrame avec les données fournies
    df = pd.DataFrame({
        'Pays': pays,
        'Substance': substances,
        'Message': messages
    })
    # Enregistrement du DataFrame en fichier CSV
    df.to_csv('modam.csv', index=False)  # 'index=False' pour éviter d'ajouter l'index comme colonne supplémentaire
    print("Le fichier 'modam.csv' a été créé avec succès.")
    """Pour utiliser la fonction to_excel il faut lancer la commande dans le venv : pip install openpyxl"""
    df.to_excel('modam.xlsx', index=False)  # 'index=False' pour éviter d'ajouter l'index comme colonne supplémentaire

    print("Le fichier 'rendu.xlsx' a été créé avec succès.")
    return True 


def csv_rendu():
    substances, pays = substances_pays()
    substances_list = []  # Liste pour stocker toutes les substances
    pays_list = []        # Liste pour stocker tous les pays
    messages = []

    for pay in pays:
        for sub in substances:
            # print(sub)
            categorie = categorie_substance(sub)

            # Instanciation des variables pour le message final:
            ae = False # autorisation d'exportation, False = autorisation pas demmandé
            ai = False # autorisation d'importation, False = autorisation pas demmandé
            import_interdite = False
            ai_general = False
            exception_liban = False
            exception_Suisse = False
            pays_ue_c4 = False
            pas_info = False


            if categorie == 4: # Catégorie 4
                pays_ue_c4, ae, ai, exception_liban, exception_Suisse, pas_info = categorie4(pay, pays_ue_c4, ae, ai, exception_liban, exception_Suisse, pas_info)

            else: # catégorie 1, 2, 3
                import_interdite, ai, ai_general, pas_info = importation(pay, sub, import_interdite, ai, ai_general, pas_info)
                if categorie == 1: # catégorie 1
                    ae = True
                else: # catégorie 2 et 3 
                    ae = exportation(pay, sub, ae)
            message = message_final(ae,ai,import_interdite,ai_general,exception_liban,exception_Suisse,pays_ue_c4,pas_info)

            # Ajouter les informations dans les listes
            substances_list.append(sub)
            pays_list.append(pay)
            messages.append(message)
    rendu = create_csv_rendu(substances_list, pays_list, messages)
    return rendu 