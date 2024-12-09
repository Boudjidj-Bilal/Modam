# Application Modam

#### Mots clés :
AE = Autorisation d'exportation
AI = Autorisation d'exportation
## 1. Explication :

L'application Modam est une simple page contenant un formulaire où l'on peut choisir un pays ainsi qu'un précurseur. Le résultat de ces deux champs retournera à l'utilisateur s'il a besoin d'une autorisation d'importation et d'exportation ou pas.

## 2. Architecture :

L'application Modam est un projet Django codé avec le language informatique Python. Django utilise des APP, chaque APP est dédiée à un outil de l'application (exemple : la gestion des utilisateurs). Une APP utilise une structure de fichier MVT(Model Views Templates).
- Model : Objet permettant de récupérer des informations dans la base, models.py
- Views : views.py Fichier recevant les requêtes, faisant appel aux fonctions et qui retourne les résultats des requêtes aux pages html, ou rend des pages html simplement. Urls.py gère toutes les urls du site, utils.py Fichier contenant toutes les fonctions pour faire des traitements, récupérer des données, etc.
- Templates : Dossier contenant toutes les pages html du projet.

## 3. Fichier CSV :

Les fichiers csv se trouvent dans le répertoire csv_tab à la racine du projet.
- tab_exportation : Répertoire contenant plusieurs fichiers csv. Celui-ci contient tous les pays qui demandent une autorisation d'exportation en fonction de la substance. Si un pays n'apparaît pas dans l'un des tableaux, alors le pays n'a pas besoin d'une autorisation d'exportation pour les substances apparaissant dans ce même tableau.
- categorie_substance.csv : Fichier contenant toutes les substances et la catégorie qui leur sont associée.
- pays_ue.csv : Fichier contenant tous les pays actuels de l'Union Européenne.
- pays.csv : Fichier contenant tous les pays.
- tab_importation.csv : Fichier contenant certaines substances de catégorie 1, de catégorie 2 et de catégorie 3, ainsi que certains pays. La combinaison des deux nous donne un numéro qui nous permettra de savoir si, pour un produit et une substance, on a besoin oui ou non d'une autorisation d'importation.

## 4. Fonctionnement : 

- Html = Page du formulaire, fichier formulaire.html
- Urls = Fichier urls.py
- Views = Fichier views.py

### 4.1 Affichage de la page du formulaire :

Html : L'utilisateur choisit sur la page un pays et un précurseur (substance).
Urls : L'urls retourne la requête avec ses paramètres à la views.
Views : 
- La views reçoit une requête d'affichage simple du formulaire
- Elle fait appel à la fonction substances_pays() du fichier utils.py, pour récupérer tous les pays et toutes les substances pour le formulaire.
- Elle retourne les pays et les substances à la page html du formulaire
Html: Affiche le formulaire.

### 4.2 Récupération des AE/AI pour un pays et une substance :

Html : L'utilisateur choisi sur la page un pays et un précurseur (substance).
Urls : L'urls retourne la requête avec ses paramètres à la views.
Views : 
- La views reçoit une requête et récupère le pays et la substance. Elle instancie les variables dont elle aura besoin à False.
- Elle fait appel au fichier utils.py, à la fonction categorie_substance(), qui prend une substance en paramètre, elle retourne la catégorie de la substance.
- Elle vérifie si la catégorie est la 1, si oui, on a besoin d'une AI et d'une AE.
- Si ce n'est pas une catégorie 1. Elle vérifie si la catégorie est la 4, si oui on fait appel à la fonction categorie4(), qui prend une substance en paramètre, le pays et certaines variables dont elle aura besoin, elle retourne les ae/ai et d'autres variables pour l'affichage.
- Si ce n'est pas non plus une catégorie 4. Cela veut dire que la catégorie est la 2 ou la 3. Elle fait donc appel à la fonction importation(), qui prend un pays et une substance en paramètre ainsi que certaines variables dont elle aura besoin, elle retourne l'ai et d'autres variables pour l'affichage. Elle fait ensuite appel à la fonction exportation(), qui prend un pays, une substance et l'ae en paramètre, elle retourne l'ae. 
- Lorsqu'elle a déterminé si on avait besoin d'une ai, d'une ae, s'il n'y a pas d'information, etc. Elle fait appel à la fonction message_final() qui prend toutes les variables en paramètre et, en fonction des valeurs de celles-ci, elle retourne un message.
- Elle fait appel à la fonction substances_pays() pour récupérer tous les pays et toutes les substances pour le formulaire.
- Elle retourne les pays, les substances et le message à la page html du formulaire
Html: Affiche le formulaire et le message obtenu.

## 5. En cas de changement :

Par exemple, si un pays est sorti de l'Union Européenne, ou est entré dans l'Union Européenne, il suffit d'aller dans le fichier csv pays_ue.csv et d'ajouter ou d'enlever un pays.
S'il y a un nouveau précurseur, il suffit de l'ajouter dans le tableau des categorie_substance, de l'ajouter dans d'autres fichiers csv si besoin et de faire les modifications adéquates dans les autres fichiers csv.

## 6. Le design de l'aplication :

Le design de l'application est basé principalement sur un formulaire simple. Celui-ci utilise des class de designs de Bootstrap.