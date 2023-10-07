import csv
#import xml.etree.ElementTree as ET
from lxml import etree as ET
import os, sys
import pandas as pd
import re

dir_path = "./pre_treatment/treated_files_df18"
xml_in = ""

NSMAP = {"tei": "http://www.tei-c.org/ns/1.0"}


def main():
    """main funtion to execute codes

    Args:
        param1: The directory of the xml file.
        param2: The filename.

    Returns:
        Creates a csv file extracted from the previous xml file

    """
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    xml_in = "./pre_treatment/" + sys.argv[1] + "/" + sys.argv[2]
    csv_out = dir_path + "/" + sys.argv[2][:-3] + "out.csv"

    file_personography = "./pre_treatment/methal-personography.xml"
    tree_person = ET.parse(file_personography)# make a xml tree of extra personal information
    #tree_person = etree.parse(file_personography)# make a xml tree of extra personal information
    root_person = tree_person.getroot()
    
    tree = ET.parse(xml_in) # make a xml tree of basic personal information
    root = tree.getroot()
    piece_id = root.find(".//{http://www.tei-c.org/ns/1.0}idno[@type='methal']")
    piece_id = "#" + piece_id.attrib["{http://www.w3.org/XML/1998/namespace}id"] # obtenir l'id de la piece
    print(piece_id)

    dic_person = person_info(root)
    dic = add_person_info(root_person, piece_id)
    #breakpoint()
    dic_person = merge_dic(dic, dic_person)

    list_piece = get_speaker_text(root, dic_person)
    write_csv(list_piece, csv_out)
    short_name = sys.argv[2][:-4]
    if ("lustig" in sys.argv[1]):
        short_name = "lustig-" + short_name
    df = pd.read_csv(csv_out, index_col = False)
    # ------------------------------- slice the piece -------------------------------------
    num_rows = df.shape[0]
    x_ticks = []
    step = num_rows // 100
    if (step == 0):
        step = 1
    x_ticks = [index for index in range(num_rows//step) for i in range(step)]
    rest = num_rows - len(x_ticks)
    rest_id = x_ticks[len(x_ticks) - 1] + 1
    for i in range(rest):
        x_ticks.append(rest_id)
    print(len(x_ticks), num_rows)
    df["progress"] = x_ticks
    # --------------------------------------------------------------------------------------
    df["short_name"] = short_name
    info_df = pd.read_csv("./pre_treatment/personnages-pieces.csv")
    print(short_name)
    genre = info_df.loc[short_name == info_df["shortName"]]
    df["drama_type"] = genre["genre"].values[0]
    #df.to_csv(csv_out, sep="\t", index=False)
    df.to_csv(csv_out, index=False)


def person_info(root):
    """Function to grab basic personal information of each character

    Args:
        param1: The root of the xml file made by ElementTree.

    Returns:
        A dictionary containing basic information of characters

    """
    dic_person = {} # information of all the characters
    dic_line = {} # information of only one character
    for kids in root.iter(tag="{http://www.tei-c.org/ns/1.0}personGrp"):
        # look for all the nodes with a label "personGrp"
        if (kids):
            if (kids.attrib):
                # get attributes of child nodes and add them to the dictionary dic_line
                sex = kids.attrib["sex"]
                id = kids.attrib["{http://www.w3.org/XML/1998/namespace}id"]
                dic_line["name"] = id
                dic_line["sex"] = sex
                dic_line["job"] = ""
                dic_line["job_category"] = ""
                dic_line["social_class"] = ""
                dic_person["#" + id] = dic_line
                dic_line = {} # reinitialise dic_line
    for kids in root.iter(tag="{http://www.tei-c.org/ns/1.0}person"):
        # look for all the nodes with a label "person"
        sex = kids.attrib["sex"]
        id = kids.attrib["{http://www.w3.org/XML/1998/namespace}id"]
        name = kids.find("{http://www.tei-c.org/ns/1.0}persName")
        realname = ""
        # get the names of characters
        if (len(name.findall("{http://www.tei-c.org/ns/1.0}emph")) == 0):
            realname = name.text
        else:
            for kid_name in name:
                if (kid_name.text):
                    if(name.text):
                        realname = name.text.strip() + " " + kid_name.text.strip()
                        #realname = name.text.strip().strip(":,;") + " " + kid_name.text.strip().strip(":,;")
                    else:
                        realname = kid_name.text.strip()
        dic_line["name"] = realname
        dic_line["sex"] = sex
        dic_line["job"] = ""
        dic_line["job_category"] = ""
        dic_line["social_class"] = ""
        dic_person["#" + id] = dic_line
        dic_line = {}
    return dic_person

def add_person_info(root, piece_id):
    """Function to grab extra personal information of each character
       from the feature-structures prosopography

    Args:
        param1: The root of the xml file made by ElementTree.
        param2: The id of the theater piece

    Returns:
        A dictionary containing extra information of characters

    """
    flag = False # a flag to check if the characters are in the same piece.
    dic = {}
    for kid in root.iter(tag="{http://www.tei-c.org/ns/1.0}person"):
        for sub_kid in kid.iter():
            if (sub_kid.get("corresp") == piece_id):
                flag = True
            if(flag == True):
                persname = kid.find("{http://www.tei-c.org/ns/1.0}persName")
                persname = persname.text.split(" ")
                #TODO may need to revise here to get more cases (try to create an ID
                # using the same conventions as for manual transformation
                # or merge, additionnally, based on exact match of persName value)
                # OR MAYBE NOT AS MOST ERRORS SO FAR WERE DUE TO THE DATA (@who not matched
                # in listPerson)
                if (len(persname) > 1):
                    # this makes sense given the way person names are compared later when
                    # merging both dictionaries in the merge_dic() function below
                    persname = persname[0][0] + " " + persname[1] # Herr Miaou -> H Miaou
                else:
                    persname = persname[0]
                job = kid.find(".//{http://www.tei-c.org/ns/1.0}f[@name='occupation']")
                job_category = kid.find(".//{http://www.tei-c.org/ns/1.0}f[@name='professional_category']")
                social_class = kid.find(".//{http://www.tei-c.org/ns/1.0}f[@name='social_class']")
                dic[persname] = ["","",""] # array which contains job, job_category and social_class
                if (job):
                    job = job.find("{http://www.tei-c.org/ns/1.0}symbol")
                    job_title = job.attrib["value"]
                    dic[persname][0] = job_title
                if (job_category):
                    job_category = job_category.find("{http://www.tei-c.org/ns/1.0}symbol")
                    cate_title = job_category.attrib["value"]
                    dic[persname][1] = cate_title
                if (social_class):
                    social_class =social_class.find("{http://www.tei-c.org/ns/1.0}symbol")
                    s_class = social_class.attrib["value"]
                    dic[persname][2] = s_class
                flag = False
    return dic

def merge_dic(dic, dic_person):
    """Function to merge two dicitonaries

    Args:
        param1: The dictionary with extra personal information (dict)
        param2: The dictionary with basic personal information (dict)

    Returns:
        A dictionary containing basic + extra information of characters

    """
    for key in dic.keys(): # iterate in the dictionary with extra personal information
        for key_p in dic_person.keys():
            key1 = key.split(" ")
            realname = dic_person[key_p]["name"].split(" ")
            # add extra personal information to the dictionary of basic personal information
            if (len(key1) > 1 and len(realname) > 1):
                if (key1[0] in realname[0] and key1[1] in realname[1]):
                    dic_person[key_p]["job"] = dic[key][0]
                    dic_person[key_p]["job_category"] = dic[key][1]
                    dic_person[key_p]["social_class"] = dic[key][2]
            else:
                if (key in dic_person[key_p]["name"]):
                    dic_person[key_p]["job"] = dic[key][0]
                    dic_person[key_p]["job_category"] = dic[key][1]
                    dic_person[key_p]["social_class"] = dic[key][2]
    return dic_person


def clean_up_text(text_part):
    """
    Strip whitespace and other normalizations to character speech
    so that can output to dataframe.

    Args:
        text_part (str): The text to normalize

    Returns:
        Normalized text
    """
    text_norm = text_part
    if text_norm is not None and len(text_norm) > 0:
        text_norm = text_norm.strip()
        text_norm = re.sub(r"\s{2,}", " ", text_norm)
    return text_norm


def get_speaker_text(root, dic_person):
    """Function to grab words + all personal information of the piece

    Args:
        param1: The root of the xml file made by ElementTree.
        param2: The merged dictionary made by function merge_dic.

    Returns:
        An array which contains words + all personal information of the piece

    """
    #count = 0
    list_who = []
    list_sp_text = [] # toutes les infos pour une tourne de parole
    list_piece = []
    text = ""
    # ------------------------------------- supprimer? -----------------------
    piece_type = root.find(".//{http://www.tei-c.org/ns/1.0}term")
    if(piece_type == None):
        piece_type = "unknown"
    else:
        piece_type = piece_type.text
    # ------------------------------------------------------------------------
    for kids in root.iter(tag="{http://www.tei-c.org/ns/1.0}sp"):
        #count += 1
        if (kids.attrib):
            who = kids.attrib["who"]
            list_who = who.split(" ")
            for who in list_who:
                if (who in dic_person):
                    list_sp_text.append(piece_type)
                    list_sp_text.append(dic_person[who]["name"])
                    list_sp_text.append(dic_person[who]["sex"])
                    list_sp_text.append(dic_person[who]["job"])
                    list_sp_text.append(dic_person[who]["job_category"])
                    list_sp_text.append(dic_person[who]["social_class"])
                else:
                    list_sp_text.append(piece_type)
                    list_sp_text.append("group")
                    list_sp_text.append("sex_unknown")
                    list_sp_text.append("job_unknown")
                    list_sp_text.append("job_category_unknown")
                    list_sp_text.append("social_class_unknown")
                # this was ok for emotion detection but bad for character distinctiveness task,
                # because this is accepting stage directions and speaker names into the text
                # kept in the dataframe. So instead will run XPath with lxml to keep child text
                # from the p elements only
                if False:
                    for subkids in kids.itertext():
                        if (subkids):
                            #text += clean_up_text(subkids) + "\n"
                            text += clean_up_text(subkids) + "|||"
                        else:
                            text += ""

                # ok to collect text here but note that under some conditions,
                # if the speech has two IDs in @who, this could result in
                # speech being repeated in the dataframe, once for each character
                # not the case now cos <sp> where @who has > 1 value are ignored
                # before crossing metadata, so they're ignored for the analyses

                # avoid stage and sp but keep p and l
                for subkids in kids.xpath(".//tei:p/text()|.//tei:l/text()", namespaces=NSMAP):
                    if subkids:
                        text += clean_up_text(subkids) + "|||"

                text = re.sub(r"\|{4,}", "|||", text)
                list_sp_text.append(text.rstrip("|"))
                text = ""
                list_piece.append(list_sp_text)
                list_sp_text = []
    return list_piece


def write_csv(list_piece, csv_out):
    """Function to write all information to csv files

    Args:
        param1: An array which contains words + all personal information of the piece.
        param2: Path to the csv file 

    Returns:
        None

    """
    header = ["drama_type", "speaker", "sex", "job", "job_category", "social_class","text"]
    with open(csv_out, "w", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(header)
        writer.writerows(list_piece)

if __name__ == "__main__":
    main()
