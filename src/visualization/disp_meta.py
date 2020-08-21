from options import Options
import pandas as pd
from  visualizer import visualizer
import os
from Tarloader import Tarloader



def main():
    opt = Options().parse()
    TL = Tarloader(opt)
    TL.ReadTar()

    df = pd.read_csv(opt.CsvOutDir)



    vis = visualizer(opt)
    histsFolder = 'hists'
    imagesFolder = 'images'

    vis.mkFolder(os.path.join(opt.OutDirName, histsFolder))
    vis.mkFolder(os.path.join(opt.OutDirName, imagesFolder))
    vis.showImg(df, imagesFolder, numberSamples = opt.NumberOfSamples)
    
    vis.showHist(df, histsFolder)
    for i in df['BodyPartExamined'].unique():
        vis.showHist(df[df['BodyPartExamined']==i], histsFolder, i)
    
    
if __name__ == "__main__":
    main()

    
