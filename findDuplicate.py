
import sys
sys.path.append(r'D:\GitHub\Python')
from EricCorePy.Utility.EricUtility import EricUtility

if len(sys.argv) != 2:
    exit

path = sys.argv[1]
path = path + r'\\'
print('Start get list, path = ')
print(path)

resultFolder = path + r"dup\\"

u = EricUtility()
u.make_folder(resultFolder)

fileColls = u.get_duplicate_file_list_by_compare_file_data(path)
for file in fileColls:
    u.move_file(path + file, resultFolder + file )

print('Finish')
