import re
import csv
from bs4 import BeautifulSoup

def map_roman_nums(roman_num):
    '''
    Map roman numbers (used in original dictionary)
    '''
    roman_num_map = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
                     'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}
    return roman_num_map[roman_num.upper()]

def get_word(soup):
    '''
    Get word, homonyms and homonym's number (if exist)
    '''
    word_content = []
    for b_content in soup.b.contents:
        if str(b_content) != '<b><u><mark> </mark></u></b>':
            word_content_str = str(b_content).lower()
            word_content_str = word_content_str.replace('\t', '')
            word_content.append(word_content_str)
    word = {}
    word_str = None
    variant = None
    # 0 if no homonyms
    homonym_num = 0
    
    # Check structures of the word based on word content list length
    if len(word_content) == 1:
        word_str = word_content[0]
    elif len(word_content) == 2:
        if 'i' in word_content[1] or 'v' in word_content[1]:
            word_str = word_content[0]
            homonym_num = map_roman_nums(word_content[1])
        elif '(' in word_content[1] and ')' in word_content[1]:
            word_str = word_content[0]
            variant = word_content[1][1:-1]
        else:
            word_str = ' '.join(word_content)
    elif len(word_content) == 3:
        if (('(' in word_content[1] and ')' in word_content[1])
            and ('i' in word_content[2] or 'v' in word_content[2])):
            word_str = word_content[0]
            variant = word_content[1][1:-1]
            homonym_num = map_roman_nums(word_content[2])
    # TODO: add case "WORD (VARIANTS, ...)"" nb: variants often grammar words
    # Filter prefixes
    if word_str:
        if (word_str[-1] == '-') or ('-)' in word_str):
            word_str = None
    
    word['word'] = word_str
    word['variant'] = variant
    word['homonym_num'] = homonym_num
    
    return word

def get_meta(soup):
    '''
    Get meta - reference to the volume and page of original book
    '''
    for div_content in soup.div.contents:
        if ('(' in div_content) and (')' in div_content):
            s_pos = div_content.find('(') + 1
            e_pos = div_content.find(')')
            meta = div_content[s_pos:e_pos]
    return meta

def clip_by_upper(str, first_skip = False):
    '''
    Clip string by first (or second) upper (capital) letter
    '''
    e_pos = len(str)
    if not first_skip:
        for index, char in enumerate(str):
            if char.isupper():
                e_pos = index
                break
    else:
        first_flag = True
        for index, char in enumerate(str):
            if char.isupper() or char.isnumeric():
                e_pos = index
                if first_flag == False:
                    break
                first_flag = False
    clip_str = str[:e_pos].strip()
    return clip_str

def clean_definition(definition):
    '''
    Clean definition by replacing abbrevaiations, removing
    special symbols and stripping
    '''
    # Copying
    definition_cleaned = definition
    # Initial mapping
    init_map = {'напр. ': 'например',
                '-л.': '-либо',
                'соотв.': 'соответственно',
                'нек-р':'некотор',
                'к-рый': 'который',
                'к-рого':'которого',
                '-н:':'-нибудь:',
                'т. д.': 'так далее',
                'т. п.': 'тому подобное',
                'употр.': 'употребляется',
                'букв.': 'буквально',
                'преим.': 'преимущество',
                'в знач.': 'в значении',
                'с отриц. ф.': 'с отрицательной формой',
                'в отриц. ф.': 'в отрицательной форме',
                'кому-чему-либо': 'кому-, чему-либо',
                'кем-чем-либо': 'кем-, чем-либо',
                'кого-чего-либо': 'кого-, чего-либо',
                'кого-что-либо': 'кого-, что-либо',
                '‘':'"',
                '’':'"',
                ' ': ':',
                ' :': ':',
                ';': ','}
    for word, replacement in init_map.items():
        definition_cleaned = definition_cleaned.replace(word, replacement)
    # Strip
    strip_map = ['"', '“', '[', '. ', ', ', '-']
    for strip_substring in strip_map:
        definition_cleaned = definition_cleaned.strip(strip_substring)
    definition_cleaned = definition_cleaned.strip()
    # Final mapping
    fin_map = {' ,': ',',
               ' )': ')',
               '<i>': '',
               '</i>': ''}
    for word, replacement in fin_map.items():
        definition_cleaned = definition_cleaned.replace(word, replacement)
    definition_cleaned = definition_cleaned.lower()
    
    return definition_cleaned

def get_features(soup):
    '''
    Get word features (part of speech, definition)
    '''
    # Get feature content in <p> tag content and breaklines
    # Define definition by Θ symbol
    feature_content = []
    next_isdef = False
    definition = ''
    for p_content in soup.p.contents:
        p_content_str = str(p_content).strip()
        if (p_content_str and p_content_str != '<br/>'
                          and '<br/>' not in p_content_str):
            feature_content.append(p_content_str)
            if next_isdef and not definition:
                definition = p_content_str
            if p_content_str == '<b> Θ </b>' and not definition:
                next_isdef = True

    # Output dictionary
    features = {}
    
    # PART OF SPEECH
    # Define part of speech by first upper letter clipping
    part_of_speech = clip_by_upper(''.join(feature_content))
    # Remove tags
    pattern = re.compile(r'<.*?>')
    part_of_speech = re.sub(pattern, '', part_of_speech)
    # Remove numbers
    pattern = re.compile(r'[0-9][.]')
    part_of_speech = re.sub(pattern, '', part_of_speech)
    # Remove quotes and strip
    part_of_speech = part_of_speech.replace('“','')
    part_of_speech = part_of_speech.strip()
    # Check is part of speech precisely specified and map it
    # otherwise None
    part_of_speech_map = {'аат.': 'noun',
                          'даҕ.': 'adj', # adjective
                          'сыһ.': 'adv', # adverb
                          'саҥа алл.': 'interj', # interjection
                          'туохт.': 'verb'}
    wrong_part_of_speech = True
    for filt_part_of_speech in part_of_speech_map.keys():
        if part_of_speech == filt_part_of_speech:
            wrong_part_of_speech = False
    if not wrong_part_of_speech:
        features['part_of_speech'] = part_of_speech_map[part_of_speech]
    else:
        features['part_of_speech'] = None
    
    # DEFINITION
    definition = clip_by_upper(definition, first_skip = True)
    definition = clean_definition(definition)
    # Check if definition not empty string and not have Sakha letters
    # otherwise None
    if definition:
        sakha_letter_in_def_flag = False
        for sakha_letter in ['Ҥ', 'ҥ', 'Ҕ' ,'ҕ' ,'Ө', 'ө', 'Һ', 'һ', 'Ү', 'ү']:
            if sakha_letter in definition:
                sakha_letter_in_def_flag = True
        if not sakha_letter_in_def_flag:
            features['definition'] = definition
        else:
            features['definition'] = None
    else:
        features['definition'] = None
    
    return features

def parse_div(soup):
    parsed = {}
    word = get_word(soup)
    features = get_features(soup)
    if word['word'] and features['definition'] and features['part_of_speech']:
        parsed['word'] = word['word']
        parsed['variant'] = word['variant']
        parsed['homonym_num'] = word['homonym_num']
        parsed['part_of_speech'] = features['part_of_speech']
        parsed['definition'] = features['definition']
        return parsed
    else:
        return None
    
# Read html-file with only divs
with open('btsja_onlydivs.html', 'r', encoding = 'utf-8') as file:
    lines = file.readlines()

# Parse and write to csv
with open('btsja_parsed_v01.csv','w',newline='',encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['id', 'word', 'variant', 'homonym_num',
                    'part_of_speech', 'ru_definition'])
    for i, line in enumerate(lines):
        soup = BeautifulSoup(line, 'html.parser')
        parsed = parse_div(soup)
        if parsed != None:
            to_write = []
            to_write.append(str(i))
            for parsed_item in parsed.values():
                if parsed_item == None:
                    to_write.append('')
                elif isinstance(parsed_item, int):
                    to_write.append(str(parsed_item))
                else:
                    to_write.append(parsed_item)
            writer.writerow(to_write)