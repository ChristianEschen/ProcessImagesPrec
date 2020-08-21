import tarfile
import os
import shutil
import pydicom
import pandas as pd
from pydicom.filebase import DicomBytesIO
import pathlib
import re


def GetTailFolder(parent, path):
        path = os.path.join(
                    parent, os.path.basename(os.path.normpath(path)))
        return path

class Tarloader():

    def __init__(self, opt):
        self.opt = opt
        self.MakeTarDestFolder()
        self.MakeOutDestFolder()
        self.files = self.GetFiles()
        self.tarfiles = self.GetTarFiles()
        self.meta_cols = meta_cols = ['DirName','BodyPartExamined',
             'Modality','PatientID', 'SOPInstanceUID']
        self.col_dict = {col: [] for col in meta_cols}

    def extractDcmList(self, tar, tarFold):
        tarfolders = self.extractTarFolders(tar)
        idx = [i for i, s in enumerate(tarfolders) if self.patientID in s]
        dicomFiles = []
        for i in range(0, len(tarfolders[idx[0]])):
            f = tar.extractfile(tar.getmember(tarfolders[idx[0]][i]))
            if os.path.splitext(tar.getmember(tarfolders[idx[0]][i]).name)[1] =='.dcm':
                content = f.read()
                raw = DicomBytesIO(content)
                ds = pydicom.dcmread(raw)
                dicomFiles.append(ds)
        return dicomFiles
        
    def getUniqueSubFolds(self, tar):
        return list(set([pathlib.Path(i).parts[0] for i in tar.getnames()]))

    def extractTarFolders(self, tar):
        archives = []
        liste = self.getUniqueSubFolds(tar)
        for i in liste:
            archives.append([x for x in tar.getnames() if re.match(i,x)])
        return archives

    def extractMeta(self, tarFold, tar):
        for i in range(0, len(tarFold)):
            f = tar.extractfile(tar.getmember(tarFold[i]))
            if os.path.splitext(tar.getmember(tarFold[i]).name)[1] =='.dcm':
                content = f.read()
                raw = DicomBytesIO(content)
                ds = pydicom.dcmread(raw)
                break
        return ds

    def ReadTarFile(self, tarpath):
        tar = tarfile.open(tarpath)
        return tar

    def ReadTar(self):
        for tarpath in self.tarfiles:
            tar = self.ReadTarFile(tarpath)
            tarFolders = self.extractTarFolders(tar)
            for tarFold in tarFolders:   
                ds = self.extractMeta(tarFold, tar)
                setattr(ds,'DirName', os.path.basename(tarpath))
                for col in self.meta_cols: 
                    self.col_dict[col].append(str(getattr(ds, col)))
        df = pd.DataFrame.from_dict(self.col_dict)
        df.to_csv(self.opt.CsvOutDir)

    def GetFiles(self):
        self.files =  [os.path.join(self.opt.DataRoot, s) for s in os.listdir(self.opt.DataRoot)]
        return self.files

    def GetTarFiles(self):
        self.tarfiles =  [os.path.join(self.opt.TarDirName, s) for s in os.listdir(self.opt.TarDirName) if s.endswith('.tar')]
        return self.tarfiles

    def MakeTarDestFolder(self):
        if not os.path.exists(self.opt.TarDirName):
            os.makedirs(self.opt.TarDirName)

    def mkFolder(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def MakeOutDestFolder(self):
        self.mkFolder(self.opt.OutDirName)

    def MakeTarfile(self):
        for path in self.files:
            shutil.make_archive(
                GetTailFolder(self.opt.TarDirName, path), 'tar', GetTailFolder(self.opt.DataRoot, path))

