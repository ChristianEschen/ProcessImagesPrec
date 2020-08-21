import argparse
import os

class Options():
    """Options class
    Returns:
        [argparse]: argparse containing arguments
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        # Base
        self.parser.add_argument('--DataRoot', default='C:\\Users\\qvd170\\Desktop\\Pancreas-CT', help='Path to dataroot')  
        self.parser.add_argument('--TarDirName', default='C:\\Users\\qvd170\\ImageProject\\imageproject\data\\raw', help='name of tardir') 
        self.parser.add_argument('--OutDirName', default='C:\\Users\\qvd170\\ImageProject\\imageproject\\reports\\figures', help='name of output dir with csv and plots')   
        self.parser.add_argument('--NumberOfSamples', type=int, default=2, help='Numper of samples to show (images)')
        self.parser.add_argument('--CsvOutDir', default="C:\\Users\\qvd170\\ImageProject\\imageproject\\data\\interim\\data.csv", help='Output path name for csv file')


    def parse(self):
        """ Parse Arguments.
        """
        self.opt = self.parser.parse_args()
        return self.opt