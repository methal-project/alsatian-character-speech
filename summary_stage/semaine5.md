#### tasks
1. correlation without merge
    - fr:
        - elal_fr vs nrc_fr  decimal 8 emos check
        - nrc_fr vs feel_fr  binary  6 emos check
        - feel_fr vs elal_fr binary  6 emos check
    - als:
        - elal_als vs elal_fr decimal 8 emos check
        - elal_als vs nrc_fr  decimal 8 emos check
        - elal_als vs feel_fr binary  6 emos check

    La Correlation entre elal_fr et nrc_fr est le plus haut dans groupe de "fr"

    Dans groupe de "als", la correlation entre elal_fr et elal_als est le plus haut.

    Le resultat me semble raisonable.

2. Ajouter les commentaires pour les fonctions dans outils.py

3. treat sliced text

    pourquoi nombre de tokens n'est pas vrai?
    ```python
    text.isalpha(), il reconnaît que les mots composés par pure lettres

    python3 avgEmoValues.py --dataPath sample_fr.csv --lexPath NRC-VAD-fr-lexicon.csv --lexNames Valence Dominance Arousal --savePath sample_outputs
    ```
    fixed
