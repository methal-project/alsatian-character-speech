#### amelioration

1. scatterplot & rolling mean:
J'ai essayé de remplacer les moyennes d'émotions par les pourcentage.
groupe1 : Valence, Arousal, Dominence
groupe2: Anger, anticipation, ... trust

le *pourcentage* implique la portion d'une emotion dans son groupe,
calculé par:
    sum de rolling means d'une emotion / sum de rolling means de toutes les emotions dans le groupe

L'amélioration est visible, les nouveaux scatterplots ont été mis dans repetoire [graphic_scatterplot](graphics)

**par exemple:**
*joy et sadness avec moyennes*
![joy_sadness](../graphics/joy_sadness.png)

*joy et sadness avec pourcantage*
![joy_sadness_percentage](../graphics/joy_sadness_percentage.png)

2. split play
En modifiant *split_plays.py*, mtn dans le fichier **rolling_mean.csv** de chaque repetoire,
la colonne "progress" représente le découpage.
la colonne "Unnamed 0:" a été enlevé.

3. pair plot
```
python3 graphic.py group
```

Pour regarder le pairplot de toutes les emotions
![pairplot](../graphics/pairplot.png)

