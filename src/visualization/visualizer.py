import os
import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk
import pandas as pd
from Tarloader import Tarloader
import pydicom
import dicom_numpy
from PIL import Image

class visualizer(Tarloader):
    def showHist(self, df, histsFolder, filter = ''):
        for c in self.meta_cols:
            ax = None
            fig = plt.figure()
            ax = df[c].hist()
            fig = ax.get_figure()
            if filter != '':
                self.mkFolder(os.path.join(self.opt.OutDirName, histsFolder, filter))
                fig.savefig(os.path.join(self.opt.OutDirName, histsFolder, filter, c + '.pdf'))
            else:
                fig.savefig(os.path.join(self.opt.OutDirName, histsFolder, c + '.pdf'))
        return
        
    def build3Darray(self, files):
        # skip files with no SliceLocation (eg scout views)
        slices = []
        skipcount = 0
        orderring_type = None
        for f in files:
            if hasattr(f, 'SliceLocation'):
                slices.append(f)
                orderring_type == 'SL'
            else:
                skipcount = skipcount + 1

        if len(slices) == 0: # Slice location not found, extract the right info:
            orderring_type == 'IN'
            for f in files:
                if hasattr(f, 'InstanceNumber'):
                    slices.append(f)
                else:
                    raise CustomException('Not implemneted InstanceNumber not provided')

        # ensure they are in the correct order
        if orderring_type == 'SL':
            slices = sorted(slices, key=lambda s: s.SliceLocation)
        elif orderring_type == 'IN':
            slices = sorted(slices, key=lambda s: s.InstanceNumber)

        # create 3D array
        img_shape = list(slices[0].pixel_array.shape)
        img_shape.append(len(slices))
        img3d = np.zeros(img_shape, dtype=np.int16)

        # fill 3D array with the images from the files
        for i, s in enumerate(slices):
            bytes = s.PixelData
            img2d = np.frombuffer(bytes, dtype=np.int16).reshape((s.Rows,s.Columns))
            img3d[:, :, i] = img2d
        
        return img3d
    def show2dsimple(self, img3d, fileName):

        fig = plt.figure()
        plt.imshow(img3d[img3d.shape[0]//2, :, :].T, cmap='gray')
        fig.savefig(os.path.join(fileName, 'corornal'+'.png'))

        fig = plt.figure()
        plt.imshow(img3d[:, :, img3d.shape[2]//2], cmap='gray')
        fig.savefig(os.path.join(fileName, 'transversal'+'.png'))

        fig = plt.figure()
        plt.imshow(img3d[:, img3d.shape[1]//2, :], cmap='gray')
        fig.savefig(os.path.join(fileName, 'sagital'+'.png'))


    def show2dfull(self, img3d, fileName):

        cor_path = os.path.join(self.opt.OutDirName, self.imagesFolder, os.path.basename(fileName), 'coronal')
        sag_path = os.path.join(self.opt.OutDirName, self.imagesFolder, os.path.basename(fileName), 'sagital')
        trans_path = os.path.join(self.opt.OutDirName, self.imagesFolder, os.path.basename(fileName), 'transversal')
        
        self.mkFolder(cor_path)
        self.mkFolder(sag_path)
        self.mkFolder(trans_path)
        
        for i in range(0,img3d.shape[0]):
            fig = plt.figure()
            plt.imshow(img3d[i, :, :].T, cmap='gray')
            fig.savefig(os.path.join(cor_path, 'corornal'+str(i)+'.png'))

        for i in range(0,img3d.shape[2]):
            fig = plt.figure()
            plt.imshow(img3d[:, :, i], cmap='gray')
            fig.savefig(os.path.join(trans_path, 'transversal'+str(i)+'.png'))

        for i in range(0,img3d.shape[1]):
            fig = plt.figure()
            plt.imshow(img3d[:, i, :], cmap='gray')
            fig.savefig(os.path.join(sag_path, 'sagital'+str(i)+'.png'))

    def showImg(self, df, imagesFolder, numberSamples = 10):
        
        for bodyPart in pd.unique(df['BodyPartExamined']):
            self.mkFolder(os.path.join(self.opt.OutDirName, imagesFolder, bodyPart))
            for mod in pd.unique(df['Modality']):
                self.mkFolder(os.path.join(self.opt.OutDirName, imagesFolder, bodyPart, mod))
                for i in range(0,numberSamples):
                    filt = df[df['BodyPartExamined']==bodyPart]
                    filt = filt[filt['Modality']==mod]

                    self.fileName = filt.DirName.iloc[i]
                    self.patientID = filt.PatientID.iloc[i]
                    dataDirectory = os.path.join(self.opt.TarDirName, self.fileName)
        
                    tar = self.ReadTarFile(dataDirectory)
                    
                    files = self.extractDcmList(tar, dataDirectory)

                    img3d = self.build3Darray(files)
                    self.imagesFolder = imagesFolder
                    outPath = os.path.join(self.opt.OutDirName, imagesFolder, bodyPart, mod, os.path.basename(self.patientID))
                    self.mkFolder(outPath)
                    self.show2dsimple(img3d, outPath)
