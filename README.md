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

## Tutoriel

#### Visualisation pour les émotions

Dans repetoire "emo_analyse" et "emo_idf_analyse", il y a un fichier *graphic.py*, qui gère les résultats d'analyse des pièces de théâtre.

*demonstration:*

``` shell
python3 graphic.py arg1 arg2 arg3 arg4
```
**arg1**: 
Les valeurs possible: single / group / most_positive / most_negative
	**single**: 
	analyser des pièces détaillées. Dans ce mode, **arg2** c'est nom de pièce. S'il y a plusieurs pièces à analyser, il faut séparer les noms par ",". **arg3** c'est émotions, séparé par "," aussi. **arg4** c'est filtre(noms des cotonnes dans fichiers csv). il est possible d'analyser
	1. la progression des émotions dans plusieurs pièces
	*exemple*
	```
	python3 graphic.py single weber-yo-yo,greber-lucie joy,sadness
	```
	![emo_progress](graphics/demonstration/emo_progress.png)
	2. Les émotions des personnages, genres, travails, classe-sociale etc.
	*exemple*
	```
	python3 graphic.py single weber-yo-yo,greber-lucie joy,sadness speaker
	```
	![with-filters](graphics/demonstration/with-filters.png)
**group**: analyses des pièces au niveau macro. **arg2** peut être soit noms des pièces de théâtre séparé par ",", (dans cette situation, il analyse des émotions que pour les pièces indiqués) soit "--émotion", soit "--shortName".
**arg3** sera des émotions séparés par "," si arg2 est "--émotion" ou noms des pièces, sinon, arg3 sera nom de la pièce. **arg4** est type de drama (comedy, drama, tale, horror), et cet argument n'est pas obligatoire pour réaliser un plot.
*exemple*
1. analyser des émotions pour les pièces indiquées:
```
python3 graphic.py group weber-yo-yo,greber-lucie,am-letzte-maskebal,arnold-der-pfingstmontag joy,sadness
```
![pieces_indicated_group_plot](graphics/demonstration/pieces_indicated_group_plot.png)
2. analyser des émotions pour toutes les pièces:
```
python3 graphic.py group --émotion joy,sadness
```
![joy_sadness_percentage](graphics/demonstration/joy_sadness_percentage.png)
3. analyser des émotions pour toutes les pièces dans un même type:
```
python3 graphic.py group --émotion joy,sadness comedy
```
![comedy](graphics/demonstration/comedy.png)
4. pairplot pour obtenir toutes les informations sur toutes les émotions
```
python3 graphic.py group
```
![pairplot_same_scale](graphics/demonstration/pairplot_same_scale.png)
5. barplot pour obtenir toutes les informations des émotions sur une seule pièce
```
python3 graphic.py group --shortName am-letzte-maskebal
```
![barplot](graphics/demonstration/barplot.png)
**most_positive**
trouver la pièce la plus positive et afficher les émotions dans cette pièce par barplot
```
python3 graphic.py most_positive
```
![most_positive](graphics/demonstration/most_positive.png)
**most_negative**
trouver la pièce la plus negative et afficher les émotions dans cette pièce par barplot
```
python3 graphic.py most_negative
```
![most_negative](graphics/demonstration/most_negative.png)
