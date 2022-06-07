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

    file_personography = "./pieces_more_info/methal-personography.xml"
    tree_person = ET.parse(file_personography)
    root_person = tree_person.getroot()
    
    tree = ET.parse(xml_in)
    root = tree.getroot()
    piece_id = root.find(".//{http://www.tei-c.org/ns/1.0}idno[@type='methal']")
    piece_id = "#" + piece_id.attrib["{http://www.w3.org/XML/1998/namespace}id"]
    print(piece_id)

    dic_person = person_info(root)
    dic = add_person_info(root_person, piece_id)
    dic_person = merge_dic(dic, dic_person)

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
                dic_line["job"] = ""
                dic_line["social_class"] = ""
                dic_person["#" + id] = dic_line
                dic_line = {}
    for kids in root.iter(tag="{http://www.tei-c.org/ns/1.0}person"):
        sex = kids.attrib["sex"]
        id = kids.attrib["{http://www.w3.org/XML/1998/namespace}id"]
        name = kids.find("{http://www.tei-c.org/ns/1.0}persName")
        realname = ""
        if (len(name.findall("{http://www.tei-c.org/ns/1.0}emph")) == 0):
            realname = name.text
        else:
            for kid_name in name:
                if (kid_name.text):
                    if(name.text):
                        realname = name.text.strip() + " " + kid_name.text.strip()
                    else:
                        realname = kid_name.text.strip()
        dic_line["name"] = realname
        dic_line["sex"] = sex
        dic_line["job"] = ""
        dic_line["social_class"] = ""
        dic_person["#" + id] = dic_line
        dic_line = {}
    return dic_person

def add_person_info(root, piece_id):
    flag = False
    dic = {}
    for kid in root.iter(tag="{http://www.tei-c.org/ns/1.0}person"):
        for sub_kid in kid.iter():
            if (sub_kid.get("corresp") == piece_id):
                flag = True
            if(flag == True):
                persname = kid.find("{http://www.tei-c.org/ns/1.0}persName")
                persname = persname.text.split(" ")
                if (len(persname) > 1):
                    persname = persname[0][0] + " " + persname[1] # Herr Miaou -> H Miaou
                else:
                    persname = persname[0]
                job = kid.find(".//{http://www.tei-c.org/ns/1.0}f[@name='occupation']")
                social_class = kid.find(".//{http://www.tei-c.org/ns/1.0}f[@name='social_class']")
                dic[persname] = ["",""]
                if (job):
                    job = job.find("{http://www.tei-c.org/ns/1.0}symbol")
                    job_title = job.attrib["value"]
                    dic[persname][0] = job_title
                if (social_class):
                    social_class =social_class.find("{http://www.tei-c.org/ns/1.0}symbol")
                    s_class = social_class.attrib["value"]
                    dic[persname][1] = s_class
                flag = False
    return dic

def merge_dic(dic, dic_person):
    for key in dic.keys():
        for key_p in dic_person.keys():
            key1 = key.split(" ")
            realname = dic_person[key_p]["name"].split(" ")
            if (len(key1) > 1 and len(realname) > 1):
                if (key1[0] in realname[0] and key1[1] in realname[1]):
                    dic_person[key_p]["job"] = dic[key][0]
                    dic_person[key_p]["social_class"] = dic[key][1]
            else:
                if (key in dic_person[key_p]["name"]):
                    dic_person[key_p]["job"] = dic[key][0]
                    dic_person[key_p]["social_class"] = dic[key][1]
    return dic_person

def get_speaker_text(root, dic_person):
    #count = 0
    list_sp_text = []
    list_piece = []
    text = ""
    piece_type = root.find(".//{http://www.tei-c.org/ns/1.0}term")
    if(piece_type == None):
        piece_type = "unknown"
    else:
        piece_type = piece_type.text

    for kids in root.iter(tag="{http://www.tei-c.org/ns/1.0}sp"):
        #count += 1
        if (kids.attrib):
            who = kids.attrib["who"]
            if (who in dic_person):
                list_sp_text.append(piece_type)
                list_sp_text.append(dic_person[who]["name"])
                list_sp_text.append(dic_person[who]["sex"])
                list_sp_text.append(dic_person[who]["job"])
                list_sp_text.append(dic_person[who]["social_class"])
            else:
                list_sp_text.append(piece_type)
                list_sp_text.append("group")
                list_sp_text.append("sex_unknown")
                list_sp_text.append("job_unknown")
                list_sp_text.append("social_class_unknown")
            for subkids in kids:
                if (subkids.text):
                    text += subkids.text + "\n"
                else:
                    text += ""
            list_sp_text.append(text)
            text = ""
            list_piece.append(list_sp_text)
            list_sp_text = []

    return list_piece
    
def write_csv(list_piece, xml_out):
    header = ["drama_type", "speaker", "sex", "job", "social_class","text"]
    with open(xml_out, "w", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(header)
        writer.writerows(list_piece)

if __name__ == "__main__":
    main()
    
    

            