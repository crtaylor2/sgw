import argparse

class LanguageAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print("TODO SHOW LANGUAGES")

class TranslationAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print("TODO SHOW TRANSLATIONS")

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--languages', action=LanguageAction, nargs=0, help='show languages supported and exit')
    parser.add_argument('-t', '--translations', action=TranslationAction, nargs=0, help='show translations supported and exit')
    args = parser.parse_args()

def main():
    parseArguments()

if __name__ == "__main__":
    main()
