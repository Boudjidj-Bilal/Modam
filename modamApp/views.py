from django.shortcuts import render
from . import utils as ut 

def viewFormulaire(request):
    if request.method == "POST": # Si la requête est de type post:

        # rendu = ut.csv_rendu()
        
        # Récupération du pays et du produit du formulair
        pays_form = request.POST.get("pays")
        substance_form = request.POST.get("produit")

        categorie_substance = ut.categorie_substance(substance_form)

        # Instanciation des variables pour le message final:
        ae = False # autorisation d'exportation, False = autorisation pas demmandé
        ai = False # autorisation d'importation, False = autorisation pas demmandé
        import_interdite = False
        ai_general = False
        exception_liban = False
        exception_Suisse = False
        pays_ue_c4 = False
        pas_info = False


        if categorie_substance == 4: # Catégorie 4
            pays_ue_c4, ae, ai, exception_liban, exception_Suisse, pas_info = ut.categorie4(pays_form, pays_ue_c4, ae, ai, exception_liban, exception_Suisse, pas_info)

        else: # catégorie 1, 2, 3
            import_interdite, ai, ai_general, pas_info = ut.importation(pays_form, substance_form, import_interdite, ai, ai_general, pas_info)
            if categorie_substance == 1: # catégorie 1
                ae = True
            else: # catégorie 2 et 3 
                ae = ut.exportation(pays_form, substance_form, ae)
                    
        message = ut.message_final(ae,ai,import_interdite,ai_general,exception_liban,exception_Suisse,pays_ue_c4,pas_info)

        # Récupération des pays et des substances pour le formulaire
        substance,pays =  ut.substances_pays()

        return render(request, 'formulaire.html', context={"pays":pays, "produits":substance,"message":message})
    else :

        substance,pays =  ut.substances_pays()

        return render(request, 'formulaire.html', context={"pays":pays, "produits":substance})
