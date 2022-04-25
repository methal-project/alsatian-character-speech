#!python
# coding: utf-8

# Based on metaphone.py
# By Andrew Collins - January 12, 2007 who claims no rights to this work
# http://www.atomodo.com/code/double-metaphone/metaphone.py/view.

# Author: Delphine Bernhard (Univ Strasbourg)

def dm(st):
    """
    dm(string) -> (string, string or None)
    returns the double metaphone codes for given string - always a tuple
    there are no checks done on the input string, but it should be a single	word
    or name.
    """
    vowels = ['A', 'À', 'Ä', 'Ã', 'Â', 'Æ', 'Å',
              'E', 'É', 'Ë', 'È', 'Ê',
              'I', 'Ì', 'Î', 'Ï', 'Í',
              'O', 'Ö', 'Ò', 'Õ', 'Ô', 'Ó', 'Œ',
              'U', 'Ü', 'Ù', 'Û',
              'Y']
    # st = st.decode('utf-8', 'ignore')
    st = st.upper()  # st is short for string. I usually prefer descriptive
    # over short, but this var is used a lot!
    length = len(st)
    first = 2
    # so we can index beyond the begining and end of the input string
    st = '-' * first + st + (' ' * 5)

    last = first + length - 1
    pos = first  # pos is short for position
    pri = sec = ''  # primary and secondary metaphone codes
    # main loop through chars in st
    while pos <= last:
        # print str(pos) + '\t' + st[pos]
        ch = st[pos]  # ch is short for character
        # nxt (short for next characters in metaphone code) is set to  a tuple
        # of the next characters in the primary and secondary codes and how many
        # characters to move forward in the string.
        # the secondary code letter is given only when it is different than the
        # primary.
        # This is just a trick to make the code easier to write and read.
        nxt = (
            None, 1)  # default action is to add nothing and move to next char
        if ch in vowels:
            nxt = (None, 1)
            if pos == first:  # all init vowels now map to 'A'
                nxt = ('A', 1)
        elif ch == 'B':
            # bezàhle, Butter, globfe
            if st[pos + 1] == 'B':
                nxt = ('P', 2)
            elif st[pos - 1] in vowels and st[pos + 1] in vowels:
                nxt = ('P', 'V', 1)
            else:
                nxt = ('P', 1)
        elif ch == 'C':
            # Bàcke, lackiere
            # if pos > (first + 1) and st[pos+1] == 'K' :
            if st[pos + 1] == 'K':
                nxt = ('K', 2)
            elif st[pos:pos + 2] == 'CH':
                # versüeche, màche, Hochwàsser, Koch, àcht, ààacht, Nààcht,
                # bräche, Buch
                if pos > first and (
                        st[pos - 1] in ['O', 'Ö', 'Ò', 'À', 'Ä', 'Ã', 'A', 'U',
                                        'Ü'] or st[pos - 2:pos] in ['ÀÀ', 'ÜE',
                                                                    'UE', 'UU',
                                                                    'ÜA']) and \
                        st[pos + 2] != 'S':
                    nxt = ('R', 2)
                # endlich, Storich
                elif st[pos + 2] == ' ' and st[pos - 1] == 'I':
                    nxt = (None, 'X', 2)
                # Kind/Chind, kalt/chalt
                elif pos == first:
                    nxt = ('K', 'X', 2)
                elif st[pos + 2] == 'S' and st[pos + 3:pos + 5] != 'CH':
                    nxt = ('KS', 'X', 3)
                elif pos > first and (st[pos - 1] == 'A'):
                    nxt = ('R', 'X', 2)
                # Kirichdurm, Leich, Sicher, Liicht, licht
                else:
                    nxt = ('X', 2)
            else:
                nxt = ('K', 1)
        elif ch == 'D':
            # Städtel
            if st[pos:pos + 2] in ['DT', 'DD']:
                nxt = ('T', 2)
            else:
                nxt = ('T', 1)
        elif ch == 'F':
            if st[pos + 1] == 'F':
                nxt = ('F', 2)
            else:
                nxt = ('F', 1)
        elif ch == 'G':
            # léngx
            if st[pos + 1:pos + 3] == 'X ':
                nxt = ('KS', 2)
            elif st[pos - 1] in ['I', 'A', 'À'] and pos == last:
                # nxt = (u'K', '', 2)
                nxt = ('K', None, 2)
            # Flieger
            # semi-consonne à l'hiatus : éjere, Fràje
            # variante géolingistique/diatopique de l'occlusive vélaire <g> :
            # fröje / froje / froga ; Wàge / Wàje
            elif pos < last and (st[pos - 1] in vowels or st[pos - 1] == 'J') \
                    and (st[pos + 1] in vowels or st[pos + 1] == ' ') \
                    and (st[pos + 1:pos + 4] != 'EN '):
                nxt = ('K', 'Y', 1)
            elif st[pos + 1] == 'G':
                nxt = ('K', 2)
            else:
                nxt = ('K', 1)
        elif ch == 'H':
            # only keep if first & before vowel or btw. 2 vowels
            if st[pos - 1] in vowels and st[pos + 1:pos + 3] == 'EN':
                nxt = ('Y', 'H', 2)
            elif (pos == first or st[pos - 1] == 'J'
                  or st[pos - 1] in vowels) and st[pos + 1] in vowels:
                nxt = ('H', 2)
            # Gsundheit, Eichhasel, Kleiderhoka, Mïlhüsa
            elif pos > (first + 1) and st[pos - 1] in (
                    'H', 'D', 'R', 'K', 'L', 'F', 'T', 'M'):
                nxt = ('H', 1)
            # Marque l'allongement de la voyelle : fàhre
            else:
                nxt = (None, 1)
        elif ch == 'J':
            # inbëjtz, Bäbegëj, mëjsle, Flëjschworscht, Majdel
            if st[pos + 1] not in vowels and st[pos - 1] in vowels:
                nxt = (None, 1)
            else:
                nxt = ('Y', 1)
        elif ch == 'K':
            if st[pos + 1] == 'K':
                nxt = ('K', 2)
            else:
                nxt = ('K', 1)
        elif ch == 'L':
            if st[pos + 1] == 'L':
                nxt = ('L', 2)
            else:
                nxt = ('L', 1)
        elif ch == 'M':
            if st[pos + 1] == 'M':
                nxt = ('M', 2)
            else:
                nxt = ('M', 1)
        elif ch == 'N':
            if st[pos + 1] == 'N':
                nxt = ('N', 2)
            # Adaptation pour l'allemand  : infinitif des versbes qui se
            # terminent par 'en'
            elif st[pos - 1] in ['E'] and pos == last:
                nxt = ('N', None, 1)
            elif st[pos - 1] in vowels and st[pos + 1] in ['F', 'T', 'M']:
                nxt = ('N', None, 1)
            else:
                nxt = ('N', 1)
        elif ch == 'P':
            if st[pos + 1] == 'H':
                nxt = ('F', 2)
            elif st[pos + 1] == 'P':
                nxt = ('P', 2)
            else:
                nxt = ('P', 1)
        elif ch == 'Q':
            # Qualle, quàtsche, Quatsch, Quettig
            if st[pos + 1] == 'U':
                nxt = ('KV', 2)
            else:
                nxt = ('K', 1)
        elif ch == 'R':
            if st[pos - 1] == 'E' and pos == last:
                nxt = ('R', None, 1)
            elif st[pos + 1] == 'R':
                nxt = ('R', 2)
            else:
                nxt = ('R', 1)
        elif ch == 'S':
            if st[pos:pos + 2] == 'SH':
                nxt = ('X', 'SH', 2)
            elif st[pos:pos + 3] == 'SCH':
                nxt = ('X', 3)
            elif st[pos:pos + 4] == 'SSCH':
                nxt = ('X', 4)
            # rutschrig
            # elif st[pos:pos+4] == 'SCHR':
            #	nxt = (u'X', 4)
            # Storich, / Storick / Storck ; Sdorich / Sdorick / Sdorch
            elif (st[pos:pos + 2] == 'ST' or st[pos:pos + 2] == 'SD') \
                    and (pos == first or st[pos - 1] in vowels
                         or st[pos - 1] in ['F', 'N', 'R', 'B', 'G']):
                nxt = ('XT', 2)
            # Speck / Spack ; Sbeck / Sback
            elif (st[pos:pos + 2] == 'SP' and st[pos + 2] != 'H') or (
                    st[pos:pos + 2] == 'SB'):
                nxt = ('XP', 2)
            elif st[pos + 1] == 'S':
                nxt = ('S', 2)
            else:
                nxt = ('S', 1)
        # Stroß, sieß
        elif ch == 'ß':
            nxt = ('S', 1)
        elif ch == 'T':
            if st[pos + 1] == 'Z':
                nxt = ('TS', 2)
            elif st[pos + 1] == 'T':
                nxt = ('T', 2)
            else:
                nxt = ('T', 1)
        elif ch == 'V':
            if st[pos + 1] == 'V':
                nxt = ('F', 'V', 2)
            else:
                nxt = ('F', 'V', 1)
        elif ch == 'W':
            # can also be in middle of word
            if st[pos - 1] in ['A', 'À'] and st[pos + 1] in ['A', 'E'] \
                    and st[pos - 2] not in ['I']:
                nxt = ('V', 'Y', 1)
            elif st[pos + 1] in vowels and st[pos - 1] in vowels:
                nxt = ('F', 'V', 1)
            elif st[pos - 1] in vowels and st[pos + 1] == ' ':
                nxt = ('F', 'V', 1)
            elif st[pos + 1] == 'W':
                nxt = ('V', 2)
            else:
                nxt = ('V', 1)
        elif ch == 'X':
            nxt = ('KS', 1)
        elif ch == 'Z':
            if st[pos + 1] in vowels or st[pos + 1] in ['W', 'L', 'Z']:
                nxt = ('TS', 1)
            elif pos == last:
                nxt = ('S', 'TS', 1)
            else:
                nxt = ('S', 1)
        # ----------------------------------
        # --- end checking letters------
        # ----------------------------------
        # print str(nxt)
        if len(nxt) == 2:
            if nxt[0]:
                pri += nxt[0]
                sec += nxt[0]
            pos += nxt[1]
        elif len(nxt) == 3:
            if nxt[0]:
                pri += nxt[0]
            if nxt[1]:
                sec += nxt[1]
            pos += nxt[2]
    if pri == sec:
        return pri, None
    else:
        return pri, sec


if __name__ == '__main__':
    names = {'einfàch': ('ANFR', 'AFR'), 'ëënfàch': ('ANFR', 'AFR'),
             'Ënfàch': ('ANFR', 'AFR'),
             'bràf': ('PRF', None), 'brààw': ('PRF', 'PRV'),
             'Kiffer': ('KFR', 'KF'), 'khiwer': ('KFR', 'KV'),
             'Wesch': ('VX', None), 'Wèsch': ('VX', None),
             'vülgär': ('FLKR', 'VLKR'), 'wülgèèr': ('VLKR', None),
             'endlich': ('ANTL', 'ANTLX'), 'andli': ('ANTL', None),
             'zwische': ('TSVX', None), 'tzwésche': ('TSVX', None),
             'zopfe': ('TSPF', None), 'tzopfe': ('TSPF', None),
             'Speck': ('XPK', None), 'Schbak': ('XPK', None),
             'bezàhle': ('PTSL', None), 'Butter': ('PTR', 'PT'),
             'globfe': ('KLPF', None),
             'sechzig': ('SXTSK', 'SXTS'),
             'köcha': ('KR', None), 'kocha': ('KR', None),
             'koche': ('KR', None),
             'khòche': ('KR', None),
             'bàche': ('PR', None), 'bàcha': ('PR', None),
             'bãcha': ('PR', None),
             'Racht': ('RRT', None),
             'chalt': ('KLT', 'XLT'),
             'Fuchs': ('FKS', 'FX'),
             'Durchschnìtt': ('TRXXNT', None),
             'licht': ('LXT', None),
             'Städtel': ('XTTL', None),
             'Düüma': ('TM', None),
             'léngx': ('LNKS', None),
             'zwìnga': ('TSVNK', None),
             'Tànz': ('TNS', 'TNTS'),
             'Eigatum': ('AKTM', 'AYTM'),
             'plätzlig': ('PLTSLK', 'PLTSL'),
             'Hüss': ('HS', None),
             'màche': ('MR', None),
             'ànnefàlle': ('ANFL', None),
             'Phosphàt': ('FSFT', None),
             'hàppa': ('HP', None),
             'Quatsch': ('KVTX', None),
             'Gàshard': ('KXRT', 'KSHRT'),
             'rutschrig': ('RTXRK', 'RTXR'),
             'Storich': ('XTR', 'XTRX'),
             'interessànt': ('ANTRSNT', 'ATRST'),
             'Sassel': ('SSL', None),
             'Schàtz': ('XTS', None),
             'Rackettel': ('RKTL', None),
             'Nàchtdischel': ('NRTTXL', None),
             'Tourischta': ('TRXT', None),
             'verlangt': ('FRLNKT', 'VRLNKT'),
             'Hüwe': ('HF', 'HV'),
             'Àx': ('AKS', None),
             "Z'middàà-Ësse": ('SMTS', None),
             'Flieger': ('FLKR', 'FLY'),
             'Dunnerschdàà': ('TNRXT', None), 'Dunnerschdi': ('TNRXT', None),
             'Dunnerschdig': ('TNRXTK', 'TNRXT'),
             'Kìnggala': ('KNKL', None),
             'erwähla': ('ARVL', None),
             'Eichhasel': ('AXHSL', None),
             'Gsundheit': ('KSNTHT', None),
             'Kleiderhoka': ('KLTRHK', None),
             'Märikhàll': ('MRKHL', None),
             'Mïlhüsa': ('MLHS', None),
             'Pfifholter': ('PFFHLTR', 'PFFHLT'),
             'Wirthüs': ('VRTHS', None),
             'Dàmmhirsch': ('TMHRX', None),
             'Majdel': ('MTL', None),
             'fröje': ('FRY', None),
             'Jager': ('YKR', 'YY'),
             'Qwàtch': ('KVTX', None),
             'sieß': ('SS', None),
             'Johreszit': ('YRSTST', None),
             'Kritzzug': ('KRTSTSK', None),
             'Schloofwàga': ('XLFVK', 'XLFVY'),
             'Schlofwaawe': ('XLFVV', 'XLFVY'),
             'Jodler': ('YTLR', 'YTL'),
             'Rüejdàà': ('RT', None), 'Rüaijtààg': ('RTK', 'RT'),
             'Schwiz': ('XVS', 'XVTS'),
             'Coupe': ('KP', None),
             'Waawe': ('VV', 'VY'),
             'schwimme': ('XVM', None), 'schwimmen': ('XVMN', 'XVM'),
             'beschtadiga': ('PXTTK', 'PXTTY'), 'bestätigen': ('PXTTKN',
                                                               'PXTTK'),
             'Nejheit': ('NHT', None), 'Näijhait': ('NHT', None),
             'Neuheit': ('NHT', None),
             'Fanschter': ('FNXTR', 'FNXT'), 'Fenster': ('FNXTR', 'FNXT'),
             'Näwwel': ('NVL', None), 'Nebel': ('NPL', 'NVL'),
             'àbzeije': ('APTSY', None), 'àbziaga': ('APTSK', 'APTSY'),
             'abziehen': ('APTSYN', 'APTSH'),
             'Gëërschta': ('KRXT', None), 'Gerste': ('KRXT', None),
             'Àbschtànd': ('APXTNT', None), 'Abstand': ('APXTNT', None),
             'aifàch': ('AFR', None), 'einfach': ('ANFR', 'AFR'),
             'Gejeteil': ('KYTL', None), 'Gegeteil': ('KKTL', 'KYTL'),
             'Gegenteil': ('KKNTL', 'KYTL'),
             'Grüawa': ('KRV', 'KRY'), 'Graben': ('KRPN', 'KRV'),
             'Uffschtànd': ('AFXTNT', None), 'Aufstand': ('AFXTNT', None),
             'Gàwwel': ('KVL', None), 'Gabel': ('KPL', 'KVL'),
             'Iwereinsschtimmung': ('AFRNXTMNK', 'AVRNXTMNK'),
             "übereinstimmung": ('APRNXTMNK', 'AVRNXTMNK'),
             'Ragamàntel': ('RKMNTL', 'RYMTL'), 'Regenmantel': ('RKNMNTL',
                                                                'RYMTL'),
             'Gmiesgàrta': ('KMSKRT', None), 'Gemüsegarten': ('KMSKRTN',
                                                              'KMSYRT'),
             'Àngscht': ('ANKXT', None), 'Angst': ('ANKXT', None),
             'Schlàgàfàll': ('XLKFL', 'XLYFL'), 'Schlaganfall': ('XLKNFL',
                                                                 'XLYFL'),
             'Fiewer': ('FFR', 'FV'), 'Fiawer': ('FFR', 'FV'),
             'Büech': ('PR', None), 'Buech': ('PR', None),
             'dihr': ('TR', None), 'diir': ('TR', None),
             'bubbele': ('PPL', None),
             'ärregt': ('ARKT', None),
             'Müschkel': ('MXKL', None), 'Mùschkel': ('MXKL', None),
             'grien': ('KRN', 'KR'),
             'April': ('APRL', None)}

    for name in list(names.keys()):
        assert (dm(name) == names[name],
                f'For "{name}" function returned {dm(name)}.'
                f' Should be {names[name]}.')

    print(dm('Chilche'))
    print(dm('Kirche'))
    print(dm('Schekbeeschel'))
    print(dm('Schäckbiachla'))
    print(dm('Müschkel'))
    print(dm('Mùschkel'))
    print(dm('April'))
    print(dm('Bléédsén'))
    print(dm('Bleedsenn'))
    print(dm('glych'))
