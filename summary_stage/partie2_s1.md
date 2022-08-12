#### task 1: pre-traitement des textes
Remplacer les variantes par une seule forme.

step1: 
lire lexique ELAL, faire un dictionnaire, avec chaque variante comme key et la première variante comme valeur.
*Le dictionnaire est sauvegarde dans fichier lexicon_analyse/variante_replace.csv*

step2: (Pas un step necessaire, mais c'est pour simplifier la visualisation)
Remplacer les variantes par les formes, puis sauvegarder le nouveau texte et mots remplacés
dans deux fichiers .txt. Les fichiers sont dans le répertoire *text_brut_replaced*

step3: lire le fichier rolling_mean.csv dans tous les répertoires de pièces de théâtre, prendre les colonnes "text" et "progress", faire une liste de tournes de paroles.

step4: calculer tf-idf avec la liste.


#### un problème trouvé

Dans les fichiers avant, j'ai mal utilisé alsace-tokenizer, 
```python
ret = at.RegExpTokeniser()
phrase = (ret.tokenise(block)).get_contents()
tokens = re.split(regex, phrase)
```
n'est pas correcte, il manque get_tokens, donc il doit être
```python
tokens = ret.tokenise(ori_text)
tokens = tokens.get_tokens() # mtn tokens c'est une liste des objets
for i in range(len(tokens)):
    print(tokens[i].get_contents()) # il fault utiliser get_contents() pour obtenir les valeurs des objets
```

La bibliotheque qu'on utilise a coupe des paroles, avgEmoValues.py

La commande est:

```
python3 avgEmoValues.py --dataPath ../pieces_more_info/treated_files/tei-lustig/am-letzte-maskebal.out.csv --lexPath ELAL-als-lexicon.csv --lexNames valence dominance arousal anger anticipation disgust fear joy sadness surprise trust --savePath am-letzte-maskebal
```
fichier entree: pieces_more_info/treated_files/tei-lustig/am-letzte-maskebal.out.csv
tout est bon dans fichier entree

fichier sortie:
am-letzte-maskebal/anger.csv
Une parole de Domino a ete coupe

**Pourquoi?**

Quand il n'y a pas de mots dans lexique trouve, alors il coupe la parole