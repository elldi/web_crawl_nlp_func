
from bs4 import BeautifulSoup
import nltk, re, string
from nltk.corpus import stopwords

#---------------------------------------------------------------------------------
"""
Function to strip the HTML markup from the file,
the head data is kept in a seperate variable to retain the useful meta data.
The information is saved into a plain text file for later processing.
"""
def stripHTML(soup, string):
    headData = soup.html.head
    headData = headData.prettify()
    text = soup.get_text()

    print("HTML has been stripped. ")

    return text
#---------------------------------------------------------------------------------
""""
Function to accept a file path string, open file for reading.
Pass the opened file into BS for html parsing.
"""
def read(string):
    try:
        file1 = open(string, 'r')
        soup = BeautifulSoup(file1, 'html.parser')
        return soup
    except FileNotFoundError:
        return False
#---------------------------------------------------------------------------------
""""
Function that takes a string, using regex will split of all of the whole words
found. Convert all words to lower case (this can be problematic when words
like IBM are encountered as the upper case adds more meaning to the token)
"""
def tokenise(text):
    text = re.sub("[\W]+ ", " ", text)

    text = [word.lower() for word in text]
    text = "".join(text)

    tokens = nltk.word_tokenize(text)

    return tokens

"""
Function the same as above but can be applied to lists. 
"""
def tokeniseList(text):
    list1 = []
    for string in text:
        text = re.sub("[\W]+ ", " ", string)

        text = [word.lower() for word in text]
        text = "".join(text)

        tokens = nltk.word_tokenize(text)
        list1.extend(tokens)

    return list1
#---------------------------------------------------------------------------------
"""
This function takes a list as an argument and runs the NLTK
tagger method, returning the list of tagged words. The list is also saved at this
point to aid in recovery from errors.
Only Nouns, Adjectives, Verbs and Foreign words are returned from the function to hone in on
keywords that are featured in the page.

https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
"""
def tagSpeech(list1):

    tagged_Page = nltk.pos_tag(list1)
    keep_tags = ['N', 'J', 'V','F', 'S']

    list1 = [s for s in tagged_Page if s[1][0] in keep_tags]

    tagged_Page = list1

    print("Speech has been tagged. ")

    return tagged_Page
#---------------------------------------------------------------------------------
"""
Function to remove stop words from the index.
Takes as argument as list of tagged words returned from the tagSpeech Function.
"""
def removeStops(tokens):
    list1 = []
    for x in range(len(tokens)):
        list1.append(tokens[x][0])
    tokens = list1

    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in tokens if not w in stop_words]

    print("Speech has been tokenised, stop words and punctuation removed. ")

    return filtered_sentence
#---------------------------------------------------------------------------------
"""
Function to control the normalisation of the webpage.
Coordinates the tokenisation, Part-of-Speech tagging, and stop words removal.
"""
def normalise(text, metaList):
    tokens = tokenise(text)
    metaTokens = tokeniseList(metaList)
    for mTokes in metaTokens:
        tokens.append(mTokes)
    
    tokens = tagSpeech(tokens)
    finalList = removeStops(tokens)

    return finalList

#---------------------------------------------------------------------------------
"""
This function takes a list of words, stems each word in the list and replaces
the original. 
"""
def stem(list1):
    stemmer = nltk.PorterStemmer()
    print("Lemmatising.")
    tokens = [stemmer.stem(token) for token in list1]
    print("Stemming complete. ")

    return tokens
#---------------------------------------------------------------------------------
"""
Function that counts the occurences of the words that have been normalised.
This will rank the keywords, with the highest occurring keyword having the most
relevance to the page, as stop words have been removed. 
"""
def termFreq(finalList):
    dict1 = {}
    for word in finalList:
        if(word in dict1):
            count = dict1[word] + 1
            dict1[word] = count
        else:
            dict1[word] = 1

    return dict1
    
#---------------------------------------------------------------------------------
"""
Function to print out contents of a list.
"""
def dictToFile(dict1, sectionTitle, outputFile):
    file1 = open(outputFile, "a")
    
    file1.write("\n"+sectionTitle + "\n")
    file1.write("#---------------------------------------------------------------------------------#\n")

    for key, value in dict1.items():
        file1.write(key +":"+ str(value)+ "\n")
    
    file1.close()
def outputToFile(list1, sectionTitle, outputFile):
    file1 = open(outputFile, "a")
    
    file1.write("\n"+sectionTitle + "\n")
    file1.write("#---------------------------------------------------------------------------------#\n")

    for data in list1:
        file1.write(str(data) + ", ")

    file1.write("\n")
    file1.close()
    
def outputHeader(soup):

    fileName = soup.title.string
    out = "".join(c for c in fileName if c not in ('!','.',':', '/'))
    fileName = out + ".txt"
    file1 = open(fileName, "w")

    file1.write("Title: " + soup.title.string + "\n") 
    file1.write("#---------------------------------------------------------------------------------#\n")
    file1.close()

    return fileName
    
#---------------------------------------------------------------------------------
"""
Function to output the term frequency to a CSV file for further analysis. 
"""
def csvOutput(dict1,soup):
    fileName = soup.title.string
    out = "".join(c for c in fileName if c not in ('!','.',':', '/'))
    fileName = out + ".csv"
    file1 = open(fileName, "w")

    temp = []
    for key in dict1:
        file1.write(key + ",")
        temp.append(key)
    file1.write("\n")
    for key in temp:
        file1.write(str(dict1[key]) + ",")
    file1.write("\n")
    file1.close()    
    
    
#---------------------------------------------------------------------------------

"""
Function to return a list of strings, these strings are the contents of the meta
tags. 
"""
def metaTags(soup):
    meta = []
    for tag in soup.find_all('meta'):
        tag = tag.get("content")    
        meta.append(tag)
    return meta
#---------------------------------------------------------------------------------

"""
Function that returns the string within the <b> tags of a web page.
Most often, words in bold are keywords related to the subject matter
of the page.
"""
def boldTags(soup):
	bold = []
	for tag in soup.find_all('b'):
		tag = tag.string
		if(tag != None):
			if(not(len(tag) <= 1)):
				bold.append(tag)
	return bold
#---------------------------------------------------------------------------------

""""
Function to return the string within the <i> tags of a web page.
These tags are used to highlight keywords within a body of text.
Uses include:
	To emphasise a point
	Titles of Works - E.G. Book, Plays, Movies, Music etc.
	Foreign Words, Technical Terms, and Unfamiliar Words
	Names of Ships, Aircraft etc.
Hence text that has been italicised is important to indexing the content
of the page.
"""
def italicTags(soup):
	it = []
	for tag in soup.find_all('i'):
		tag = tag.string
		if(tag != None):
			if(not(len(tag) <= 1)):
				it.append(tag)

	return it
#---------------------------------------------------------------------------------    
"""
Simple function to return the no. of urls featured in the page.
This statistic can be used to determine the reliability of a page
but it recommended that further analysis of what these links link to
is a better gauge of authority.
"""
def urlReliability(soup):
	links = []
	for link in soup.find_all('a'):
		links.append(link.get('href'))
	return len(links), links
#---------------------------------------------------------------------------------
def main(list1):
    for file in list1:
        file = file.strip() # Strip leading or trailing whitespace
        soup = read(file)
        if(not soup):
            print("File could not be found! Please try again.")
            break
        
        outputFileName = outputHeader(soup)
        
        noHTML = stripHTML(soup, file)

        metaList = metaTags(soup)
        
        normalised = normalise(noHTML, metaList)

        stemming = stem(normalised)
        dict1 = termFreq(stemming)
        dictToFile(dict1, "Term Frequency Words:", outputFileName)
        outputToFile(boldTags(soup), "Bold Words:", outputFileName)
        outputToFile(stemming, "Stemmed Words:", outputFileName)
        noLinks, __ = urlReliability(soup)
        outputToFile([noLinks], "Number of Links:", outputFileName)

        csvOutput(dict1,soup)

        


 









    
    
