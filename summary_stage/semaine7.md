#### tasks
1. add drama type, person infos into csv
2. modify TED slice method (isalpha())
3. re-structure files in emotion_dynamics_essaie

#### add person infos

1.  <bibl xml:id="mtl-001"> dans fichier methal-personography.xml,
    <idno type="methal" xml:id="mtl-001"/> dans pièce de théâtre,
    utilise mtl-001 pour trouver des personnages apparues dans une même pièce de théâtre.
2. utiliser Xpath pour parcourir les informations de jobs et social-class
3. combiner les informations ensemble

#### bugs
```shell
    bastian-hofnarr-heidideldum.xml
    stoskopf-dr-hoflieferant.xml
    stoskopf-ins-ropfers-apothek.xml
    hart-dr-poetisch-oscar.xml
    greber-sainte-cecile.xml
    bastian-hofnarr-heidideldum.xml
    
    #Il n'y a pas de tag "term" pour indiquer le type de la piece
```
```xml (fixed)
    stoskopf-dr-hoflieferant.xml
    <person xml:id="fritz_grinsinger" sex="MALE">
        <persName>Fritz <emph rend="italic">Grinsinger</emph></persName>
    </person>
    <person xml:id="madame_grinsinger" sex="FEMALE">
        <persName>
            <emph rend="italic">Caroline Grinsinger</emph>
        </persName>
    </person>

    Il y a <emph> dans <persName>, donc faut encore parcourir les enfants de <persName>
```
Pour parcourir les informations des personnages,
Dans repetoires tei-lustig et tei2, le <idno type="methal" xml:id="mtl-001"/> n'existe pas,
cela pose un probleme quand il y a meme noms et prenoms dans differentes pieces de theatre.

#### ted analyse:
```shell
python3 avgEmoValues.py --dataPath ../pieces_more_info/treated_files/bastian-dr-hans-im-schnokeloch.out.csv --lexPath ELAL-als-lexicon.csv --lexNames valence dominance arousal anger anticipation disgust fear joy sadness surprise trust --savePath bastian-dr-hans-im-schnokeloch
```
