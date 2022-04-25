import sys
from pathlib import Path

from bs4 import BeautifulSoup

def read_tei(tei_file):
    with open(tei_file,'r') as tei:
        soup = BeautifulSoup(tei, 'xml')
        return soup
    raise RuntimeError('Cannot generate a soup from the input')

def elem_to_text(elem, default = ''):
    if elem:
        return elem.getText()
    else:
        return default

# @dataclass
# class Person:
#     id: str
#     sex: str
#     persName: str

class TEIFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.soup = read_tei(filename)

        self._title = ''
        self._author = ''
        self._front = None
        self._body = None

    def basename(self):
        p = Path(self.filename)
        stem = Path(self.filename).stem
        if p.parent.name == 'tei-lustig':
            stem = 'lustig-' + stem
        if stem.endswith('.tei'):
            # Return base name without tei file
            return stem[0:-4]
        else:
            return stem

    # sourceDesc
    def idnoMtl(self):
        tag_temp = self.soup.find('idno', type = 'methal')

        if tag_temp:
            idmtl = tag_temp.attrs.get('xml:id')
            self._idnoMtl = idmtl
        else:
            self._idnoMtl = tag_temp
        return self._idnoMtl

    @property
    def title(self):
        if not self._title:
            title_list = []
            for title in self.soup.bibl.find_all('title'):
                title_list.append(title.getText())
            titles = "\n".join(title_list)
            self._title = titles
        return self._title

    @property
    def author(self):
        if not self._author:
            self._author = self.soup.author.getText()
        return self._author

    def publisher(self):
        pub_temp = self.soup.bibl.publisher
        self._publisher = elem_to_text(pub_temp)
        return self._publisher

    def pubPlace(self):
        pubP_temp = self.soup.bibl.pubPlace
        self._pubPlace = elem_to_text(pubP_temp)
        return self._pubPlace

    def dateWritten(self):
        dateW_temp = self.soup.bibl.find('date', type = 'written')
        self._dateWritten = elem_to_text(dateW_temp)
        return self._dateWritten

    def datePrint(self):
        dateP_temp = self.soup.bibl.find('date', type = 'print')
        self._datePrint = elem_to_text(dateP_temp)
        return self._datePrint

    # text
    @property
    def front(self):
        if not self._front:
            self._front = self.soup.front.getText()
        return self._front

    @property
    def body(self):
        if not self._body:
            self._body = self.soup.body.getText()
        return self._body

    def textBrut(self):
        for tag_bruit in self.soup.body.find_all(['stage','pb']):
            tag_delete = tag_bruit.extract()
            # print( '被删除的标签: ', tag_delete)
        # print('stage和pb标签: ',self.soup.body.find_all(['stage','pb']))
        text_brut_list = []
        for tag in self.soup.body.find_all(['p','l']):
            text_brut_list.append(tag.getText().replace('\n',''))
            # print(j.getText())
            # print(text_brut_list)
        text_brut = ' '.join(text_brut_list)
        self._textBrut = text_brut
        return self._textBrut


def main():
    currentPath = Path.cwd()
    corpusPath = currentPath.joinpath('corpus-methal-all','pieces')
    def get_corpus():
        type_name = sys.argv[1]
        file_name = sys.argv[2]
        file_path = corpusPath.joinpath(Path(type_name),Path(file_name))
        return file_path

    tei_doc = get_corpus()
    tei = TEIFile(tei_doc)
#     print(f"\n      =====Description for this play=====\n\n\
# IdnoMethal: {tei.idnoMtl()}\n\nTitle:\n\n{tei.title}\n\nAuthor: {tei.author}\n\n\
# publisher: {tei.publisher()}\n\npubPlace: {tei.pubPlace()}\n\n\
# dateWritten: {tei.dateWritten()}\n\ndatePrint: {tei.datePrint()}\n\n\
#     =====front====={tei.front}\n\n\
# =====body====={tei.body}")



    # for i in tei.body.find_all(['stage','pb']):
    #     tag_delete = i.extract()
    #     # print( '被删除的标签: ', tag_delete)
    # print('stage和pb标签: ',tei.body.find_all(['stage','pb']))
    # text_brut_list = []
    # for j in tei.body.find_all(['p','l']):
    #     text_brut_list.append(j.getText())
    #     # print(j.getText())
    #     # print(text_brut_list)
    # text_brut = ' '.join(text_brut_list)
    # print(text_brut)


if __name__ == "__main__":
    main()