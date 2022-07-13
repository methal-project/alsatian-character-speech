#### tasks
1. Même axe pour pairplot
2. Coeff IDF pour pièce de théâtre
3. Améliorer Readme.md
4. une dot pour scatterplot de personnage

#### calculate IDF

Tous ça sera fait dans un nouvel répertoire (emo_idf_analyse)

step 1. extraction de textes pures pour chaque pièce de théâtre (les paroles)
step 2. calculer TF-IDF pour toutes les pièces, et sauvegarder les valeurs dans un fichier csv
step 3. modifier le fichier avgEmoValues.py pour recalculer coeffs d'emotions
(coef_IDF * coef_emotion * 10)

#### pairplot

Le pairplot après le règlement des axes devient ressemblant aux scatterplot de pourcentage

```shell
python3 graphic.py group
```

#### une dot pour scatterplot par personne

```shell
python3 graphic.py single arnold-der-pfingstmontag sadness,joy speaker
```