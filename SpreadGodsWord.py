import argparse
import json
import flask

class LanguageAction(argparse.Action):
    def languagesAsJson():
        #get file object
        f = open("languages.txt")
        langs = []
        while(True):
	        line = f.readline()
	        if not line:
		        break
	        langs.append(line.strip())
        f.close
        langs_dict = dict()
        langs_dict["languages"] = langs
        langs.sort()
        json_str = json.dumps(langs_dict)
        return json_str

    def __call__(self, parser, namespace, values, option_string=None):
        print(LanguageAction.languagesAsJson())


class TranslationAction(argparse.Action):
    def translationsAsJson():
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
	        list.append(another_dict)
	        transDict[lang] = list
        f.close
        yet_another_dict = dict()
        yet_another_dict["translations"] = transDict
        json_str = json.dumps(yet_another_dict)
        return json_str

    def __call__(self, parser, namespace, values, option_string=None):
       print(TranslationAction.translationsAsJson())

app = flask.Flask(__name__)

class ServerAction(argparse.Action):
    @app.route('/languages')
    def languages():
        return LanguageAction.languagesAsJson()

    @app.route('/translations')
    def translations():
        return TranslationAction.translationsAsJson()

    def __call__(self, parser, namespace, values, option_string=None):
       app.run(debug=True)


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--languages', action=LanguageAction, nargs=0, help='show languages supported and exit')
    parser.add_argument('-t', '--translations', action=TranslationAction, nargs=0, help='show translations supported and exit')
    parser.add_argument('-s', '--server', action=ServerAction, nargs=0, help='run as a REST server')
    args = parser.parse_args()

def main():
    parseArguments()

if __name__ == "__main__":
    main()
