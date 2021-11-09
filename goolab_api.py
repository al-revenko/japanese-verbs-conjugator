import os
import requests

from dotenv import load_dotenv

# https://labs.goo.ne.jp/api/en/hiragana-translation/

load_dotenv()


APP_ID = os.getenv('APP_ID')
OUTPUT_TYPE = 'hiragana'

def convert_kanji(word):
    response = requests.post('https://labs.goo.ne.jp/api/hiragana', {"app_id":APP_ID, "sentence":word, "output_type":OUTPUT_TYPE}) 
    return response.json()

    
                  
                
                 


    

