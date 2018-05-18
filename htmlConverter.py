#!/env/bin python
# -*- coding: utf-8 -*-
import os
import shutil
import re
from requests import get
from lxml import html

class AdvertisementEntry(object):
    def __init__(self, url):
        super(AdvertisementEntry, self).__init__()
        self.scrapedHTML = ""
        self.url = url
        self.updateScrapedText()

    def updateScrapedText(self):
        def extractTextFromChildren(tree):
            if isinstance(tree, basestring):
                return tree
            children = tree.xpath('child::node()')
            text = []
            while '\n' in children:
                children.remove('\n')
            for child in children:
                text.append(extractTextFromChildren(child))
            text = "".join(text)
            text = (tree.tag == 'li') and text + ". " or text 
            return text

        def scrapeHTMLContent(htmlHandler):
            tree = html.fromstring(htmlHandler.content)
            children = tree.xpath('//div[@class="job-body"]/child::node()')
            while "\n" in children:
                children.remove("\n")
            content = []
            for child in children:
                content.append(extractTextFromChildren(child))
            return " ".join(content).encode("utf-8")

        print("Anfragen von " + self.url)
        htmlHandler = get(self.url)
        #savePureHTMLContent(htmlHandler)
        self.scrapedHTML = scrapeHTMLContent(htmlHandler)
        htmlHandler.close()

    def stringifyResults(self):
        return self.url + ": \n" + self.scrapedHTML + "\n"*3


class AdvertisementList(object):
    def __init__(self):
        super(AdvertisementList, self).__init__()
        self.advertisements = []

    def add(self ,url):
        newEntry = AdvertisementEntry(url)
        self.advertisements.append(newEntry)

    def stringifyAllResults(self):
        allResults = ""
        for entry in self.advertisements:
            print(entry.stringifyResults())
            allResults + entry.stringifyResults()
        return allResults

    def fillWithFirstJobs(self, requestedJobs=20):
        """
        This function randomly generates 20 AdvertimentEntries representing job advertisements
        from jopage. These url-addresses are are extracted from https://www.jopago.com/jobs/search?pg=1 e.g. 
        We use regular expressions to search for actual job-links.
        """

        #This variable is used to keep track on which sides we have searched for jobs:
         #If we have processed all Jobs at https://www.jopago.com/jobs/search?pg=1
         # we simply go to https://www.jopago.com/jobs/search?pg=2 e.g.
        pageCounter = 1
        #This Variable keeps track on the amount of jobs we have extracted so far
        counter= 0
        site = "https://www.jopago.com"
        #lastLink prevents to receive the same job twice because of the html's structure 
        lastLink = ''
        while counter < requestedJobs:
            #We are looking with help of regular expressions in the HTML-File for strings in the for href="/jobs/<jobName>"
            htmlHandler = get(site + "/jobs/search?pg=" + str(pageCounter))
            unicode_re = re.compile('(?<=href=\"/jobs/)[^\""]+\"', re.IGNORECASE | re.UNICODE)
            for line in htmlHandler:
                m = unicode_re.search(line)
                if m :
                    link = m.group(0)
                    link = link[0:-1]
                    link = site + "/jobs/" + link

                    if not "search" in link and lastLink!=link:
                        newEntry = AdvertisementEntry(link)
                        self.advertisements.append(newEntry)
                        counter = counter + 1
                    if counter==requestedJobs:
                        return
                    lastLink = link
            pageCounter = pageCounter + 1
            htmlHandler.close()