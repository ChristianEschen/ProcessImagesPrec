from options import Options
import os
from Tarloader import Tarloader

def main():
    opt = Options().parse()
    TL = Tarloader(opt)
    TL.MakeOutDestFolder()
    TL.MakeTarfile()
    

if __name__ == "__main__":
    main()

    