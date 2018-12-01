import os

from common.utils.FileSystemUtil import FileSystemUtil

'''Clears the Trash Directory of all files'''
class FlushDirectoryTask():
    def __init__(self, directory, protectedFiles):
        self.directory = directory
        self.protectedFiles = protectedFiles

    def do(self):
        path = FileSystemUtil.getTrashPath(self.directory)
        files = FileSystemUtil.getFiles(path)
        for file in files:
            try:
                rawName = file.split(".")[0]
                if not rawName in self.protectedFiles:
                    os.remove(os.path.join(path, file))
            except:
                print(os.path.join(path, file) + " failed to delete.")

    # No undo, we don't want to repopulate the trash in case of a failure
    def undo(self):
        pass

    def getErrorMessage(self):
        return "Failed to remove image"
