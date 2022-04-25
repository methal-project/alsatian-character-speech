corpus-methal-all
-----------------

- Sources pour stages TAL et théâtre alsacien
- Les sources étaient originalement dans plusieurs dépôts dépendamment de leur origine et elles ont été collectées ici pour faciliter la manipulation

## Contenu

Chaque dossier contient les ressources suivantes :
- **pieces**
	- **html** : Pièces pour lesquelles l'OCR a été corrigé à la main par une personne, mais pour lesquelles aucun document TEI n'a été publié (des fichiers TEI existent, dans le dossier *tei2* décrit ci-dessous, mais ils n'ont pas encore été publiés)
	- **tei** : les pièces encodées en TEI qui ont été publiées sur [GitLab](https://git.unistra.fr/methal/methal-sources) Unistra et sur [Nakala](https://nakala.fr/collection/10.34847/nkl.feb4r8j9). La source première est une numérisation en mode image de ressources sur [Numistral](https://www.numistral.fr/services/engine/search/sru?operation=searchRetrieve&exactSearch=false&collapsing=true&version=1.2&query=(colnum%20adj%20%22BNUStr058%22)&suggest=10&keywords=), pour lesquelles nous avons effectué l'OCR, sa correction et l'encodage TEI
	- **tei-lustig** : pièces en TEI dont la source est des documents sur [Wikisource](https://als.wikipedia.org/wiki/Text:August_Lustig/A._Lustig_S%C3%A4mtliche_Werke:_Band_2), en format wiki-markup. Il s'agit des œuvres complètes d'August Lustig. Elles ont été transformées en TEI par script lors d'un stage en 2021
	- **tei2** : pièces en TEI pas encore publiées par le projet. Utilisables sachant que :
	  - Il y a eu moins de validation que pour les pièces publiées
	  - Il y aura donc plus d'erreurs que dans ces dernières
	  - Il manque de gérer les traits d'union en fin de ligne (donne un pourcentage de mots mal découpés)
- **autres**
	- **db** : Base de données sqlite pour Django, pour l'application sur https://methal.eu/ui/ Pas certain si ça peut être utile pour ce projet
	- **md** : Export du classeur en ligne qui contient les métadonnées
	- **personography** : personographie en TEI pour les pièces du corpus pour lesquelles les personnages ont été transcrits. Pas certain si utile pour le projet

- **code**
	- Code d'analyse du corps par @hyang1 ainsi que des résultats d'analyse et corpus reformaté par lui (p. ex. des dataframes avec le contenu du corpus et avec les métadonnées déjà intégrées)
	- Contenu de ce dossier et sous-dossiers sont encore à documenter


## Métadonnées pour les pièces

- Ce [classeur](https://docs.google.com/spreadsheets/d/1_xUK1uP209UCjJ9agqr_Zik65u08A8rOAVo53PTtj8Y/edit#gid=731925022) google docs contient les infos originales
	- Si pas accès, svp demander l'ajout avec son adresse gmail à pruizf
		- En attendant, le dossier [autres/md](./autres/md) contient un export récent du classeur
	- La colonne `shortName` de l'onglet `pieces` correspond aux noms de fichiers utilisés dans les différents dossiers de ce dépôt. Pour les documents où l'ID de la pièce n'est pas mentionné (c.à.d. les HTML et les tei-lustig), cette colonne devrait servir à obtenir les métadonnées pour le document en croisant avec le nom du fichier. Autrement, avec l'ID de la pièce on peut croiser avec la colonne `id` de l'onglet `pieces`
	- C'est à partir de ce classeur que la BD Django est générée. Des scripts créent des "fixtures" pour import dans la BD
