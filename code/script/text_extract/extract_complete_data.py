from pathlib import Path
import pandas as pd
file_to_metadata = '../../data/corpus-methal-all/autres/md/personnages.ods'
file_to_csv = '../../working_dir/metadata/tei_metadata_avec_text_brut.csv'
pd.set_option('display.max_columns', 100000)
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_colwidth', 100000)
pd.set_option('display.width', 100000)
csv = pd.read_csv(file_to_csv)
pieces = pd.read_excel(file_to_metadata, sheet_name='pieces', engine='odf', usecols=['id','shortName','author','publisher','print'])
auteurs = pd.read_excel(file_to_metadata, sheet_name='auteurs', engine='odf', usecols=['concat','placeOfBirth'])
editeurs = pd.read_excel(file_to_metadata, sheet_name='editeurs', engine='odf', usecols=['name_one','place'])
places_dept = pd.read_excel(file_to_metadata, sheet_name='places', engine='odf', usecols=['place','dept'])

haut_outdir = Path('../../working_dir/text_brut/haut-rhin')
bas_outdir = Path('../../working_dir/text_brut/bas-rhin')
haut_outdir.mkdir(parents=True, exist_ok=True)
bas_outdir.mkdir(parents=True, exist_ok=True)

def complete_metadata(df_pieces,df_editeurs,df_dept,df_auteurs):

    for fn in csv.FileName:
        mtlid = 'mtl-' + df_pieces.query("shortName==@fn").id.to_string(index=False,header=False)

        author_in_meta = df_pieces.query("shortName==@fn").author.to_string(index=False,header=False)
        csv.loc[csv['FileName']==fn,'Author']=author_in_meta

        publisher = df_pieces.query("shortName==@fn").publisher.to_string(index=False,header=False)
        date_print = df_pieces.query("shortName==@fn").print.to_string(index=False,header=False)
        pub_place = df_editeurs.query("name_one==@publisher").place.drop_duplicates().to_string(index=False,header=False)

        author = csv.query("FileName==@fn").Author.to_string(index=False,header=False)
        author_birth_place = df_auteurs.query("concat==@author").placeOfBirth.to_string(index=False,header=False)

        pub_place = pub_place.split()[0]
        dept = df_dept.query("place==@pub_place").dept.to_string(index=False,header=False)

        csv.loc[csv['FileName']==fn,'IdMtl']=mtlid

        csv.loc[csv['FileName']==fn,'Publisher']=publisher

        csv.loc[csv['FileName']==fn,'datePrint']=date_print
        csv.datePrint = pd.to_numeric(csv.datePrint,downcast='integer')
        csv.dateWritten = pd.to_numeric(csv.dateWritten,downcast='integer')

        csv.loc[csv['Publisher']==publisher,'PubPlace']=pub_place

        csv.loc[csv['PubPlace']==pub_place,'PubDept']=dept

        csv.loc[csv['Author']==author,'authorPlaceOfBirth']=author_birth_place

        # output textBrut to .txt

        corpus_temp = csv.query("FileName==@fn")
        if corpus_temp.PubDept.to_string(index=False,header=False) == 'Bas-Rhin':
            textBrutBasRhin = corpus_temp.textBrut.to_string(index=False,header=False)

            p = bas_outdir / Path(fn + '.txt')
            with p.open("w") as f:
                f.write(textBrutBasRhin)

        if corpus_temp.PubDept.to_string(index=False,header=False) == 'Haut-Rhin':
            textBrutHautRhin = corpus_temp.textBrut.to_string(index=False,header=False)

            p = haut_outdir / Path(fn + '.txt')
            with p.open("w") as f:
                f.write(textBrutHautRhin)





complete_metadata(pieces,editeurs,places_dept,auteurs)
# csv = csv.reindex(columns = ['IdMtl', 'FileName', 'Title', 'Author', 'authorPlaceOfBirth', 'Publisher', 'PubPlace','PubDept','datePrint','textBrut'])
# csv = csv.reindex(columns = ['FileName','Author', 'authorPlaceOfBirth', 'PubPlace','PubDept','datePrint','textBrut'])
csv = csv.reindex(columns = ['FileName','Author', 'authorPlaceOfBirth', 'PubPlace','PubDept','datePrint'])

csv.to_csv('../../working_dir/metadata/metadata_tei.csv', index=False)
print("Done with csv")


pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.width', 100)
print(csv)