
import sys
sys.path.append(r'D:\GitHub\Python')
from EricCorePy.Utility.EricUtility import EricUtility

u = EricUtility()
if len(sys.argv) != 2:
    exit

path = sys.argv[1]
print('Start get list, path = ')
print(path)

resultFolder = path + r'\\dup\\'
u.make_folder(resultFolder)

fileColls = u.get_duplicate_file_list(path)
for file in fileColls:
    u.move_file(path + file, resultFolder + file )

print('Finish')
