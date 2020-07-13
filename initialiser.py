lines_to_copy = []
copy = []

with open("template.txt", "r") as file:
    lines_to_copy = file.readlines()
        #line = line.rstrip("\n") + r"\n"
        #if '\\' in line:
        #    line = line.replace("\\", "\\\\")

        #if line.strip('\n') != '':
        #    line = line.strip('\n') + r'\n'
    print(lines_to_copy)


with open("test1.tex", "w") as newFile:
    item = 0
    while lines_to_copy[item] != '\\begin{document}\n':
        newFile.write(lines_to_copy[item])
        item = item + 1
    print("Found begin document statement!")


    newFile.close()