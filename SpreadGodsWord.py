import argparse
import json

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
        
        langs.sort()
        json_str = json.dumps(langs)
        print (json_str)

    def __call__(self, parser, namespace, values, option_string=None):
        LanguageAction.languagesAsJson()


class TranslationAction(argparse.Action):
    def translationsAsJson():
        #get file object
        f = open("translations.txt")
        transl = []
        while(True):
	        line = f.readline()
	        if not line:
		        break
	        transl.append(line.strip())
        f.close
        
        transl.sort()
        json_str = json.dumps(transl)
        print (json_str)

    def __call__(self, parser, namespace, values, option_string=None):
       TranslationAction.translationsAsJson()


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--languages', action=LanguageAction, nargs=0, help='show languages supported and exit')
    parser.add_argument('-t', '--translations', action=TranslationAction, nargs=0, help='show translations supported and exit')
    args = parser.parse_args()

def main():
    parseArguments()

if __name__ == "__main__":
    main()
