#identifies and removes gridT, gridU, and gridV files that give "all nan slice" errors
#Rowan Brown
#May 8, 2023

#running all 6 simulations at 23hrs, 10gb

import xarray as xr
import os

def filepaths(run): 

    #directory of nemo output files on graham
    nemo_output_dir = '/home/rowan/projects/rrg-pmyers-ad/pmyers/ANHA4/ANHA4-' + run + '-S/'

    #list of filepaths
    filepaths_gridT = sorted([nemo_output_dir + file for file in os.listdir(nemo_output_dir) if file.endswith('gridT.nc')])#[::300]
    ##filepaths_gridU = sorted([nemo_output_dir + file for file in os.listdir(nemo_output_dir) if file.endswith('gridU.nc')])#[::300]
    ##filepaths_gridV = sorted([nemo_output_dir + file for file in os.listdir(nemo_output_dir) if file.endswith('gridV.nc')])#[::300]
    ##filepaths_gridB = sorted([nemo_output_dir + file for file in os.listdir(nemo_output_dir) if file.endswith('gridB.nc')])#[::300]
    ##filepaths_gridW = sorted([nemo_output_dir + file for file in os.listdir(nemo_output_dir) if file.endswith('gridW.nc')])#[::300]
    ##filepaths_icebergs = sorted([nemo_output_dir + file for file in os.listdir(nemo_output_dir) if file.endswith('icebergs.nc')])#[::300]
    ##filepaths_icemod = sorted([nemo_output_dir + file for file in os.listdir(nemo_output_dir) if file.endswith('icemod.nc')])#[::300]

    #testing if gridT files are read-able
    bad_files = [] #initializing list of bad filepaths
    for filepath in filepaths_gridT:
        try:
            DS = xr.open_dataset(filepath)
        except:
            bad_files.append(filepath[:-8]) #saving any bad filepaths
            print('gridT: ' + filepath)

    ###testing if gridU files are read-able
    ##for filepath in filepaths_gridU:
    ##    try:
    ##        DS = xr.open_dataset(filepath)
    ##    except:
    ##        bad_files.append(filepath[:-8]) #saving any bad filepaths
    ##        print('gridU: ' + filepath)
    ##
    ###testing if gridV files are read-able
    ##for filepath in filepaths_gridV:
    ##    try:
    ##        DS = xr.open_dataset(filepath)
    ##    except:
    ##        bad_files.append(filepath[:-8]) #saving any bad filepaths
    ##        print('gridV: ' + filepath)
    ##
    ###testing if icemod files are read-able
    ##for filepath in filepaths_icemod:
    ##    try:
    ##        DS = xr.open_dataset(filepath)
    ##    except:
    ##        bad_files.append(filepath[:-9]) #saving any bad filepaths
    ##        print('icemod: ' + filepath) 

    #removing duplicates from the list
    bad_files = list( dict.fromkeys(bad_files) )

    #removing bad filepaths
    for bad_file in bad_files:
        print(bad_file + ' is a bad file')
        filepaths_gridT.remove(bad_file + 'gridT.nc')
        ##filepaths_gridU.remove(bad_file + 'gridU.nc')
        ##filepaths_gridV.remove(bad_file + 'gridV.nc')
        ##filepaths_gridB.remove(bad_file + 'gridB.nc')
        ##filepaths_gridW.remove(bad_file + 'gridW.nc')
        ##filepaths_icebergs.remove(bad_file + 'icebergs.nc')
        ##filepaths_icemod.remove(bad_file + 'icemod.nc')

    #creating directory if doesn't already exist
    dir = run + '_filepaths/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    #saving the filepaths as txt files
    with open(dir + run + '_gridT_filepaths_Jan2024.txt', 'w') as output:
        for i in filepaths_gridT:
            output.write(str(i) + '\n')
    ##with open(dir + run + '_gridU_filepaths.txt', 'w') as output:
    ##    for i in filepaths_gridU:
    ##        output.write(str(i) + '\n')
    ##with open(dir + run + '_gridV_filepaths.txt', 'w') as output:
    ##    for i in filepaths_gridV:
    ##        output.write(str(i) + '\n')
    ##with open(dir + run + '_gridB_filepaths.txt', 'w') as output:
    ##    for i in filepaths_gridB:
    ##        output.write(str(i) + '\n')
    ##with open(dir + run + '_gridW_filepaths.txt', 'w') as output:
    ##    for i in filepaths_gridW:
    ##        output.write(str(i) + '\n')
    ##with open(dir + run + '_icebergs_filepaths.txt', 'w') as output:
    ##    for i in filepaths_icebergs:
    ##        output.write(str(i) + '\n')
    ##with open(dir + run + '_icemod_filepaths.txt', 'w') as output:
    ##    for i in filepaths_icemod:
    ##        output.write(str(i) + '\n')

if __name__ == '__main__':
    for i in ['EPM151','EPM152','EPM155','EPM156','EPM157','EPM158']:
        filepaths(run=i)
