
import sys
from os import listdir
from os.path import isfile, join

sys.path.append(r'D:/GitHub/Python')
from EricCorePy.Utility.EricUtility import EricUtility


class FileObj:
    def __init__(self):
        self.name = ""
        self.size = 0
        self.isFile = True

def get_fileObj_colls(folderPath, fileColls):
    u = EricUtility()
    files = listdir(folderPath)

    for f in files:
        fullpath = join(folderPath, f)
        fo = FileObj()
        fo.name = fullpath
        fo.isFile = isfile(fullpath)
        fo.size = u.get_file_size(fullpath)
        fileColls.append(fo)
    
    return fileColls

def get_duplicate_file_by_compare_file_data(fileDirGroupDirBySize):
    u = EricUtility()
    dupFileList = []
    compareSize = 512*1024
    for fileSize in fileDirGroupDirBySize:
        sameFileSizeGroup = fileDirGroupDirBySize[fileSize]
        # 只處理兩個以上，且相同檔案大小的group
        if len(sameFileSizeGroup) < 2:
            continue

        #把相同檔案大小的檔案 group 中的每個檔案的資料讀出
        fileNameAndDatas = []
        for fileName in sameFileSizeGroup:
            fileNameAndDatas.append([fileName, u.get_file_data_binary(fileName, compareSize)])
        
        # 取出要 compare 的對象，使用兩個迴圈對每個檔案做比較
        # 注意! 使用窮舉的方式，所有的檔案都會被標成記號，需要自己比較要留哪一個
        for compare in fileNameAndDatas: # compare 的格式為 [fileName, data]
            for file in fileNameAndDatas:
                # 如果檔名相同，就跳過
                if compare[0] == file[0]:
                    continue

                print(compare[0])
                # 檔名不同，且資料相同，則判定為 duplicate，最後所有重複的檔案都會被標成重複
                if compare[1] == file[1]:
                    dupFileList.append(compare[0])
                    break
    return dupFileList

def get_file_name_by_full_path(fullPath):
    idx = fullPath.rfind("\\")
    if idx == -1:
        idx = fullPath.rfind("/")
    res = fullPath[idx+1:]
    return res

def rename_file(fileColls):
    res = "chcp 65001" + u.crlf()
    for file in fileColls:
        fileName = get_file_name_by_full_path(file)
        #加上 zzz 可保持排序在最後
        res += 'ren "' + file + '" "ZZZZ_dup_' + fileName + '"' + u.crlf()
        #res += 'move "' + file + '" E:\\Download\\tmp\\dup' + u.crlf()

    return res

#------------------------
# window command line 切換到 utf-8
# chcp 65001
#-----------------
if __name__ == '__main__':
    u = EricUtility()
    paths = []
    for i in sys.argv:
        if u.is_dir(i):
            paths.append(i)

    if len(paths)==0:
        print("No any path")
        exit()

    #for debug
    #paths.append("G:\CuteDL\mask_reserve")
    print(paths)

    fileColls = []
    for path in paths:
        fdPath = path + r'\\'
        fileColls = get_fileObj_colls(fdPath, fileColls)
    
    fileDirGroupDirBySize = u.group_file_by_size(fileColls)

    dupFileList = get_duplicate_file_by_compare_file_data(fileDirGroupDirBySize)
    print("make bat")
    dupFileList.sort()
    res = rename_file(dupFileList)
    u.to_file("renameFiles.bat", res)

    print(res)
    print('Finish')

# 有重複的會被抓出來(連同本身)