import requests
from bs4 import BeautifulSoup


def parse(url):
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', string=lambda text: 'articleBody' in text)
            
            if script_tag:
                desc = script_tag.text.split('articleBody')[0].split('"description":')[1].split('genre')[0]
                text = script_tag.text.split('articleBody')[1].split('@')[0]
                return desc + text
        else:
            return 'До связи'
    except:
        return 'До связи'
