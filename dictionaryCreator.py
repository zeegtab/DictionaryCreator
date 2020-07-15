import subprocess
import os

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

class Dictionary:
    def __init__(self, newName='', newAuthor='Unknown', newDate='Unknown'):
        self.name = newName
        self.author = newAuthor
        self.date = newDate
        self.words = {1: 'Hoisting'}
        self.wordList = ['Hoisting']
        self.definitions = {'Hoisting': 'When an interpreter (such as the JavaScript interpreter) raises all defined functions to the top of the code before the main program is executed. This means that a function can be called before it has been defined.'}
        self.types = {'Hoisting':'Verb'}
        self.file = 'untitled'

    def add_entry(self, newEntry, type=''):

        print('The new word to be added is: ' + newEntry)
        if self.__confirm_entry(newEntry):
            print("Great! Adding new word...")

            self.wordList.append(newEntry)
            self.wordList.sort()

            print(self.wordList)

            self.__list_to_dict()

            self.definitions[newEntry] = '{No Definition}'
            self.types[newEntry] = type

            print("\nUpdated dictionary:")
            print(self.words)

        else:
            print("Entry not added.")


    def __confirm_entry(self, newEntry):

        message = "The new word: '" + newEntry + "' will be inserted "
        tempList = []

        for i in range(1, len(self.words) + 1):
            tempList.append(self.words[i])

        tempList.append(newEntry)
        tempList.sort()

        if tempList.index(newEntry) != 0:
            message = message + "after " + tempList[tempList.index(newEntry) - 1]

        if (tempList.index(newEntry) > 0) and (tempList.index(newEntry) < (len(tempList) - 1)):
            message = message + " and "

        if tempList.index(newEntry) != (len(tempList) - 1):
            message = message + "before " + tempList[tempList.index(newEntry) + 1]

        print(message + ".")

        choice = input("Continue? (Y) Otherwise cancelled.")
        if choice == 'Y' or choice == 'y':
            return True
        else:
            return False

    def __list_to_dict(self):
        self.words = {}
        entryNum = 1
        for word in self.wordList:
            self.words[entryNum] = word
            entryNum += 1
        return self.words

    def add_definition(self, entry):
        if entry in self.wordList:
            print("Entry found in dictionary...")
            print("Would you like to add a definition to the entry: " + entry + "? (Y otherwise cancelled)")

            choice = input()
            confirmation = ''

            while confirmation != 'Y' or confirmation != 'y':
                if choice == 'Y' or choice == 'y':
                    current_definition = str(input("Enter the definition below:\n"))

                    print(entry + ": " + current_definition)
                    print("Are you satisfied with this definition?")

                    confirmation = input()
                    if confirmation == 'Y' or confirmation == 'y':
                        self.definitions[entry] = current_definition
                        print("Confirmed. Definition has been added to dictionary.")
                        break

    def generate_file(self, filename):
        self.file = filename

        lines_to_copy = []
        with open("template.txt", "r") as file:
            for line in file:
                lines_to_copy.append(line)

        with open(self.file + '.tex', "w") as newFile:
            item = 0
            while lines_to_copy[item] != '\\begin{document}\n':
                newFile.write(lines_to_copy[item])
                item = item + 1
            print("Found begin document statement!")

            newFile.write('\\begin{document}\n')

            newFile.write('\\title{' + self.name + '}\n')
            newFile.write('\\author{' + self.author + '}\n')
            newFile.write('\\date{' + self.date + '}\n')
            newFile.write('\\maketitle\n')

            newFile.write('\\section*{' + self.words[1][0] + '}\n')

            newFile.write('\\begin{multicols}{2}\n')

            current_section = self.wordList[0][0]

            for word_counter in range(0, len(self.words)):
                if current_section != self.words[word_counter+1][0]:
                    current_section = self.words[word_counter+1][0]

                    newFile.write('\\end{multicols}\n')
                    newFile.write('\\section*{' + current_section.upper() + '}\n')
                    newFile.write('\\begin{multicols}{2}\n')

                self.generate_definition(newFile, self.words[word_counter + 1],
                                         self.types[self.words[word_counter + 1]],
                                         self.definitions[self.words[word_counter + 1]])

            newFile.write('\\end{multicols}\n')
            newFile.write('\\end{document}')

            newFile.close()

    def generate_definition(self, fileIterator, entryName, entryType, entryDef):
        fileIterator.write('\\entry{'+entryName+'}{'+entryType + '}{'+entryDef+'}\n\n')
        return

    def compile(self):
        x = os.system('pdflatex ' + self.file + '.tex')

        if x != 0:
            print("Oh no the exit code wasn't 0!!")
        else:
            os.system('open ' + self.file + '.pdf')



myDict = Dictionary('Computer Science Dictionary', 'Zarya Mekathotti', 'July 2020')
myDict.add_entry('Algorithm', 'Noun')
myDict.add_definition('Algorithm')

myDict.add_entry('Machine Learning', 'Noun')
myDict.add_definition('Machine Learning')

myDict.generate_file('newdictionary')
myDict.compile()


