from goolab_api import convert_kanji


class Verb:
    def __init__(self, converted_word, irregular_masu=None, irregular_te=None, irregular_group=None):
        self.word = converted_word
        self.group = self.__class__.__name__
        self.irregular_masu = irregular_masu
        self.irregular_te = irregular_te
        self.irregular_group = irregular_group


class ThirdGroup(Verb):
    def __init__(self, converted_word):
        Verb.__init__(self, converted_word)
        
        match self.word:
           case 'する':
               self.masu = 'します'
               self.te = 'して'
           
           case 'くる':
               self.masu = 'きます'
               self.te = 'きて'

    
class SecondGroup(Verb):
    def __init__(self, converted_word, irregular_masu=None, irregular_te=None, irregular_group=None):
        Verb.__init__(self, converted_word, irregular_masu, irregular_te, irregular_group)
        
        masu_f = self.word[:-1] + 'ます'
        te_f = self.word[:-1] + 'て'
        self.masu = masu_f
        self.te = te_f



class FirstGroup(Verb):    
    def __init__(self, converted_word, irregular_masu=None, irregular_te=None, irregular_group=None):
        Verb.__init__(self, converted_word, irregular_masu, irregular_te, irregular_group)

        masu_relationship = {
                'う': 'い', 
                'く': 'き', 
                'ぐ': 'ぎ', 
                'す': 'し', 
                'ず': 'じ', 
                'つ': 'ち', 
                'づ': 'ぢ', 
                'ぬ': 'に', 
                'ふ': 'ひ', 
                'ぶ': 'び', 
                'ぷ': 'ぴ', 
                'む': 'み', 
                'る': 'り'
                } 
        for key in masu_relationship:
            if key == self.word[-1]:
                result = self.word[:-1] + masu_relationship[key] + 'ます'
                break
        
        self.masu = result
    
        te_relationship = {
                ('う','つ','る'): 'って',
                ('ぬ','ぶ','む'): 'んで',
                'く': 'いて',
                'ぐ': 'いで',
                'す': 'して',
                }
        for key in te_relationship:
            if isinstance(key, tuple) and self.word[-1] in key:
                result = self.word[:-1] + te_relationship[key]
                break

            elif self.word[-1] == key:
                result = self.word[:-1] + te_relationship[key]
                break
        
        self.te = result


def verb_veryfication(converted_word):
    ending_verb = ('う', 'く', 'す', 'つ', 'ぬ', 'ふ', 'む', 'る')

    if converted_word.isalpha() and converted_word[-1] in ending_verb:
        if converted_word[-2:] != 'ます':
            return True
        else:
            return False
    else:
        return False
               

def irregular_veryfication(converted_word):
    
    irregular_words = {
            'いく':('FirstGroup', 'いきます', 'いって'),
            'かえる':('FirstGroup', 'かえります', 'かえって'),
            'はいる':('FirstGroup', 'はいります', 'はいって'),
            'きる':('FirstGroup', 'きリます', 'きって')}

    if converted_word in irregular_words:
        return irregular_words[converted_word]
    
    else:
        return False


def find_group(converted_word):

    third_words = ('する', 'くる')
    
    second_ends = {
            'iru': ('いる','きる','しる','ちる','にる','ひる','みる','りる'), 
            'eru': ('える','ける','せる','てる','ねる','へる','める','れる')}
    
    if converted_word in third_words:
        return 3
    
    elif converted_word[-2:] in second_ends['iru'] or converted_word[-2:] in second_ends['eru']:
        return 2
    
    else:
        return 1


def start_conjugation(converted_word):
    if verb_veryfication(converted_word):

        irregular = irregular_veryfication(converted_word)
        
        if not irregular:
            match find_group(converted_word):
                case 3:
                    return ThirdGroup(converted_word)
                case 2:
                    return SecondGroup(converted_word)
                case 1:
                    return FirstGroup(converted_word)
        else:
            match find_group(converted_word):
                case 2:
                    return SecondGroup(converted_word, irregular[1], irregular[2], irregular[0])
                case 1:
                    return FirstGroup(converted_word, irregular[1], irregular[2], irregular[0])
    else:
        raise Exception('Not a Verb or formated verb!')



if __name__ == '__main__':
    while True:
        value = input('Write verb: ')
        converted_value = convert_kanji(value)['converted']
        result = start_conjugation(converted_value)
        if result.irregular_masu or result.irregular_te:
            print(result.masu, result.te, result.group )
            print(result.irregular_masu, result.irregular_te, result.irregular_group, '<- irregular')
        else:
            print(result.masu, result.te, result.group)

