#Afaf Guesmia
#Assignment5
#axg190061
##Building a Corpus


from urllib.parse import urlparse
from urllib import request
from bs4 import BeautifulSoup
import os
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pickle

##Function extract_link used to extract 15 urls from the chosen url
def extract_links(url):
    ##Create 2 lists for internal and external urls
    urls_internal = []
    urls_external = []
   ##make sure the urls are in the domain of the chosen url
    original_domain = urlparse(url).netloc
    ##exctact external and internal and external urls using beautiful Soup
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None:
            parsed_href = urlparse(href)
            if parsed_href.netloc == original_domain and len(urls_internal) < 10:
                urls_internal.append(href)
            elif parsed_href.netloc != '' and len(urls_external) < 6:
                urls_external.append(href)

    return urls_internal, urls_external

##create function clean_text to clean each text in the pages for newlines,tabs and stopwords
def clean_text(text):
    # Remove newlines and tabs
    cleaned_text = re.sub(r'[\n\t]+', ' ', text)

    # Lowercase everything
    cleaned_text = cleaned_text.lower()

    # Remove punctuation
    cleaned_text = cleaned_text.translate(str.maketrans("", "", string.punctuation))

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(cleaned_text)
    cleaned_words = [word for word in words if word not in stop_words]

    return cleaned_words

##create function save_text that stores text from pages as the original text as well as the modified ones.
def save_text(link):
    try:
        ##using html and beautuful soyp to extract the text
        html = request.urlopen(link).read().decode('utf8')
        soup = BeautifulSoup(html)
        text = soup.get_text()

        # Save the original text
        with open(link.split('/')[-1] + ".txt", "w", encoding='utf-8') as f:
            f.write(text)
        print(f"Text from {link} has been saved.")

        # Save the cleaned text
        cleaned_text = clean_text(text)
        with open(link.split('/')[-1] + "_cleaned.txt", "w", encoding='utf-8') as f:
            f.write(" ".join(cleaned_text))
        print(f"Cleaned text from {link} has been saved.")

        # Save the top 25-40 terms
        word_count = Counter(cleaned_text)
        top_words = [word for word, count in word_count.most_common(40)]
        with open(link.split('/')[-1] + "_top_words.txt", "w", encoding='utf-8') as f:
            f.write("\n".join(top_words))
        print(f"Top words from {link} have been saved.")
    except:
        print(f"Error processing {link}.")

##main function
if __name__ == '__main__':
    ##main url
    url = 'https://www.vogue.com/'
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html)

    internal_links, external_links = extract_links(url)
    links = internal_links + external_links
    ## print both external and internal urls
    print("Internal links:")
    for url in internal_links:
        print(url)

    print("\nExternal links:")
    for url in external_links:
        print(url)

    for link in links:
        save_text(link)

    # Print top words from each cleaned/tokonized file
    for filename in os.listdir():
        if filename.endswith("_cleaned.txt"):
            with open(filename, "r", encoding='utf-8') as file:
                cleaned_text = file.read().lower()
                cleaned_words = clean_text(cleaned_text)
                word_count = Counter(cleaned_words)
                top_words = [word for word, count in word_count.most_common(40)]
                print(f"Top words from {filename}:")
                print("\n".join(top_words))
    #top 10 terms  manually generated.
    terms=['fashion', 'makeup','shades','style','designer','artist','trendy','outfit','look','2022']
    print(terms)
    ##Create a knoledge base using the top 10 terms, using python dicts and pickes
    knowledge_base = {
        'fashion': [
            'Fashion is a form of self-expression and autonomy at a particular period and place and in a specific context',
            'Fahsion consists of clothing, footwear, lifestyle, accessories, makeup, hairstyle, and body posture.',
            'The term implies a look defined by the fashion industry as that which is trending.'
        ],
        'makeup': [
            'Makeup is a form of self-expression that has been around for thousands of years.',
            'cosmetics such as lipstick or powder applied to the face, used to enhance or alter the appearance',
            'Makeup mainly is used to change or enhance the way we look, to feel more confident and also to hide our imperfection'
        ],
        'shades': [
            'Shades are a type of eyewear designed to protect the eyes from sunlight.',
            'Sunglasses can reduce the risk of developing cataracts and other eye diseases.',
            'A shade is when a color remains its original hue but has been darkened.'
        ],
        'style': [
            'Style is a way of expressing oneself through clothing, accessories, and other aesthetic choices.',
            'In the fashion world, “style” is usually shorthand for “personal style,” or the way an individual expresses themselves through aesthetic choices such as their clothing, accessories, '
            'hairstyle, and the way they put an outfit together.'
        ],
        'designer': [
            'A fashion designer is someone who creates clothing, footwear, and accessories.',
            'Famous fashion designers include Coco Chanel, Christian Dior, and Giorgio Armani.',
            'The fashion industry relies heavily on designers to create new and innovative products.'
        ],
        'artist': [
            'Fashion designers can be considered artists because they use creative expression to design clothing and accessories.',
            'Many fashion designers also collaborate with artists on special collections.',
            'The Metropolitan Museum of Art in New York City has a Costume Institute that showcases fashion as art.'
        ],
        'trendy': [
            'Trendy refers to something that is popular or fashionable at a particular time.',
            'Trends can come and go quickly in the fashion industry.',

        ],
        'outfit': [
            'a set of clothes worn for a particular occasion or activity',
            'An outfit refers to a set of clothing and accessories worn together.',
            'The right outfit can make a person feel confident and stylish.'

        ],
        'look': [
            'A look refers to a particular style or appearance that a person is trying to achieve.',
            'Fashion influencers and bloggers often showcase their looks on social media.'
        ],
        '2022': [
            'Fashion trends for 2022 include bold prints, oversized clothing, and bright colors.',
            '2022 is expected to be a year of experimentation and creativity in the fashion industry.'
        ]
    }
    with open("knowledge_base.pickle", "wb") as picke_file:
        pickle.dump(knowledge_base, picke_file)

