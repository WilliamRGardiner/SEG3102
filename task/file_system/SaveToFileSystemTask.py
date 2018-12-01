import os
from common.utils.FileSystemUtil import FileSystemUtil

'''Saves files to the system'''
class SaveToFileSystemTask():
    def __init__(self, directory, subdirectory, fileName, file, ext):
        self.directory = directory
        self.subdirectory = subdirectory
        self.fileName = fileName
        self.file = file
        self.ext = ext

    def do(self):
        path = FileSystemUtil.getPath(self.directory, self.subdirectory)
        name = FileSystemUtil.getFullFilename(self.fileName, self.ext)
        # Create the directories if they don't exist
        if not os.path.exists(path):
            os.makedirs(path)
        # Save the file
        self.file.save(os.path.join(path, name))

    def undo(self):
        path = FileSystemUtil.getPath(self.directory, self.subdirectory)
        name = FileSystemUtil.getFullFilename(self.fileName, self.ext)
        os.remove(os.path.join(path, name))

    def getErrorMessage(self):
        return "Failed to store image"
