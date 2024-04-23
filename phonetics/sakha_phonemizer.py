def word_to_ipa(word):
    '''Function to translate Sakha Cyrillic script to phonemes
    in IPA (International Phonetic Alphabet) notation
    
    Parameters
    ----------
    word : string
        Word in Sakha Cyrillic script, lowercase
    
    Returns
    -------
    word_ipa : tuple of strings
        Phonemes in IPA notation
    
    '''
    # All tri/bi/mono-graphs in Sakha language
    graphs = {3: {'ннь': 'ɲ:',
                  'ддь': 'dʑ:'},
              2: {'ыа': 'ɯa', 'иэ': 'iɛ', 'үө': 'yœ', 'уо': 'uɔ',
                  'нь': 'ɲ', 'дь': 'dʑ',
                  'аа': 'a:', 'оо': 'ɔ:', 'уу': 'u:', 'ыы': 'ɯ:',
                  'ээ': 'ɛ:', 'өө': 'œ:', 'үү': 'y:', 'ии': 'i:',
                  'мм': 'm:', 'нн': 'n:', 'ҥҥ': 'ŋ:',
                  'пп': 'p:', 'тт': 't:', 'чч': 'tɕ:', 'кк': 'k:',
                  'бб': 'b:', 'дд': 'd:', 'гг': 'g:',
                  'сс': 's:', 'хх': 'χ:', 'һһ': 'h:',
                  'ҕҕ': 'ʁ:', 'лл': 'l:', 'йй': 'j:', 'рр': 'ɾ:'},
              1: {'а': 'a', 'о': 'ɔ', 'у': 'u', 'ы': 'ɯ',
                  'э': 'ɛ', 'ө': 'œ', 'ү': 'y', 'и': 'i',
                  'м': 'm', 'н': 'n', 'ҥ': 'ŋ',
                  'п': 'p', 'т': 't', 'ч': 'tɕ', 'к': 'k',
                  'б': 'b', 'д': 'd', 'г': 'g',
                  'с': 's', 'х': 'χ', 'һ': 'h',
                  'ҕ': 'ʁ', 'л': 'l', 'й': 'j', 'р': 'ɾ'}}
    word_ipa = {}
    # Iterating over all n-graphs
    for n in range(3,0,-1):
        # Iterating for all n-grams
        for i in range(len(word)-(n-1)):
            gram = word[i:i+n]
            # 0 is a mark of identified graph
            if '0' not in gram:
                # Iterating for all graphs
                for ngraph in graphs[n]:
                    # Identifying
                    if gram == ngraph:
                        word_ipa[i] = graphs[n][ngraph]
                        # Marking identified graph
                        word = word[:i] + ''.join(['0']*n) + word[i+n:]
    
    # Sorting and taking tuple of phonemes
    word_ipa = list(zip(*sorted(word_ipa.items())))[1]
    
    return word_ipa

def word_to_vc(word):
    '''Function to translate Sakha Cyrillic script to
    consonants and vowels notation (C and V respectively)
    
    Parameters
    ----------
    word : string
        Word in Sakha Cyrillic script, lowercase
    
    Returns
    -------
    word_vc : tuple of strings
        Phoneme representation as consonant ("c") or vowel ("v")
    
    '''
    # All tri/bi/mono-graphs in Sakha language
    graphs = {3: {'ннь': 'c',
                  'ддь': 'c'},
              2: {'ыа': 'v', 'иэ': 'v', 'үө': 'v', 'уо': 'v',
                  'нь': 'c', 'дь': 'c',
                  'аа': 'v', 'оо': 'v', 'уу': 'v', 'ыы': 'v',
                  'ээ': 'v', 'өө': 'v', 'үү': 'v', 'ии': 'v',
                  'мм': 'c', 'нн': 'c', 'ҥҥ': 'c',
                  'пп': 'c', 'тт': 'c', 'чч': 'c', 'кк': 'c',
                  'бб': 'c', 'дд': 'c', 'гг': 'c',
                  'сс': 'c', 'хх': 'c', 'һһ': 'c',
                  'ҕҕ': 'c', 'лл': 'c', 'йй': 'c', 'рр': 'c'},
              1: {'а':  'v', 'о':  'v', 'у':  'v', 'ы':  'v',
                  'э':  'v', 'ө':  'v', 'ү':  'v', 'и':  'v',
                  'м':  'c', 'н':  'c', 'ҥ':  'c',
                  'п':  'c', 'т':  'c', 'ч':  'c', 'к':  'c',
                  'б':  'c', 'д':  'c', 'г':  'c',
                  'с':  'c', 'х':  'c', 'һ':  'c',
                  'ҕ':  'c', 'л':  'c', 'й':  'c', 'р':  'c'}}
    word_vc = {}
    # Iterating over all n-graphs
    for n in range(3,0,-1):
        # Iterating for all n-grams
        for i in range(len(word)-(n-1)):
            gram = word[i:i+n]
            # 0 is a mark of identified graph
            if '0' not in gram:
                # Iterating for all graphs
                for ngraph in graphs[n]:
                    # Identifying
                    if gram == ngraph:
                        word_vc[i] = graphs[n][ngraph]
                        # Marking identified graph
                        word = word[:i] + ''.join(['0']*n) + word[i+n:]
    
    # Sorting and taking tuple of phonemes
    word_vc = list(zip(*sorted(word_vc.items())))[1]
    
    return word_vc

if __name__ == "__main__":
    # Test
    sentence = 'Дьон барыта бэйэ суолтатыгар уонна ' \
               'быраабыгар тэҥ буолан төрүүллэр'
    for word in sentence.split(' '):
        print(word.lower())
        print(word_to_ipa(word.lower()))
        print(word_to_vc(word.lower()))
