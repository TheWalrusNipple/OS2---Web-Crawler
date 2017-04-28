import urllib.request
import html.parser
import concurrent.futures
import queue
import re



def main():
    linksVisited = []
    linksWaiting = []
    tmpList = []

    wordsLinksList = {}
    rootAddress = "http://selenium.ssucet.org:8001"

    linksWaiting.append(rootAddress)


    #https://docs.python.org/3/library/concurrent.futures.html
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        while len(linksWaiting) > 0:
            # Start the load operations and mark each future with its URL
            thread = {executor.submit(analyzeData, link, linksVisited, tmpList, wordsLinksList): link for link in linksWaiting}
            for future in concurrent.futures.as_completed(thread):
                future.result()             #fuuuuutuuuuuuure

            linksWaiting = []
            linksWaiting = tmpList
            tmpList = []





    print("done!")
    #print results
    for w in wordsLinksList:
        print(w, " ", wordsLinksList[w])

class MyParser(html.parser.HTMLParser):
    def my_data(self):
        self.wordsFound = []
        self.linksFound = []

    def handle_starttag(self, tag, attrs):
        if tag == "a" and attrs[0][0] == "href":                                                                        #if it's a link...
            curLink = attrs[0][1]
            if curLink[:26] == "http://selenium.ssucet.org":                                                            #if it's the selenium site...
                self.linksFound.append(curLink)
            elif curLink[0] == "/":             #makes sure the /num sites are included
                tmp = "http://selenium.ssucet.org:8001" + curLink
                self.linksFound.append(tmp)


    def handle_data(self, data):
        wordList = data.split()
        for word in wordList:
            if ord(word[0]) >= 97 and ord(word[0]) < 123:       #excludes html data that's not a real word
                if not word in self.wordsFound:
                    self.wordsFound.append(word)

def analyzeData(url, linksVisited, linksToVisit, wordsList):
    #open url
    if not url in linksVisited:
        linksVisited.append(url)
        #linksToVisit.remove(url)
        u = urllib.request.urlopen(url)
        data = u.read()
        data = data.decode()
        u.close()

        #create a parser for it
        parser = MyParser()
        parser.my_data()
        parser.feed(data)

        #gets data from parser and puts them in the proper lists
        for link in parser.linksFound:              #adds found links to the queue
            if not link in linksVisited:
                linksToVisit.append(link)
        for word in parser.wordsFound:              #adds the words found to the dictionary
            wordsList.setdefault(word, [])
            wordsList[word].append(url)


















if __name__ == '__main__':
    main()