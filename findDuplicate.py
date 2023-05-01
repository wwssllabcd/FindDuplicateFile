
import sys
from os import listdir
from os.path import isfile, join, getmtime

sys.path.append(r'./../')
from EricCorePy.Utility.EricUtility import *


class FileObj:
    def __init__(self):
        self.name = ""
        self.size = 0
        self.isFile = True
        self.mtime = 0

def get_fileObj_colls(folderPath, fileColls):
    u = EricUtility()
    files = listdir(folderPath)

    for f in files:
        fullpath = join(folderPath, f)
        fo = FileObj()
        fo.name = fullpath
        fo.isFile = isfile(fullpath)
        fo.size = u.get_file_size(fullpath)
        fo.mtime = getmtime(fullpath)
        fileColls.append(fo)
    
    return fileColls

#回傳 duplicate list
def get_duplicate_file_and_data_list(fileDirGroupDirBySize):
    compareSize = 512*1024
    result = []
    u = EricUtility()

    #相同的 file size 當作 group
    for fileSize in fileDirGroupDirBySize:
        sameFileSizeGroup = fileDirGroupDirBySize[fileSize]
        # 只處理兩個以上，且相同檔案大小的group
        if len(sameFileSizeGroup) < 2:
            continue

        #把相同檔案大小的檔案 group 中的每個檔案的資料讀出
        sameSizeList = []
        for fo in sameFileSizeGroup:
            sameSizeList.append([fo, u.get_file_data_binary(fo, compareSize)])
        result.append(sameSizeList)
    return result

def get_duplicate_file_by_compare_file_data(fileDirGroupDirBySize):
    dupFileListolls = get_duplicate_file_and_data_list(fileDirGroupDirBySize)
    dupFileNameList = []
    #相同的 file size 當作 group
    for dupFileList in dupFileListolls:
        # 取出要 compare 的對象，使用兩個迴圈對每個檔案做比較
        # 注意! 使用窮舉的方式，所有的檔案都會被標成記號，需要自己比較要留哪一個
        # 刪完後可使用 windows rename 功能全部rename
        checkDone = [False] * len(dupFileList)
        for i in range(len(dupFileList)):
            for j in range(i+1, len(dupFileList)):
                if j>= len(dupFileList):
                    continue
                
                if checkDone[i] == True:
                    continue

                mainFile = dupFileList[i]
                compareFile = dupFileList[j]

                if mainFile[1] == compareFile[1]:
                    dupFileNameList.append(compareFile[0])
                    checkDone[j] = True
    return dupFileNameList

def get_file_name_by_full_path(fullPath):
    idx = fullPath.rfind("\\")
    if idx == -1:
        idx = fullPath.rfind("/")
    res = fullPath[idx+1:]
    return res

def rename_file(fileColls):
    u = EricUtility()
    res = "chcp 65001" + u.crlf()
    for file in fileColls:
        fileName = get_file_name_by_full_path(file)
        #加上 zzz 可保持排序在最後
        res += 'ren "' + file + '" "ZZZZ_dup_' + fileName + '"' + u.crlf()
        #res += 'move "' + file + '" E:\\Download\\tmp\\dup' + u.crlf()

    return res


def main():
    
    
    paths = []
    # for i in sys.argv:
    #     if u.is_dir(i):
    #         paths.append(i)

    # if len(paths)==0:
    #     print("No any path")
    #     exit()

    #for debug
    paths.append("E://test")
 
   
    
    print(paths)

    fileColls = []
    for path in paths:
        fdPath = path + "//"
        fileColls = get_fileObj_colls(fdPath, fileColls)
    
    onlyFiles = []
    for fileObj in fileColls:
        if fileObj.isFile == True:
            onlyFiles.append(fileObj)

    u = EricUtility()
    fileDirGroupDirBySize = u.get_file_list_by_size(onlyFiles)
    
    dupFileList = get_duplicate_file_by_compare_file_data(fileDirGroupDirBySize)
    print(dupFileList)
    print("make bat")
    #print(dupFileList)
    dupFileList.sort()
    res = rename_file(dupFileList)
    u.to_file("renameDupFiles.bat", res)

    print(res)
    print('Finish')

# 會留一個檔案，其餘的會被標成 zzz_dup, 可以檢查一下是否會留一個重複的下來

#------------------------
# window command line 切換到 utf-8
# chcp 65001
#-----------------
if __name__ == '__main__':
    main()