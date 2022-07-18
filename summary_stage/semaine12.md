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

#### raison pour manque de job-category:

Dans emo_xml_treat.py, y'a une faute de logique
```python
if (key in dic_person[key_p]["name"]):
                    dic_person[key_p]["job"] = dic[key][0]
                    dic_person[key_p]["job_category"] = dic[key][1]
                    dic_person[key_p]["social_class"] = dic[key][2]
                '''else:
                    dic_person[key_p]["job"] = ""
                    dic_person[key_p]["job_category"] = ""
                    dic_person[key_p]["social_class"] = ""'''
```
, avec le else, il va eraser les infos deja entree...