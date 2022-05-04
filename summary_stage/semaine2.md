tasks:
1. how to devide texts
2. rules for analysation
3. alsacien & french texts analyse
4. comparation

If really quickly: python script to extract corpus

#### étapes pour analyser le texte
*fichier lexicon_analyse/outils.py*

1. la division
	le texte est divisé en blocs, séparé par 5 phrases une bloc
2. recherche de mots-clés dans chaque bloc
	- structure de données
		dict pour sauvegarder les scores et mots
	- traitement du fichier tsv
		- sélectionner les colonnes nécessaires
		- séparer les mots dans la même cellule
			dans fichier ELAL_all.tsv, si dans la cellule il y a ";", (par exemple: *claque;applaudir*), j'utilise la fonction split pour les séparer et ajouter dans la dictionnaire.
	- ajouter dans le dictionnaire le contenu du fichier tsv
	```shell
		{
		# le dictionnaire ressemble à ça:
		'sourit': [0.9489999999999998, 0.53, 0.536, 0.0, 0.0, 0.0, 0.0, 0.682, 0.0, 0.0, 0.0], 
		'applaudir': [0.8650000000000001, 0.824, 0.464, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.562], 
		'claque': [0.323, 0.662, 0.381, 0.615, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		}
	```
	- lire le fichier texte et recherches les mots dans le dictionnaire, sauvegarder les mots-clés trouvés dans une variable *keywords*
3. calculer le score pour chaque bloc
	- calculer la somme des coefficients de chaque emotion selon les mots-clés, et trouver le coefficient le plus grand pour VAD et emotions de base.
4. comparer les résultats de deux fichiers.
	- la polarité des emotions sont ressemblants entre les deux textes.
	- les différences sont dû à la procédure de parcourir les mots-clés.
		- valence est souvent confondue avec dominance
		- certains mots-clés ont été parcouru dans un texte, mais pas dans l'autre. *"fête"*
		- *"Guete Morje"* sont parcouru comme deux mots qui ont des emotions positives, pourtant, *"Bonjour"* c'est un seule mots positive, les différences comme ça affectent le calcul d'emotions
		- mélange de français dans le texte Alsacien *"Dictionnaire"* etc. 

#### Bugs

- mots avec un comma après ne peuvent pas être parcouru ( par exemple, *Vater,*, *Ritter!*) **Fixé**
- les dernière lignes du fichier n'ont pas été parcouru **Fixé**
- affichage des mots-clés