corpus-methal-all
-----------------

- Sources pour stages analyse d'émotions pour les pièces théâtres alsaciennes
- Les sources étaient originalement dans plusieurs dépôts dépendamment de leur origine et elles ont été collectées ici pour faciliter la manipulation

## Contenu

Chaque dossier contient les ressources suivantes :

- **emo_analyse**
	- Résultats des analyses d'émotions pour chaque pièce de théâtre.
	- *avgEmoValues.py*, script ecrit par [EmotionDynamics](https://github.com/Priya22/EmotionDynamics/tree/master/code), pour calculer les coefficients des émotions selon un lexicon
	- *graphic.py*, script pour réaliser des analyses sur les émotions et visualiser les résultats pour les pièces théâtres
- **emo_idf_analyse**
	- Même chose avec emo_analyse mais avec coefficient idf
- **graphics**
	- Les résultats d'analyse sauvegardé en images
- **lexicon_analyse**
	- Comparaison entre différents lexicons sur une même pièce de théâtre
	- cor_als_fr_FEEL
		- corrélation entre ELAL Alsacien et FEEL français
		- coefficients d'émotions pour chaque bloc de la pièce
	- cor_fr_als_ELAL
		- corrélation entre ELAL Alsacien et ELAL français
		- coefficients d'émotions pour chaque bloc de la pièce
	- cor_fr_ELAL_FEEL
		- corrélation entre ELAL français et FEEL français
		- coefficients d'émotions pour chaque bloc de la pièce
	- cor_fr_NRC_ELAL
		- corrélation entre ELAL français et NRC français
		- coefficients d'émotions pour chaque bloc de la pièce
	- cor_fr_NRC_FEEL
		- corrélation entre NRC français et FEEL français
		- coefficients d'émotions pour chaque bloc de la pièce
	- *outils.py* : les fonctions pour parcourir les mots-clés, et pour réaliser les comparaisons entre les lexicons
	- *statistiques.py* : les fonctions pour calculer la corrélation
	- *main.py*: réaliser les analyses avec les fonctions dans outils.py et statistiques.py
- **pieces_more_info**
	- script: 
		Script pour analyser les fichiers de théâtre en XML, et sortir des fichiers en CSV avec des informations supplémentaires de personnages, type de théâtre etc.
	- tei, tei2, tei-lustig:
		Pièces de théâtre en xml sans aucun traitement
	- treated_files:
		Contien les fichiers CSV (pièces de théâtre en format .csv) traités avec des informations supplémentaires

- **summary_stage**
	Chaque semaine un fichier md pour conclure ce que j'ai fait 
- **command_list.txt**
	liste des commandes pour convertir les fichiers xml aux fichiers csv avec les informations supplémentaires
- **command_list_ed_analyse.txt**
	liste des commandes pour calculer les coefficients des émotions pour chaque pièce de théâtre
