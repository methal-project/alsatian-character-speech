#### tasks
1. ajouter jobcategory, drama type to csv files
2. fix the bug (pas pouvoir parcourir tous le texte)
3. seaborn to plot graphs of evaluations of sentiments

#### graphic

lineplot by seaborn

```shell
python3 graphic.py am-letzte-maskebal anger,anticipation,arousal,disgust,dominance,fear,joy,sadness,surprise,trust,valence speaker

python3 graphic.py am-letzte-maskebal anger,joy sex,speaker

python3 graphic.py am-letzte-maskebal anger,joy

# arg 1: nom du piece de theatre
# arg 2: les emotions (doivent etre separe par ",")
# arg 3: nom du colomn utilise pour regrouper les donnees
```
arg 1 et arg 2 sont necessaire, arg 3 optionnel


