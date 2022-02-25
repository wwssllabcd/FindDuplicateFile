
import sys
from os import listdir
from os.path import isfile, join

sys.path.append(r'D:/GitHub/Python')
from EricCorePy.Utility.EricUtility import EricUtility

#------------------------
# window command line 切換到 utf-8
# chcp 65001
#-----------------
if __name__ == '__main__':
    u = EricUtility()

    folderPath = "E:\Cute_DL\webcam\g"
    print(folderPath)
    files = listdir(folderPath)

    res = "chcp 65001" + u.crlf()
    revert = "chcp 65001" + u.crlf()
    for f in files:
        newFileName = f.replace("", "") 
        res += 'ren "' + folderPath + '\\' + f + '" "' + newFileName + '"'+ u.crlf()
        revert += 'ren "' + folderPath + '\\' + newFileName + '" "' + f + '"'+ u.crlf()

    
    #print(res)
    u.to_file("batRename.bat", res)
    u.to_file("revert.bat", revert)

    print('Finish')

