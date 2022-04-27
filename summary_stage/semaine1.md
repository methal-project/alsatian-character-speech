## Semaine 1
personal token: glpat-RyyEgf6G5LHSjh7cVQs_

#### 1. bib abdaoui 2017
*objectif:*

    Use auto-translators to analyse sentiment
*keywords:*
```
polarity (positive, negative), 
conveyed emotions (joy, fear), 
Emotions typology(Ekman):
    six types: joy, surprise, anger, fear, sadness, disgust
French benchmarks(for evaluation)
```
*methods:*

    1. 6 automatic translators to define an emotion
    2. human translator to validate machine translations
    3. evaluate sentiments by French benchmarks

#### 2. bib schmidt et al. 2022
*objectif:*

    Use human annotation to obtain a gold standard, and machine learning to train models
*keywords:*
```
hierarchical annotation scheme
transformer_based models(for evaluation)
emotion classification algorithms
gold standard (human annotation)
```
*methods:*

    1. defined a emotional scheme
    2. annotations with sub-emotions
        two annotators for one play
        mark text sequences of varied lengths
    3. statistics of emotions based on the emotional scheme
    4. filter the corpus into 3 classifications
    5. use base-line and transformer-based ml models to do evaluation

#### 3. Mohammed Obtaining reliable human rating 2018
*objectif:*

    A new rating method for VAD, and some statistics about differences in annotations due to age, sex, personality etc.

*keywords:*
```
VAD(valence, arousal, dominance)
SHR(split-half reliability, verify if the annotation is reliable)
Best-Worst Scaling (compare N tuples (words), sort the tuples) 
```
*methods:*

    1. Select commonly used terms
    2. Use best-scaling method to annotate
    3. avoid random or malicious annotations by using gold questions.(if accuracy < 80%, change annotator)
    4. count how many times a word was chosen to determine its score
    5. do statistiques and compare results between lexicons
    6. calculate reliability and correlations of VAD

#### conclusion

**Etapes pour analyser des emotions**
1. définir une structure d'émotions de base, par exemple *Ekman*, *plutchik*, *VAD* etc.
2. définir des règles pour annotation selon la structure. *(échelle, lexicon etc.)*
3. statistique des résultats obtenu.
4. utiliser un benchmark, un modèle (ml) ou formule (*SHR par exemple*) pour vérifier les résultats.
5. conclusion.

*Comment je vais analyser:*
1. touver d'abord des mots cles dans une phrase
2. selon le lexicon d'emotion, donner l'emotion pour cette phrase avec echelle (score?)
3. selon les phrase, analyser des emotions d'une personnage 

**Structure de corpus**
**tei**

    Listperson
        person(xml:id, sex)
            persName
        personGrp(xml:id, sex)
            persName
***
    castList
        head
        castItem(corresp (id == xml:id))
            role
            roleDesc
***
    listRelation
        relation (name, mutual, active, passive)

***
    div(type)
        head
        sp
        spGrp
        div(type)

    spGrp(type, rend)
        stage
        sp(who)

    sp(who)
        speaker
        stage
        p
        pb(n)
        lg

    lg
        head
        stage
        l

***

