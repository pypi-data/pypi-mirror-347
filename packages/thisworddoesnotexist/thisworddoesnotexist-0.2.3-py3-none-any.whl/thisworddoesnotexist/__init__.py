import requests
from bs4 import BeautifulSoup
import sys

def get_fake_word():
    """
    Fetches a fake word from thisworddoesnotexist.com
    
    Returns:
        str: A randomly generated fake word
    """
    try:
        response = requests.get('https://www.thisworddoesnotexist.com/')
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        word_element = soup.find('div', {'class': 'word'})
        
        if word_element:
            return word_element.text.strip()
        else:
            raise ValueError("Could not find word on the page")
            
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch word: {str(e)}")
    
def cli():
    """
    Command line interface for the thisworddoesnotexist package.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    try:
        word = get_fake_word()
        print(word)
        return 0
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(cli())