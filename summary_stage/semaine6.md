#### tasks
1. Learn xml.etree to treat xml files
2. regrouper les pièces par nouveaux méta-données (sortie csv)
3. vérifier comment changer isalpha()

#### notes xml.etree

```python
root = getroot() # root of the nodes
root.findall("nodename") # find all tags with the "nodename" (direct children only)
root.find("nodename") # find the first tag with "nodename" (direct children only)

root.iter("tag name") # C'est la plus utilises

node.tag        ->      tagname
node.attrib     ->      attribute name
node.text       ->      text
```

#### faire les fichiers csv avec nouveaux méta-données

speaker,sex,text

hans,M,"Hans :
Wenn ich numme ellaan uff d'r Welt wär. Ach, jetzt brüehlt d'Kueh aunoch !
"

```
python3 pieces_more_info/script/emo_xml_treat.py nom_de_pieces_theatres
```

BUGs:
```xml
<personGrp xml:id="alli" sex="UNKNOWN">
            <persName>Alli</persName>
          </personGrp>
          <personGrp>
            <persName>Zwei Page, Mickeymies, hochi Staatsbeamti, Diener un Dienere biem Maharadscha, e
            Drache</persName>
          </personGrp>
parfois, il y a des tags sans attributs
```
```
greber-d-jumpfer-prinzesse.xml  xml.etree.ElementTree.ParseError: not well-formed (invalid token): line 8, column 46
greber-lucie.xml xml.etree.ElementTree.ParseError: not well-formed (invalid token): line 8, column 74

pas bien forme, peut pas construire l'arbre xml

```
Le problem est à cause de l'encodage, dans ces deux articles,
<?xml version='1.0' encoding='utf8'?>, utf8 est utilisé au lieu de UTF-8, donc les lettres comme ü, ß ne peuvent pas être lu.

Dans arnold-der-pfingstmontag, 
<person xml:id="christinel" sex="F">
<sp who="#christinle">
<speaker>Christinel</speaker>
<stage>eintretend</stage>
Le nom de personnage est different, je prends "christinel" comme le vrai nom

<sp who="#rosine #prechtere">
    <speaker>Fr. Rosine, Fr. Prechtere</speaker>
    <stage>zugleich</stage>
    <l>Guede Daa, Frau Bas. Isch Si wohl uf?</l>
</sp>
id melange...