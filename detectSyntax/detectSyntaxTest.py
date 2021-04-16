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

class Color:
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

interrogatives = ['comment', 'quand', 'qui', 'où', 'd\'où', 'combien', 'combien de', 'quel', 'quelle', 'pourquoi', 'quels', 'quelles']

pronomsObjets = ['me', 'm\'', 't\'', 'se', 's\'', 'te', 'nous',
                 'vous', 'le', 'la', 'l\'', 'les', 'lui', 'leur', 'y', 'en']

apostropheObjects = ['m\'', 't\'', 'l\'', 's\'']


def usage_demo():
    print('-' * 88)
    phraseList = []
    comp_detect = ComprehendDetect(boto3.client('comprehend'))  # Use AWS Comprehend with boto3
    try:
        value = input("Mettez votre phrase ici:")  # Ask for user input
        print('-' * 88)
    except SyntaxError:
        value = ""
    if not value.lower() == "none":  # This allows for user to either use detect_sample.txt or their own phrase
        sample_text = value.lower()
        phraseList.append(sample_text)
    else:
        with open('detect_sample.txt') as sample_file:  # In case there are several phrases in the file
            for line in sample_file.readlines():
                phraseList.append(line.lower())
            # sample_text = sample_text.lower()
    while value != 'END':
        print("Détectant des éléments de syntaxe.")
        for phraseCount, sample_text in enumerate(phraseList):
            initialPhrase = sample_text  # hang onto phrase to output later

            # Adapt peux --> puis and remove (Que/qu')est-ce que/qu'
            if not initialPhrase.find('je peux') == -1:
                sample_text = sample_text.replace('peux', 'puis')
            if not initialPhrase.find('qu\'est-ce que') == -1:
                sample_text = sample_text.replace('qu\'est-ce que', 'que')
            elif not initialPhrase.find('qu\'est-ce qu\'') == -1:
                sample_text = sample_text.replace('qu\'est-ce qu\'', 'que ')
            if not initialPhrase.find('est-ce que') == -1:
                sample_text = sample_text.replace('est-ce que', '')
            elif not initialPhrase.find('est-ce qu\'') == -1:
                sample_text = sample_text.replace('est-ce qu\'', ' ')
            syntax_tokens = comp_detect.detect_syntax(sample_text, 'fr')

            wordWithPart = []
            for index, value in enumerate(syntax_tokens):  # Replace with syntax_tokens/TestPhrase when testing
                wordWithPart.append((value['Text'], value['PartOfSpeech']['Tag']))

            for i, value in enumerate(wordWithPart):
                if value[0].lower() in interrogatives:  # This will remove the interrogative before moving things
                    wordWithPart.remove(value)
                    break

            # this ensures that all the pronouns that precede the conjugated verb stay in front
            pronoms = ''
            for word in pronomsObjets:
                for i, text in enumerate(wordWithPart):
                    if text[1] == 'VERB' or text[1] == 'AUX':
                        break

                    if word == text[0] and text[1] != 'DET' and i != 0:
                        pronoms += word
                        if word not in apostropheObjects:  # Only add space if there isn't an apostrophe
                            pronoms += ' '
                        del syntax_tokens[i]  # Remove pronouns from syntax_tokens object
                        continue
                else:
                    break
                continue

            # This will check for confidence level of syntax analysis
            disclaimer = ''
            try:
                for i in syntax_tokens:
                    if i['PartOfSpeech']['Score'] < .9:
                        disclaimer = '\n' + Color.BOLD + Color.YELLOW + "*AVERTISSEMENT*" + Color.END + '\n' \
                                     + 'Vu que l\'intervalle de confiance du mot ' + Color.BOLD + \
                                     Color.YELLOW + i['Text'].upper() + \
                                     Color.END + ' est moins de 90%, la précision de ce changement de ' \
                                                 'phrase ne peut être garantie.' + '\n'

                # Clear the list and start over to account for nous and vous not as object pronouns
                wordWithPart.clear()
                interrogatif = ''
                wordWithPart = []
                for index, value in enumerate(syntax_tokens):  # Replace with syntax_tokens/TestPhrase when testing
                    wordWithPart.append((value['Text'], value['PartOfSpeech']['Tag']))

                for i, value in enumerate(wordWithPart):
                    if value[0].lower() in interrogatives:  # This will remove the interrogative before moving things
                        wordWithPart.remove(value)
                        interrogatif = value[0] + ' '
                        break

                # This will find the verb and subject pronoun so that they can switch places later
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

                # have user indicate gender pronoun to account for this
                # Sometimes the gender isn't clear, so the user will be prompted to put the intended gender
                foundPronAfter = False
                addedPronoun = ""
                while not foundPron:
                    gender = input("Indiquez le sexe/genre du sujet. Mettez masc ou fém:  ").lower()
                    if gender == "masc":
                        addedPronoun = "il"
                        foundPron = True
                        foundPronAfter = True
                    elif gender == "fém":
                        addedPronoun = "elle"
                        foundPron = True
                        foundPronAfter = True
                if foundPronAfter:
                    tempTuple = (addedPronoun, 'PRON')
                    for index, word in enumerate(wordWithPart):
                        if word[1] == 'VERB' or word[1] == 'AUX':
                            wordWithPart.insert(index, tempTuple)
                            pronounIndex.append(index)
                            verbIndex.clear()
                            verbIndex.append(index + 1)
                            break
                # Swap verb and subject pronoun in list
                for index, verb in enumerate(verbIndex):
                    wordWithPart[verbIndex[index]], wordWithPart[pronounIndex[index]] = wordWithPart[
                                                                                            pronounIndex[index]], \
                                                                                        wordWithPart[verbIndex[index]]
                stringBuilder = ''
                tempString = ''
                firstWord = True
                index = 0
                # Now time to build the first part, basically the subject
                while len(wordWithPart) > 0:
                    if wordWithPart[index][1] != 'VERB' and wordWithPart[index][1] != 'AUX':
                        if firstWord:
                            if wordWithPart[index][0] == ',':
                                tempString = tempString[:-1]
                            if (wordWithPart[index][1] == 'DET' or wordWithPart[index][1] == 'ADP' or
                                wordWithPart[index][1] == 'PRON') \
                                    and wordWithPart[index][0][len(wordWithPart[index][0]) - 1] == '\'':
                                tempString += wordWithPart[index][0]  # This is to handle apostrophes
                            else:
                                tempString += wordWithPart[index][0] + ' '

                            firstWord = False
                        else:
                            if wordWithPart[index][0] == ',':
                                tempString = tempString[:-1]
                            if wordWithPart[index][1] == 'DET' and \
                                    wordWithPart[index][0][len(wordWithPart[index][0]) - 1] == '\'':
                                tempString += wordWithPart[index][0]
                            else:
                                tempString += wordWithPart[index][0] + ' '

                        del wordWithPart[index]
                    else:
                        firstWord = True
                        break

                # This is for the rest of the phrase, starting at the first conjugated verb
                for index, each in enumerate(wordWithPart):
                    if each[0].lower() == 'j\'':
                        tempTuple = ('je', 'PRON')
                        del wordWithPart[index]
                        wordWithPart.insert(index, tempTuple)
                        stringBuilder += tempTuple[0]
                        stringBuilder += ' '
                        continue

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
                            if (each[0][-1] == 'a' or each[0][-1] == 'e') and index < len(wordWithPart) - 1 \
                                    and (wordWithPart[index + 1][0].lower() != 'j\''
                                         and wordWithPart[index + 1][0].lower() != 'je'):
                                stringBuilder += 't-'  # handle interrogative words like comment and quand
                            firstWord = False
                        elif each[0] in apostropheObjects:
                            stringBuilder += each[0]
                        else:
                            stringBuilder += each[0]
                            stringBuilder += ' '
                if '?' not in stringBuilder:
                    stringBuilder += '?'

                print(disclaimer)

                # Interrogatives + subject + any object pronouns + verb phrase
                totalString = interrogatif + tempString + pronoms + stringBuilder.lower()
                print(str(phraseCount + 1) + '. ' + 'Phrase originale: ' + initialPhrase)
                print('\t' + 'Phrase invertie: ' + totalString)
                print('-' * 88)
            except IndexError or SyntaxError:
                print(Color.RED + "Incapable d'invertir votre phrase. Veuillez essayer une phrase différente.")
        try:
            value = input("Mettez votre phrase ici:")
            phraseList.clear()
            print('-' * 88)
        except SyntaxError:
            value = ""
        if not value.lower() == "none":
            sample_text = value.lower()
            phraseList.append(sample_text)
        else:
            with open('detect_sample.txt') as sample_file:
                for line in sample_file.readlines():
                    phraseList.append(line.lower())


if __name__ == '__main__':
    usage_demo()
