######################################################################
#
# Cariessa Taylor
# August 9, 2021
# CSIS 483 Phase 3
#
# This project serves as a platform to retreive the scriptures in
# various languages and translations. This program can run in two
# different methods:
#  1. Stand Alone - useful for development, testing, and single
#     user situations
#  2. REST HTTP server - useful as a backend server to provide
#     HTTP based REST APIs
#
# For more details, see the README.md file.
#
######################################################################

import argparse
import json
import flask
import os
import requests
import sys

app = flask.Flask(__name__)

class HomePage:
    def homePage():
        html = "<html>"
        html += "<head>"
        html += "<title>Spread God's Word</title>"
        html += "</head>"
        html += "<body>"
        html += "<h1>Spread God's Word</h1>"
        html += "<hr>"
        html += "<h2><a href=\"languages\">Languages</a><h2>"
        html += "<h2><a href=\"translations\">Translations - All</a><h2>"
        f = open("languages.txt")
        html += "<h3>"
        while(True):
	        line = f.readline()
	        if not line:
		        break
	        line = line.strip()
	        html += "<a href=\"translations\\" + line + "\">[" + line + "</a>] "
        html += "</h3>"
        f.close
        html += "<h2>Books of the Bible</h2>"
        f = open("books.txt")
        html += "<h3>"
        while(True):
	        line = f.readline()
	        if not line:
		        break
	        line = line.strip()
	        html += "<a href=\"references\\" + line + "\">[" + line + "</a>] "
        html += "</h3>"
        f.close
        html += "<h2>Concordance</h2>"
        html += "<form action=\"/concordance\"><h3>"
        html += "<label for=\"translation\">Translation</label>"
        html += "<select id=\"translation\" name=\"translation\">"
        f = open("translations.txt")
        while(True):
            line = f.readline()
            if not line:
                break
            lang, abbr, trans = TranslationAction.parseTranslation(line)
            if abbr == "kjv":
                html += "<option selected value=\"" + abbr + "\"> " + lang + ":" + trans + "</option>"
            else:
                html += "<option value=\"" + abbr + "\"> " + lang + ":" + trans + "</option>"
        f.close()
        html += "</select>"
        html += "<label for=\"search\">Search:</label>"
        html += "<input type=\"text\" id=\"search\" name=\"search\">"
        html += "<button type=\"submit\">Search</button>"
        html += "</h3></form>"
        html += "<hr>"
        html += "<address>Cariessa Taylor<br>August 9, 2021</address>"
        html += "</body>"
        html += "</html>"
        return html

######################################################################
# This class performs the actions for the language requests (i.e. what
# languages are supported by this program?)
######################################################################
class LanguageAction(argparse.Action):
    def languagesAsJson(language_filter=None):
        #get file object
        f = open("languages.txt")
        langs = []
        while(True):
	        line = f.readline()
	        if not line:
		        break
	        if language_filter is None or (language_filter is not None and language_filter.lower() == line.strip().lower()):
	            langs.append(line.strip())
        f.close
        langs_dict = dict()
        langs.sort()
        langs_dict["languages"] = langs
        json_str = json.dumps(langs_dict)
        return json_str

    def __call__(self, parser, namespace, values, option_string=None):
        print(LanguageAction.languagesAsJson(values))


######################################################################
# This class performs the actions for the translations request (i.e.
# what translations are supported by this program?)
######################################################################
class TranslationAction(argparse.Action):
    def translationsAsJson(language_filter=None):
        #get file object
        f = open("translations.txt")
        transDict = dict()
        while(True):
	        line = f.readline()
	        if not line:
		        break
	        lang, abbr, trans = TranslationAction.parseTranslation(line)
	        if lang in transDict:
	            list = transDict[lang]
	        else:
	            list = []
	        another_dict = {}
	        another_dict["language"] = lang
	        another_dict["name"] = trans
	        another_dict["abbreviation"] = abbr
	        if language_filter is None or (language_filter is not None and language_filter.lower() == lang.lower()):
	            list.append(another_dict)
	            transDict[lang] = list
        f.close
        yet_another_dict = dict()
        yet_another_dict["translations"] = transDict
        json_str = json.dumps(yet_another_dict)
        return json_str

    def parseTranslation(line):
        line = line.strip()
        lang = line.split(':')[0].strip()
        trans = line.split(':')[1].strip()
        left = trans.rindex('(')+1
        right = trans.rindex(')')
        abbr = trans[left:right]
        trans = trans[:left-1].strip()
        return lang, abbr, trans

    def __call__(self, parser, namespace, values, option_string=None):
        print(TranslationAction.translationsAsJson(values))


######################################################################
# This class allows the user to look up a verse reference.
######################################################################
class ReferenceAction(argparse.Action):
    def referencesAsJson(reference, translation):
        url = 'https://getbible.net/json?passage=' + reference[0]
        if translation is not None:
            url = url + '&version=' + translation
        response = requests.get(url)
        if response.ok:
            txt = response.text
            txt = txt.lstrip('(')
            txt = txt.rstrip(';')
            txt = txt.rstrip(')')
            return txt
        else:
            return None

    def __call__(self, parser, namespace, values, option_string=None):
        nextIsTranslation = False
        translation = "kjv"
        for arg in sys.argv:
            if nextIsTranslation:
                translation = arg
                break
            if arg == '-v' or arg == '--version':
                nextIsTranslation = True
        print(ReferenceAction.referencesAsJson(values, translation))


######################################################################
# This class performs concordance actions for the program
######################################################################
concord = dict()

class ConcordanceAction(argparse.Action):

    def concordancesAsJson(anyWords, translation):
        ConcordanceAction.buildConcordance(translation)
        wordList = anyWords[0].split(' ')
        if wordList[0].lower() in concord[translation]:
            answer = concord[translation][wordList[0].lower()]
            for i in range(1, len(wordList)):
                if wordList[i].lower() in concord[translation]:
                    answer = answer.intersection(concord[translation][wordList[i].lower()])
                else:
                    answer = set()
            return str(answer)
        else:
            return "NULL"

    def buildConcordance(translation):
        if translation in concord:
            return
        else:
            concord[translation] = dict()
        f = open("books.txt")
        while(True):
            book = f.readline()
            if not book:
                break
            book = book.strip()
            if translation is not None:
                fname = os.path.join("cache", translation + book + ".json")
            else:
                fname = os.path.join("cache", book + ".json")
            if os.path.isfile(fname):
                r = open(fname)
                book_json = r.readline()
                r.close()
            else:
                book_list = []
                book_list.append(book)
                print("Downloading " + book + "...")
                book_json = ReferenceAction.referencesAsJson(book_list, translation)
                c = open(fname, "w")
                c.write(book_json)
                c.close()
            try:
                parsed = json.loads(book_json)
            except json.decoder.JSONDecodeError:
                print("unable to parse")
                continue
            for chapter_nr in parsed["book"]:
                for verse_nr in parsed["book"][chapter_nr]["chapter"]:
                    verse = parsed["book"][chapter_nr]["chapter"][verse_nr]["verse"].strip()
                    for word in verse.split(' '):
                        word = word.replace('.', '')
                        word = word.replace(',', '')
                        word = word.replace(';', '')
                        word = word.replace(':', '')
                        word = word.replace('!', '')
                        word = word.replace('?', '')
                        word = word.replace('(', '')
                        word = word.replace(')', '')
                        word = word.lower()
                        if word in concord[translation]:
                            concord[translation][word].add(book + chapter_nr + ":" + verse_nr)
                        else:
                            concord[translation][word] = set()
                            concord[translation][word].add(book + chapter_nr + ":" + verse_nr)
        f.close
        print('Loaded ' + translation + ', it has ' + str(len(concord[translation].keys())) + ' words')

    def __call__(self, parser, namespace, values, option_string=None):
        nextIsTranslation = False
        translation = "kjv"
        for arg in sys.argv:
            if nextIsTranslation:
                translation = arg
                break
            if arg == '-v' or arg == '--version':
                nextIsTranslation = True
        print(ConcordanceAction.concordancesAsJson(values, translation))


######################################################################
# This class performs the HTTP server actions for the program
######################################################################
class ServerAction(argparse.Action):
    @app.route('/')
    def home():
        return HomePage.homePage()

    @app.route('/languages')
    def languagesAll():
        return LanguageAction.languagesAsJson(None)

    @app.route('/languages/<string:language>')
    def languagesFiltered(language):
        return LanguageAction.languagesAsJson(language)

    @app.route('/translations')
    def translationsAll():
        return TranslationAction.translationsAsJson(None)

    @app.route('/translations/<string:language>')
    def translationsFiltered(language):
        return TranslationAction.translationsAsJson(language)

    @app.route('/references/<string:reference>')
    def references(reference):
        reflist = []
        reflist.append(reference)
        return ReferenceAction.referencesAsJson(reflist, "kjv")

    @app.route('/references/<string:reference>/<string:translation>')
    def refsTrans(reference, translation):
        reflist = []
        reflist.append(reference)
        return ReferenceAction.referencesAsJson(reflist, translation)

    @app.route('/concordance')
    def concordanceForm():
        wordlist = []
        wordlist.append(flask.request.args.get('search'))
        translation = flask.request.args.get('translation')
        return ConcordanceAction.concordancesAsJson(wordlist, translation)

    @app.route('/concordance/<string:anyWord>')
    def concordance(anyWord):
        wordlist = []
        wordlist.append(anyWord)
        return ConcordanceAction.concordancesAsJson(wordlist, "kjv")

    @app.route('/concordance/<string:anyWord>/<string:translation>')
    def concordTrans(anyWord, translation):
        wordlist = []
        wordlist.append(anyWord)
        return ConcordanceAction.concordancesAsJson(wordlist, translation)

    def __call__(self, parser, namespace, values, option_string=None):
       app.run(debug=False)


######################################################################
# This class functions as the main class. It parses the arguments and
# calls the supporting functions to accomplish its goal.
######################################################################
class SpreadGodsWord:
    def parseArguments():
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--print-supported-languages', action=LanguageAction, nargs='?',
            default=None, help='show languages supported and exit')
        parser.add_argument('-t', '--print-supported-translations', action=TranslationAction, nargs='?',
            default=None, help='show translations supported and exit')
        parser.add_argument('-s', '--server', action=ServerAction, nargs=0,
            help='run as a REST server')
        parser.add_argument('-r', '--reference', action=ReferenceAction, nargs=1,
            help='specify reference')
        parser.add_argument('-v', '--version', action=None, nargs=1,
            help='specify versions')
        parser.add_argument('-c', '--concordance', action=ConcordanceAction, nargs=1,
            help= 'concordance')
        args = parser.parse_args()

    def main():
        SpreadGodsWord.parseArguments()

if __name__ == "__main__":
    SpreadGodsWord.main()
