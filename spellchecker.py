# -*- coding: utf-8 -*-

#                       __ __        __                __
#   .-----.-----.-----.|  |  |.----.|  |--.-----.----.|  |--.-----.----.
#   |__ --|  _  |  -__||  |  ||  __||     |  -__|  __||    <|  -__|   _|
#   |_____|   __|_____||__|__||____||__|__|_____|____||__|__|_____|__|
#         |__|
#
#   Creaeted by Annika, Christina, Erik, Qian, Seda and Vita
#
#   SE Einführung in die maschinelle Sprachverarbeitung mit Python
#   SoSe2016
#
#   Version 0.1.0


import sys
import re

try:
    from termcolor import colored
except ImportError:
    print("please install termcolor by executing: 'sudo pip3 install termcolor'")

from nltk.tokenize import sent_tokenize, word_tokenize

try:
  import enchant
except ImportError:
  print("please install execute: `pip install pyenchant`")

WORD = re.compile(r'^\w+$')


def intro():
  print('                    __ __        __                __               ')
  print('.-----.-----.-----.|  |  |.----.|  |--.-----.----.|  |--.-----.----.')
  print('|__ --|  _  |  -__||  |  ||  __||     |  -__|  __||    <|  -__|   _|')
  print('|_____|   __|_____||__|__||____||__|__|_____|____||__|__|_____|__|  ')
  print('      |__|                                                          ')
  print('*********************************************************************\n')

  txt = "Hi there!\nI'm your spellchecker. Show me the path to your file that holds the text\n" + \
        "that should be processed. You'd further need to specify the language in which your \n" + \
        "text is written and an output file. Let's go ..\n\n"
  print(txt)


# first task
def read_file():
  file_found = False
  while not file_found:
    path = input(highlight('Please enter the file directory: ', 0)) #übersetzt ins Englische
    try:
      with open(path) as f:
        text = f.read()
    except IOError:
      print(highlight('File not found.\n', 1), file=sys.stderr)
    else:
      file_found = True
      print(highlight('ok.\n', 2))
      return text


def turn_into_corpus(text):
  return [word_tokenize(sent) for sent in sent_tokenize(text)]


# Folgendes neu von Seda+Christina eingefügt: Oberfläche für die Wahl einer Sprache
def select_language():
  available_languages = enchant.list_languages()
  selected_language = None
  print(highlight("Please select a language: ", 0))
  print(available_languages)
  for i, s in enumerate(available_languages):
    print(i, '-', s)
  while not selected_language:
    try:
      n = int(input('? '))
      selected_language = available_languages[n]
    except (IndexError, ValueError):
      print(highlight('You did not select a language!\n',1))
  print("You selected %s.\n" % highlight(selected_language, 2))
  return selected_language


def look_for_suggestions(sentences, language):
  d = enchant.Dict(language)
  for sent in sentences:
    sentence_and_suggestions = []
    for word in sent:
      if WORD.match(word) and not d.check(word):
        suggestions = d.suggest(word)
      else:
        suggestions = []
      sentence_and_suggestions.append((word, suggestions))
    yield sentence_and_suggestions


def ask_for_correction(sentences_and_suggestions):
  for sentence in sentences_and_suggestions:
    corrected_sentence = []
    for word, suggestions in sentence:
      if suggestions:
        print()
        print('Sentence:', ' '.join(w for w, sug in sentence))
        print('You wrote "%s", this will be replaced with' % colored(word, 'red'))
        for i, s in enumerate(suggestions):
          print(i, '-', s)
        print('%i - enter custom value' % len(suggestions))
        print('%s - keep original' % (len(suggestions)+1))
        pick = None
        while not pick:
          try:
            n = int(input('? '))
            if n == len(suggestions):
              word = input(highlight('>> ', 0))
            elif n == len(suggestions) +1 :
              word = word
            else:
              word = suggestions[n]
            pick = True
            print(highlight('ok.',2))
          except (IndexError, ValueError):
            print(highlight('Oops. Pick a value between 0 and %s\n' % len(suggestions),1))
      corrected_sentence.append(word)
    yield corrected_sentence


def write_file(sentences):
  output_file = input(highlight('Which name do you wish your corrected file to have? ', 0)) #ermöglicht dem User die Wahl des Dateinamens
  with open(output_file, 'w') as f:
    for sentence in sentences:
      f.write(' '.join(sentence) + '\n')
  print('\nCorrected text saved in: %s' % highlight(output_file, 2))


def highlight (txt, typeof):
  if typeof == 0: # declarative
    return colored(txt, 'yellow', attrs=['bold'])
  elif typeof == 1: # error
    return colored(txt, 'red', attrs=['bold'])
  elif typeof == 2: # success
    return colored(txt, 'green', attrs=['bold'])


def byebye ():
  print(highlight('\n\nBye bye!', 2))


def main():
  try:
    intro()
    text = read_file()
    corpus = turn_into_corpus(text)
    selected_language = select_language() #neue Funktion
    sentences_and_suggestions = look_for_suggestions(corpus, selected_language)
    corrected_sentences = ask_for_correction(sentences_and_suggestions)
    write_file(corrected_sentences)
    byebye()
  except (KeyboardInterrupt, EOFError):
    byebye()

if __name__ == '__main__':
    main()
