# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Script created by Dallin Christensen Thursday March 4th, 2021

"""
Purpose
Perform syntax analysis on French phrases to convert them to inverted questions

"""

import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class ComprehendDetect:
    """Encapsulates Comprehend detection functions."""

    def __init__(self, comprehend_client):
        """
        :param comprehend_client: A Boto3 Comprehend client.
        """
        self.comprehend_client = comprehend_client

    def detect_syntax(self, text, language_code):
        """
        Detects syntactical elements of a document. Syntax tokens are portions of
        text along with their use as parts of speech, such as nouns, verbs, and
        interjections.

        :param text: The document to inspect.
        :param language_code: The language of the document.
        :return: The list of syntax tokens along with their confidence scores.
        """
        try:
            response = self.comprehend_client.detect_syntax(
                Text=text, LanguageCode=language_code)
            tokens = response['SyntaxTokens']
            # logger.info("Detected %s syntax tokens.", len(tokens))
        except ClientError:
            logger.exception("Couldn't detect syntax.")
            raise
        else:
            return tokens


partsOfSpeech = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET',
                 'INTJ', 'NOUN', 'NUM', 'O', 'PART', 'PRON',
                 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB']

TestPhrasePunct = [{'TokenId': 1, 'Text': 'Tu', 'BeginOffset': 0, 'EndOffset': 2,
                    'PartOfSpeech': {'Tag': 'PRON', 'Score': 0.9997075200080872}},
                   {'TokenId': 2, 'Text': 'aime', 'BeginOffset': 3, 'EndOffset': 7,
                    'PartOfSpeech': {'Tag': 'VERB', 'Score': 0.9982920289039612}},
                   {'TokenId': 3, 'Text': 'aller', 'BeginOffset': 8, 'EndOffset': 13,
                    'PartOfSpeech': {'Tag': 'VERB', 'Score': 0.9991148114204407}},
                   {'TokenId': 4, 'Text': 'au', 'BeginOffset': 14, 'EndOffset': 16,
                    'PartOfSpeech': {'Tag': 'ADP', 'Score': 0.9997463822364807}},
                   {'TokenId': 5, 'Text': 'magasin', 'BeginOffset': 17, 'EndOffset': 24,
                    'PartOfSpeech': {'Tag': 'NOUN', 'Score': 0.9990205764770508}},
                   {'TokenId': 6, 'Text': '?', 'BeginOffset': 24, 'EndOffset': 25,
                    'PartOfSpeech': {'Tag': 'PUNCT', 'Score': 0.9999500513076782}}]
# {'TokenId': 7, 'Text': 'Moi', 'BeginOffset': 26, 'EndOffset': 29,
#  'PartOfSpeech': {'Tag': 'PRON', 'Score': 0.9687632322311401}},
# {'TokenId': 8, 'Text': ',', 'BeginOffset': 29, 'EndOffset': 30,
#  'PartOfSpeech': {'Tag': 'PUNCT', 'Score': 0.9999955892562866}},
# {'TokenId': 9, 'Text': 'je', 'BeginOffset': 31, 'EndOffset': 33,
#  'PartOfSpeech': {'Tag': 'PRON', 'Score': 0.9999996423721313}},
# {'TokenId': 10, 'Text': 'veux', 'BeginOffset': 34, 'EndOffset': 38,
#  'PartOfSpeech': {'Tag': 'VERB', 'Score': 0.7699386477470398}},
# {'TokenId': 11, 'Text': 'te', 'BeginOffset': 39, 'EndOffset': 41,
#  'PartOfSpeech': {'Tag': 'PRON', 'Score': 0.9978506565093994}},
# {'TokenId': 12, 'Text': 'parler', 'BeginOffset': 42, 'EndOffset': 48,
#  'PartOfSpeech': {'Tag': 'VERB', 'Score': 0.9999996423721313}},
# {'TokenId': 13, 'Text': '.', 'BeginOffset': 48, 'EndOffset': 49,
#  'PartOfSpeech': {'Tag': 'PUNCT', 'Score': 0.999948263168335}}]

TestPhraseWithMultVerbs = [{'TokenId': 1,
                            'Text': 'Je',
                            'BeginOffset': 0,
                            'EndOffset': 2,
                            'PartOfSpeech': {'Tag': 'PRON',
                                             'Score': 0.9999997615814209}
                            },
                           {'TokenId': 2,
                            'Text': 'peux',
                            'BeginOffset': 3,
                            'EndOffset': 7,
                            'PartOfSpeech': {'Tag': 'VERB',
                                             'Score': 0.9804850220680237}
                            },
                           {'TokenId': 3,
                            'Text': 'aller',
                            'BeginOffset': 8,
                            'EndOffset': 13,
                            'PartOfSpeech': {'Tag': 'VERB',
                                             'Score': 0.9998579025268555}
                            },
                           {'TokenId': 4, 'Text': 'au', 'BeginOffset': 14, 'EndOffset': 16,
                            'PartOfSpeech': {'Tag': 'ADP', 'Score': 0.9999063014984131}},
                           {'TokenId': 5, 'Text': 'magasin', 'BeginOffset': 17, 'EndOffset': 24,
                            'PartOfSpeech': {'Tag': 'NOUN', 'Score': 0.9988178610801697}},
                           {'TokenId': 6, 'Text': 'Je', 'BeginOffset': 26, 'EndOffset': 28,
                            'PartOfSpeech': {'Tag': 'PRON', 'Score': 0.9935977458953857}},
                           {'TokenId': 7, 'Text': 'compte', 'BeginOffset': 29, 'EndOffset': 35,
                            'PartOfSpeech': {'Tag': 'VERB', 'Score': 0.9990035891532898}},
                           {'TokenId': 8, 'Text': 'vouloir', 'BeginOffset': 36, 'EndOffset': 43,
                            'PartOfSpeech': {'Tag': 'VERB', 'Score': 0.9990276098251343}},
                           {'TokenId': 9, 'Text': 'faire', 'BeginOffset': 44, 'EndOffset': 49,
                            'PartOfSpeech': {'Tag': 'VERB', 'Score': 0.999724805355072}},
                           {'TokenId': 10, 'Text': 'quelque', 'BeginOffset': 50, 'EndOffset': 57,
                            'PartOfSpeech': {'Tag': 'DET', 'Score': 0.9998217225074768}},
                           {'TokenId': 11, 'Text': 'chose', 'BeginOffset': 58, 'EndOffset': 63,
                            'PartOfSpeech': {'Tag': 'NOUN', 'Score': 0.9996148347854614}}]

TestPhrase = [
    {'TokenId': 1,
     'Text': 'Bonjour',
     'BeginOffset': 0,
     'EndOffset': 7,
     'PartOfSpeech': {'Tag': 'INTJ',
                      'Score': 0.9786997437477112}
     },
    {'TokenId': 2,
     'Text': 'je',
     'BeginOffset': 8,
     'EndOffset': 10,
     'PartOfSpeech': {'Tag': 'PRON',
                      'Score': 1.0}
     },
    {'TokenId': 3,
     'Text': 'suis',
     'BeginOffset': 11,
     'EndOffset': 15,
     'PartOfSpeech': {'Tag': 'AUX',
                      'Score': 0.9963362216949463}
     },
    {'TokenId': 4,
     'Text': 'content',
     'BeginOffset': 16,
     'EndOffset': 23,
     'PartOfSpeech': {'Tag': 'ADJ',
                      'Score': 0.9582428932189941}
     }
]

interrogativePronouns = ['comment', 'quand', 'qui', 'où', 'd\'où', 'combien',
                         'quel', 'quelle', 'pourquoi', 'quels', 'quelles']


def usage_demo():
    print('-' * 88)
    # print("Welcome to the Amazon Comprehend detection demo!")

    # logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    comp_detect = ComprehendDetect(boto3.client('comprehend'))
    try:
        value = input("Mettez votre phrase ici:")
        print('-' * 88)
    except SyntaxError:
        value = ""
    if not value.lower() == "none":
        sample_text = value
    else:
        with open('detect_sample.txt') as sample_file:
            sample_text = sample_file.read()
            sample_text = sample_text.lower()
    while value != 'END':
        print("Détectant des éléments de syntaxe.")
        # analyze text to find newlines and add question marks
        if not sample_text.find('je peux') == -1:
            sample_text = sample_text.replace('peux', 'puis')
        if not sample_text.find('qu\'est-ce que') == -1:
            sample_text = sample_text.replace('qu\'est-ce que', 'que')
        elif not sample_text.find('qu\'est-ce qu\'') == -1:
            sample_text = sample_text.replace('qu\'est-ce qu\'', 'que ')
        if not sample_text.find('est-ce que') == -1:
            sample_text = sample_text.replace('est-ce que', '')
        elif not sample_text.find('est-ce qu\'') == -1:
            sample_text = sample_text.replace('est-ce qu\'', ' ')
        syntax_tokens = comp_detect.detect_syntax(sample_text, 'fr')
        disclaimer = ''
        try:
            for i in syntax_tokens:
                if i['PartOfSpeech']['Score'] < .9:
                    disclaimer = '\n' + color.BOLD + color.YELLOW + "*AVERTISSEMENT*" + color.END + '\n' \
                                 + 'Vu que l\'intervalle de confiance du mot ' + color.BOLD + \
                                 color.YELLOW + i['Text'].upper() + \
                                 color.END + ' est moins de 90%, la précision de ce changement de ' \
                                             'phrase ne peut être garantie.' + '\n'


            # Use TestPhrase instead of calling the API - this will save some data
            # Make a list of words with Partof speech

            wordWithPart = []
            for index, value in enumerate(syntax_tokens):  # Replace with syntax_tokens/TestPhrase when testing
                wordWithPart.append((value['Text'], value['PartOfSpeech']['Tag']))

            interrogPron = ''
            for i, value in enumerate(wordWithPart):
                if value[0].lower() in interrogativePronouns:
                    wordWithPart.remove(value)
                    interrogPron = value[0] + ' '
                    break

            # If there isn't punctuation after each phrase
            verbIndex = []
            pronounIndex = []
            foundVerb = False
            foundPron = False
            for index, each in enumerate(wordWithPart):
                if foundVerb and foundPron:
                    break
                if not foundVerb and each[1] == 'VERB' or each[1] == 'AUX':  # Distinguish between AUX and VERB
                    foundVerb = True
                    verbIndex.append(index)

                elif not foundPron and each[1] == 'PRON':
                    foundPron = True
                    pronounIndex.append(index)
                elif not each[0] == ',' and each[1] == 'PUNCT':
                    foundVerb = False
                    foundPron = False
            # print(wordWithPart)

            # have user indicate gender pronoun to account for this
            foundPronAfter = False
            addedPronoun = ""
            while not foundPron:
                gender = input("Indiquez le sexe/genre du sujet. Mettez masc ou fém").lower()
                if gender == "masc":
                    addedPronoun = "il"
                    foundPron = True
                    foundPronAfter = True
                elif gender == "fém":
                    addedPronoun = "elle"
                    foundPron = True
                    foundPronAfter = True
            addComma = ''
            if foundPronAfter:
                tempTuple = (addedPronoun, 'PRON')
                for index, word in enumerate(wordWithPart):
                    if word[1] == 'VERB' or word[1] == 'AUX':
                        wordWithPart.insert(index, tempTuple)
                        # wordWithPart.insert(index, (',', 'PUNCT'))
                        addComma = ', '
                        pronounIndex.append(index)
                        verbIndex.clear()
                        verbIndex.append(index + 1)
                        break

            # Figure out how to insert the pronoun if there is none initially
            # now figure out just a subject like, "mon père"
            for index, verb in enumerate(verbIndex):
                wordWithPart[verbIndex[index]], wordWithPart[pronounIndex[index]] = wordWithPart[pronounIndex[index]], \
                                                                                    wordWithPart[verbIndex[index]]
            stringBuilder = ''
            stringBuilder += interrogPron  # TODO: Look at this again
            tempString = ''
            firstWord = True
            index = 0
            while len(wordWithPart) > 0:
                if wordWithPart[index][1] != 'VERB' and wordWithPart[index][1] != 'AUX':
                    if firstWord:
                        if wordWithPart[index][0] == ',':
                            tempString = tempString[:-1]
                        if wordWithPart[index][1] == 'DET' and wordWithPart[index][0][len(wordWithPart[index][0]) - 1] == '\'':
                            tempString += wordWithPart[index][0]
                        else:
                            tempString += wordWithPart[index][0] + ' '

                        firstWord = False
                    else:
                        if wordWithPart[index][0] == ',':
                            tempString = tempString[:-1]
                        if wordWithPart[index][1] == 'DET' and wordWithPart[index][0][len(wordWithPart[index][0]) - 1] == '\'':
                            tempString += wordWithPart[index][0]
                        else:
                            tempString += wordWithPart[index][0] + ' '


                    del wordWithPart[index]
                else:
                    firstWord = True
                    break

            for index, each in enumerate(wordWithPart):
                if not each[0] == '?' and each[1] == 'PUNCT':
                    stringBuilder = stringBuilder[:-1]
                    if not each[0] == ',':
                        stringBuilder += ' ?'
                        stringBuilder += '\n'
                        firstWord = True
                    else:
                        stringBuilder += each[0]
                        stringBuilder += ' '
                elif each[0] == '?':
                    stringBuilder += each[0]
                    stringBuilder += '\n'
                    firstWord = True
                else:
                    if firstWord:
                        if not foundPronAfter:
                            stringBuilder += each[0]
                        else:
                            stringBuilder += each[0]
                        stringBuilder += '-'
                        if each[0][-1] == 'a' or each[0][-1] == 'e':  # handle interrogative words like comment and quand
                            stringBuilder += 't-'
                        firstWord = False
                    else:
                        stringBuilder += each[0]
                        stringBuilder += ' '
            if '?' not in stringBuilder:
                stringBuilder += '?'

            print(disclaimer)
            if len(tempString) > 0:
                if tempString[len(tempString) - 1] == ' ' and tempString[len(tempString) - 2] != ',':
                    tempString = tempString[:-1]
                    if tempString.lower() not in 'que':
                        tempString += ', '
                    else:
                        tempString += ' '
                    # tempString += addComma
            totalString = tempString + stringBuilder
            total = ''
            if totalString.find(' ,') != -1:
                firstHalf = totalString[:totalString.find(' ,')] + ', '
                secondHalf = totalString[totalString.find(',') + 1:]
                print(firstHalf)
                print(secondHalf)
                total = firstHalf + secondHalf
            if len(total) > 0:
                print(total)
            else:
                print(tempString + stringBuilder.lower())
            print('-' * 88)
        except IndexError or SyntaxError:
            print(color.RED + "Incapable d'invertir votre phrase. Veuillez essayer une phrase différente.")
        try:
            value = input("Mettez votre phrase ici:")
            print('-' * 88)
        except SyntaxError:
            value = ""
        if not value.lower() == "none":
            sample_text = value
        else:
            with open('detect_sample.txt') as sample_file:
                sample_text = sample_file.read()
                sample_text = sample_text.lower()

if __name__ == '__main__':
    usage_demo()
