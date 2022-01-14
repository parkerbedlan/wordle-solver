

global words
global letters
words = []
letters = []

def initializeWords():
  global words
  f = open('dictionary.txt', 'r')
  words = [w.strip() for w in f.readlines() if len(w) == 6]

  freqs = {'e': 56.88, 'a': 43.31, 'r': 38.64, 'i': 38.45, 'o': 36.51, 't': 35.43, 'n': 33.92, 's': 29.23, 'l': 27.98, 'c': 23.13, 'u': 18.51, 'd': 17.25, 'p': 16.14, 'm': 15.36, 'h': 15.31, 'g': 12.59, 'b': 10.56, 'f': 9.24, 'y': 9.06, 'w': 6.57, 'k': 5.61, 'v': 5.13, 'x': 1.48, 'z': 1.39, 'j': 1.00, 'q': 1}
  def diversity(word):
    return -1 * len(set([letter for letter in word]))
  def total_freq(word):
	  return -1 * sum([freqs[letter] for letter in word])
  def sorter(word):
	  return diversity(word)*100 + total_freq(word)
  
  words.sort(key=sorter)


def initializeLetters():
  global letters
  letters = dict([[chr(i),{'good_indexes': set(), 'bad_indexes': set(), 'included': None}] for i in range(97, 97+26)])


def initialize():
  initializeWords()
  initializeLetters()


def guess(results):
  global words
  global letters
  changed_letters = set()
  for index in range(5):
    result = results[index]
    letter = result[0]
    color = result[1]
    if color == 'g':
      if index not in letters[letter]['good_indexes']:
        changed_letters.add(letter)
        letters[letter]['good_indexes'].add(index)
        if index in letters[letter]['bad_indexes']:
          letters[letter]['bad_indexes'].remove(index)
        letters[letter]['included'] = True
    elif color == 'y':
      if index not in letters[letter]['bad_indexes']:
        changed_letters.add(letter)
        letters[letter]['bad_indexes'].add(index)
        letters[letter]['included'] = True
    elif color == 'b':
      changed_letters.add(letter)
      if letters[letter]['included']:
        letters[letter]['bad_indexes'].add(index)
      else:
        for i in range(5):
          letters[letter]['bad_indexes'].add(i)
        letters[letter]['included'] = False
  
  for letter in changed_letters:
    for good_index in letters[letter]['good_indexes']:
      words = [w for w in words if w[good_index] == letter]
    for bad_index in letters[letter]['bad_indexes']:
      words = [w for w in words if w[bad_index] != letter]
    if letters[letter]['included']:
      words = [w for w in words if letter in w]
  
  return words[0:10]