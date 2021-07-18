######################################################################
#
# Cariessa Taylor
# July 17, 2021
# CSIS 483 Phase 1
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

app = flask.Flask(__name__)

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
        langs_dict["languages"] = langs
        langs.sort()
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
	        line = line.strip()
	        lang = line.split(':')[0].strip()
	        trans = line.split(':')[1].strip()
	        left = trans.rindex('(')+1
	        right = trans.rindex(')')
	        abbr = trans[left:right]
	        trans = trans[:left-1].strip()
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

    def __call__(self, parser, namespace, values, option_string=None):
        print(TranslationAction.translationsAsJson(values))

######################################################################
# This class performs the HTTP server actions for the program
######################################################################
class ServerAction(argparse.Action):
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
        args = parser.parse_args()

    def main():
        SpreadGodsWord.parseArguments()

if __name__ == "__main__":
    SpreadGodsWord.main()
