import os

'''Utility for managing uploaded files'''
class FileSystemUtil():

    '''Drirectory name for files to be deleted'''
    TRASH = "trash"

    '''Gets the absolute path to a directory'''
    def getPath(directory, subdirectory):
        # Get current directory path
        base = os.path.dirname(__file__)
        # Get path to App Root
        array = base.split("\\")
        indexOfAppRoot = array.index("SEG3102App")
        array = array[:indexOfAppRoot+1]
        base = "\\".join(array)
        # Return path to correct subdirectory and filename
        return os.path.join(base, directory, subdirectory)

    '''Gets the absolute path to the trash directory'''
    def getTrashPath(directory):
        # Get current directory path
        base = os.path.dirname(__file__)
        # Get path to App Root
        array = base.split("\\")
        indexOfAppRoot = array.index("SEG3102App")
        array = array[:indexOfAppRoot+1]
        base = "\\".join(array)
        # Return path to correct subdirectory and filename
        return os.path.join(base, directory, FileSystemUtil.TRASH)

    '''Returns the file name with the extension'''
    def getFullFilename(filename, ext):
        return filename + "." + ext

    '''Gets the name of ever file in a directory'''
    def getFiles(path):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            files.extend(filenames)
            break
        return files
