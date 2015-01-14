'''
Created on Jul 18, 2013

@author: qurban.ali
'''
import site
site.addsitedir(r'R:\Python_Scripts')
import os
import os.path as osp
import math
from PyQt4.QtCore import QRegExp, QString


def normpath(path):
    return osp.normpath(path)

def pathExists(path):
    return osp.exists(path)

def dirname(path):
    return osp.dirname(path)

def isfile(path):
    return osp.isfile(path)

def join(path1, path2):
    return osp.join(path1, path2)

def files(path):
    dirs = []
    for di in os.listdir(path):
        if osp.isfile(osp.join(path, di)):
            dirs.append(di)
    return sorted(dirs)

def frameNumber(fileName):
    '''
    returns the frame number from the file name
    '''
    regExp = QRegExp('(\\d+)(\.)')
    if regExp.indexIn(fileName) > -1:
        return str(list(regExp.capturedTexts())[1])

def chopStr(st, n):
    '''
    removes the n characters from the end of the string
    '''
    st = QString(st)
    st.chop(n)
    return str(st)

def size(path):
    '''
    returns the size of the file in bytes
    '''
    return osp.getsize(path)

def frameNumToName(frames, name):
    '''
    converts the frame numbers to file names
    '''
    names = []
    name = QString(name)
    for frame in frames:
        names.append(str(name.replace(QRegExp('(\\d+)'), frame)))
    return names

def standardDeviation(population, lower = False, upper = False):
    '''
    returns the standard deviation for file sizes
    '''
    n = len(population)
    s = sum(population)
    mean = s/n
    # calculate the standard deviation
    variance = (sum([math.pow(x - mean, 2) for x in population]))/n
    stdDev = math.sqrt(variance)
    if upper and lower: return {'upper': mean + stdDev, 'lower': mean - stdDev}
    if lower: return mean - stdDev
    if upper: return mean + stdDev
    return stdDev
    