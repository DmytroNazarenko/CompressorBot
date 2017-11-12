from bs4 import BeautifulSoup
import re
import urllib.request as urllib


def download_file(link):
    file_name = re.search(r'[^/]*$',link).group(0)
    urllib.urlretrieve(link, file_name)
    return file_name

def retrieve_text(url):
    f = urllib.urlopen(url)
    text = f.read()
    soup = BeautifulSoup(text, 'html.parser')
    arr = soup.find_all(href=re.compile("https?://.*txt$"))
    links = [o['href'] for o in arr]
    names = list(map(download_file, links))
    return names

#print(retrieve_text('https://www.python.org/dev/peps/pep-0263/'))