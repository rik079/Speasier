import re

def sanitizeText(text):
    return __replaceLink(text)

def __replaceLink(text):
    linkRegex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))" # from https://www.geeksforgeeks.org/python-check-url-string/
    link = re.search(linkRegex, text)
    while link != None:
        text = text[:link.span()[0]] + __extractDomain(link.group()) + text[link.span()[1]:]
        link = re.search(linkRegex, text)
    return text

def __extractDomain(link):
    domainRegex = r"[a-z0-9.\-]+[.][a-z]{2,4}"
    return re.search(domainRegex, link).group()
