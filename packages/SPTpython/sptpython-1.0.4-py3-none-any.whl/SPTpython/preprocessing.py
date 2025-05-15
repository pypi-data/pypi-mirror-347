import logging
logging.getLogger(__name__)

import os
import tkinter
import tkinter.filedialog
import pathlib

def extract_files(extension = None):
    """
    Extracts .tif files in selected folder, moving all files up one directory.

    Returns:
        int: number of files that were moved
    """
    
    if extension == None:
        extension = '.tif'
    
    root = tkinter.Tk()
    root.withdraw()
    
    start = tkinter.filedialog.askdirectory()
    root.destroy()
    
    if start == '':
        return 0
    
    start = os.path.abspath(start)
    roots = []
    files = []
    for root, dirs, tempfiles in os.walk(top=start, topdown=False):
        for name in tempfiles:
            # check to make sure you're moving .tif files, so you don't accidentally
            # destroy your computer
            # also check to make sure the file isn't already in the starting directory
            if root.split(start)[1] != '' and extension in name:
                roots.append(root)
                files.append(name)
    logging.info(f"Found {len(roots)} files")
    
    # double check with user
    root = tkinter.Tk()
    root.withdraw()
    result = tkinter.messagebox.askyesno('Proceed?',f'Found {len(roots)} nested {extension} files.\n'
                                            f'Move all {len(roots)} {extension} files up one directory?')

    root.destroy()
    
    if result:
        for name,root in zip(files,roots):
            newRoot = '\\'.join(root.split('\\')[:-1]) # lop off one directory
            logging.info(f"Moving file up one directory:{name}")
            currentPath = os.path.join(root,name)
            newPath = os.path.join(newRoot,name)

            if pathlib.Path(newPath).is_file():
                append = 2
                newPath = newPath[:-4] + str(append) + '.tif'
                while pathlib.Path(newPath).is_file():
                    append += 1
                    newPath = newPath[:-5] + str(append) + '.tif'

            os.rename(currentPath,newPath)
        return len(roots)

def truncateVideo(video, start=None, end=None, save=False):
    raise NotImplementedError    
    # if start == None and end == None:
    #     raise RuntimeError("Must pass in either start or end")
    
    # if end == None:
    #     return video[start:]
    # elif start == None:
    #     return video[:end]
    # else:
    #     return video[start:end]
    # # TODO: figure out how to save


if __name__ == '__main__':
    pass
    # import tkinter.filedialog
    # paths = tkinter.filedialog.askopenfilenames()
    
    # # cutoff = int(input("Input number of frames to truncate up to: "))
    
    # for path in paths:
    #     frames = pims.open(path)
    #     truncateVideo(frames,start=1500, save=True)