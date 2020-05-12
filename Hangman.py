
import random
HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\  |
 / \  |
     ===''']
words = {'Colores':'rojo naranja amarillo verde azul lila violeta blanco negro marron'.split(),
'Figuras':'cuadrado triangulo rectangulo circulo elipse rombo trapezoide pentagono hexagono heptagono octogono'.split(),
'Frutas': 'manzana naranja limon lima pera sandia uva cereza banana mango frutilla'.split(),
'Animales':'murcielago oso castor gato puma ciervo perro burro pato aguila pez rana cabra sanguijuela leon lagartija mono alce raton nutria buho panda piton conejo rata tiburon oveja zorrino calamar tigre pavo tortuga comadreja ballena lobo wombat zebra'.split()}

def getRandomWord(wordDict):
    ''' This function returns a random string from the passed dictionary of lists of strings, and the key also.'''

    # First, randomly select a key from the dictionary:
    wordKey = random.choice(list(wordDict.keys()))

    # Second, randomly select a word from the key's list in the dictionary:
    wordIndex = random.randint(0, len(wordDict[wordKey]) - 1)

    return [wordDict[wordKey][wordIndex], wordKey]

def displayBoard(missedLetters, correctLetters, secretWord):
    print(HANGMAN_PICS[len(missedLetters)])
    print()

    print('Letras erradas:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): # replace blanks with correctly guessed letters
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks: # show the secret word with spaces in between each letter
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed):
    # Returns the letter the player entered. This function makes sure the player entered a single letter, and not something else.
    while True:
        print('Adiviná una letra.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Por favor ingresá una sóla letra.')
        elif guess in alreadyGuessed:
            print('Ya usaste esa letra en un intento anterior. Elegí otra.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Por favor ingresá una LETRA.')
        else:
            return guess

def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('¿Querés jugar de nuevo? (sí o no)')
    return input().lower().startswith('y')

def main(*args):

    if len(args) != 0:
        intentos = args[0]
    else:
        intentos = 0

    print('A H O R C A D O')

    difficulty = 'X'
    while difficulty not in 'FID':
      print('Ingrese la dificultad: F - Fácil, I - Intermedio, D - Difícil')
      difficulty = input().upper()
    if difficulty == 'I':
        del HANGMAN_PICS[3]
    if difficulty == 'D':
        del HANGMAN_PICS[5]
        del HANGMAN_PICS[3]
        del HANGMAN_PICS[2]

    missedLetters = ''
    correctLetters = ''
    secretWord, secretSet = getRandomWord(words)
    gameIsDone = False

    while True:


        print('La palabra está en el grupo: ' + secretSet)
        displayBoard(missedLetters, correctLetters, secretWord)

        # Let the player type in a letter.
        guess = getGuess(missedLetters + correctLetters)

        if guess in secretWord:
            correctLetters = correctLetters + guess

            # Check if the player has won
            foundAllLetters = True
            for i in range(len(secretWord)):
                if secretWord[i] not in correctLetters:
                    foundAllLetters = False
                    break
            if foundAllLetters:
                print('¡Sí, la palabra es "' + secretWord + '"! ¡Ganaste!')
                gameIsDone = True
        else:
            missedLetters = missedLetters + guess

            # Check if player has guessed too many times and lost.
            if len(missedLetters) == len(HANGMAN_PICS) - 1:
                displayBoard(missedLetters, correctLetters, secretWord)
                print('¡Te quedaste sin intentos!\nDespués de ' + str(len(missedLetters)) + ' intentos fallidos y ' + str(len(correctLetters)) + ' correctos, la palabra era "' + secretWord + '"')
                gameIsDone = True

        # Ask the player if they want to play again (but only if the game is done).
        if gameIsDone:

            intentos += 1

            if playAgain():
                missedLetters = ''
                correctLetters = ''
                gameIsDone = False
                secretWord, secretSet = getRandomWord(words)
            else:
                if __name__ == '__main__':
                    break
                else:
                    return intentos

if __name__ == '__main__':
    main()
