tasks:
1. retokenize texts (spacy, als_tokenizer) into files
2. re-analyze with ELAL for als, NRC and FEEL for fr
3. average score of each emotion + graph
4. calculate correlation
5. get a log from results of als and fr

#### Tâche + fichiers de sortie:

- re-structurer les fichiers
- re-tokeniser avec spacy pour français et tokeniser pour alsacien
- amélioré les sortie en txt
- ajouté les sortie en csv
*tous les fichiers de sorties sont dans le repetoire out_files*

        Mots-clés français en ELAL et les coeffs -> mots_fr_ELAL.csv
        Mots-clés français en NRC(sans coefs intensif) et les coeffs -> mots_fr_FEEL.csv
        Moyenne des émotions par bloc pour les mots-clés français -> moyenne_fr_FEEL.csv
        Moyenne des émotions par bloc pour les mots-clés alsacien-> moyenne_als_ELAL.csv
        corrélation entre les deux moyennes de français et Alsacien -> pk.csv
        comparaison ELAL et NRC -> compare_mots_elal_nrc.csv

#### Travail pas encore fait:
- rendre lisible les codes
- comparer autres lexicons