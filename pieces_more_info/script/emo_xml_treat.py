import csv
import xml.etree.ElementTree as ET
import os, sys

dir_path = "./pieces_more_info/treated_files"
xml_in = ""


def main():
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    xml_in = "./pieces_more_info/" + sys.argv[1]
    xml_out = dir_path + "/" + sys.argv[1][:-3] + "out.csv"
    tree = ET.parse(xml_in)
    root = tree.getroot()
    dic_person = person_info(root)
    list_piece = get_speaker_text(root, dic_person)
    write_csv(list_piece, xml_out)

def person_info(root):
    dic_person = {}
    dic_line = {}
    for kids in root.iter(tag="{http://www.tei-c.org/ns/1.0}personGrp"):
        if (kids):
            if (kids.attrib):
                sex = kids.attrib["sex"]
                id = kids.attrib["{http://www.w3.org/XML/1998/namespace}id"]
                dic_line["name"] = id
                dic_line["sex"] = sex
                dic_person["#" + id] = dic_line
                dic_line = {}
    for kids in root.iter(tag="{http://www.tei-c.org/ns/1.0}person"):
        sex = kids.attrib["sex"]
        id = kids.attrib["{http://www.w3.org/XML/1998/namespace}id"]
        dic_line["name"] = id
        dic_line["sex"] = sex
        dic_person["#" + id] = dic_line
        dic_line = {}
    return dic_person

def get_speaker_text(root, dic_person):
    #count = 0
    list_sp_text = []
    list_piece = []
    text = ""
    
    for kids in root.iter(tag="{http://www.tei-c.org/ns/1.0}sp"):
        #count += 1
        if (kids.attrib):
            who = kids.attrib["who"]
            if (who in dic_person):
                list_sp_text.append(dic_person[who]["name"])
                list_sp_text.append(dic_person[who]["sex"])
            else:
                list_sp_text.append("group")
                list_sp_text.append("unknown")
            for subkids in kids:
                if (subkids.text):
                    text += subkids.text + "\n"
            list_sp_text.append(text)
            text = ""
            list_piece.append(list_sp_text)
            list_sp_text = []

    return list_piece
    
def write_csv(list_piece, xml_out):
    header = ["speaker", "sex", "text"]
    with open(xml_out, "w", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(header)
        writer.writerows(list_piece)

if __name__ == "__main__":
    main()