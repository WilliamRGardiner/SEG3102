import os
from shutil import copyfile

from common.utils.FileSystemUtil import FileSystemUtil

'''Moves files to the Trash Directory'''
class RemoveFromFileSystemTask():
    def __init__(self, directory, subdirectory, fileName, ext):
        self.directory = directory
        self.subdirectory = subdirectory
        self.fileName = fileName
        self.ext = ext

    def do(self):
        path = FileSystemUtil.getPath(self.directory, self.subdirectory)
        trash = FileSystemUtil.getTrashPath(self.directory)
        name = FileSystemUtil.getFullFilename(self.fileName, self.ext)
        # Move the file to the trash
        os.rename(os.path.join(path, name), os.path.join(trash, name))

    def undo(self):
        path = FileSystemUtil.getPath(self.directory, self.subdirectory)
        trash = FileSystemUtil.getTrashPath(self.directory)
        name = FileSystemUtil.getFullFilename(self.fileName, self.ext)
        # Move the file from the trash
        os.rename(os.path.join(trash, name), os.path.join(path, name))

    def getErrorMessage(self):
        return "Failed to remove image"
