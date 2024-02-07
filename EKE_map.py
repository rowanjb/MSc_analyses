#simple throwaway script making maps of data 
  
import xarray as xr
import LSmap
import numpy as np
import math
import os

def eke_map(mask, run1, run2=False):
    
    for depth in ['50','200','1000','2000']:

        path1 = run1 + '_EKE/' + run1 + '_EKE_map_' + mask + depth + '.nc'
        da1 = xr.open_dataarray(path1)
        da1 = da1.where(da1 > 0)

        if run2!=False:
            path2 = run2 + '_EKE/' + run2 + '_EKE_map_' + mask + depth + '.nc'
            da2 = xr.open_dataarray(path2)
            da2 = da2.where(da2 > 0)
            da = da1-da2
        else:
            da = da1

        minmax = LSmap.xrLSminmax(da,da.nav_lat_grid_T,da.nav_lon_grid_T)

        if run2!=False:
            CBlabel = '$\Delta$EKE ($J$)'
        else:
            CBlabel = 'EKE ($J$)'

        if mask == 'LS2k': mask_description = ' interior'
        elif mask == 'LS': mask_description = ''
        elif mask == 'LSCR': mask_description = ' convection region'

        if run2!=False:
            title = 'Difference in eddy kinetic energy in the top ' + depth + 'm of \nthe Labrador Sea' + mask_description + ', ' + run1 + '-' + run2
            fileName  = 'pics_EKE/' + run1 + '-' + run2 + '_EKE_map_' + mask + depth
        else:
            title = 'Eddy kinetic energy in the top ' + depth + 'm of \nthe Labrador Sea' + mask_description + ', ' + run1
            fileName  = 'pics_EKE/' + run1 + '_EKE_map_' + mask + depth

        LSmap.LSmap(da,da.nav_lon_grid_T,da.nav_lat_grid_T,minmax,CBlabel,title,fileName)#,scale='log')

def eke_movie_frames(mask, run, depth): #ADD FUNCTIONALITY FOR DEALING WITH DEPTH

    run_characteristics={
        'EPM151': 'CGRF with tides',
        'EPM152': 'ERA-I with tides',
        'EPM155': 'CGRF with tides + SMLEs',
        'EPM156': 'ERA-I with tides + SMLEs',
        'EPM157': 'CGRF control',
        'EPM158': 'ERA-I control'
    }

    directory = run + '_EKE/movie_NCs/' # + mask + str(depth) + '*' 
    #filepaths_gridT = sorted([nemo_output_dir + file for file in os.listdir(nemo_output_dir) if file.endswith('gridT.nc')])#[::300]
    movie_files = sorted([directory + ncfile for ncfile in os.listdir(directory) if mask+str(depth) in ncfile])
    for i in movie_files:
        date = i[-13:-3]
        da = xr.open_dataarray(i)
        #minmax = LSmap.xrLSminmax(da,da.nav_lat_grid_T,da.nav_lon_grid_T)
        CBlabel = '$J$ $m^{-2}$'
        title = 'Eddy Kinetic Energy in top ' + str(depth) + ' m\n' + run_characteristics[run] + ' - ' + date #note: could include mask descriptor, but unecessary likely because I'll only plot LS
        folder = run + '_EKE/movie_frames'
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = folder + '/' + run + '_EKE_map_' + mask + str(depth) + '_' + date
        LSmap.LSmap(da,da.nav_lon_grid_T,da.nav_lat_grid_T,(0,10000),CBlabel,title,filename,scale='log')
        print(date + ' mapped')

if __name__ == "__main__":
    for run in ['EPM158']:#['EPM151','EPM152','EPM155','EPM156','EPM157','EPM158']:
        eke_movie_frames('LS',run,1000)
    quit()
    eke_map(mask='LS', run1='EPM151', run2='EPM155')
    eke_map(mask='LS', run1='EPM151', run2='EPM157')
    eke_map(mask='LS', run1='EPM155', run2='EPM157')
    eke_map(mask='LS', run1='EPM152', run2='EPM156')
    eke_map(mask='LS', run1='EPM152', run2='EPM158')
    eke_map(mask='LS', run1='EPM156', run2='EPM158')

