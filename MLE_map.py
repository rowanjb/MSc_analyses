#simple throwaway script making maps of data 

import xarray as xr
import LSmap 
import numpy as np 
import math
import os

def mle_map(mask, run1, run2=False):
    
    #EPM158_MLE_Q_map_MASKCHOICE.NC
    #EPM151_MLE_Q_map_LS_19.nc
    #Q.map.to_netcdf(run + '_MLE/' + run + '_MLE_Q_map_' + mask + '.nc')

    path1 = run1 + '_MLE/' + run1 + '_MLE_Q_map_' + mask + '.nc'
    da1 = xr.open_dataarray(path1)

    if run2!=False:
        path2 = run2 + '_MLE/' + run2 + '_MLE_Q_map_' + mask + '.nc'
        da2 = xr.open_dataarray(path2)
        da = da1-da2    
    else:
        da = da1

    minmax = LSmap.xrLSminmax(da,da.nav_lat_grid_T,da.nav_lon_grid_T)

    CBlabel = 'Heat flux ($J/S$?)'

    if run2!=False:
        title = 'Difference of the ... in \nthe Labrador Sea, ' + run1 + '-' + run2
        fileName  = 'pics_MLE/' + run1 + '-' + run2 + '_' + variable + '_map_' + mask
    else:
        title = 'Average heat flux through the bottom of the mixed layer, ' + run1 
        fileName  = 'pics_MLE/' + run1 + '_MLE_Q_map'
    
    LSmap.LSmap(da,da.nav_lon_grid_T,da.nav_lat_grid_T,minmax,CBlabel,title,fileName)#,scale='log')

def mle_movie_frames(mask, run1):
    folder = run1 + '_MLE/movie_NCs/'
    movie_files = sorted([folder + file for file in os.listdir(folder)])
    frames_folder = run1 + '_MLE/movie_frames/'
    if not os.path.exists(frames_folder):
            os.makedirs(frames_folder)
    with open('flistname_time_counter.txt') as f: lines = f.readlines()
    flistname_dates = [line.strip() for line in lines]  
    for i in movie_files:
        date = i[-13:-3]
        if date in flistname_dates:
            print(date)
            da = xr.open_dataarray(i)
            print('file opened')
            #minmax = LSmap.xrLSminmax(da,da.nav_lat_grid_T,da.nav_lon_grid_T)
            CBlabel = 'Heat flux ($W$)'
            title = 'Heat flux across the mixed layer\n ' + run1 + ' - ' + date
            fileName  = run1 + '_MLE/movie_frames/' + run1 + '_MLE_Q_map_' + date
            LSmap.LSmap(da,da.nav_lon_grid_T,da.nav_lat_grid_T,(0,10000),CBlabel,title,fileName,scale='log')

def mle_diff_frames_test(mask, run1, run2):
    folder1 = run1 + '_MLE/movie_NCs/'
    movie_files1 = sorted([folder1 + file for file in os.listdir(folder1)])
    folder2 = run2 + '_MLE/movie_NCs/'
    movie_files2 = sorted([folder2 + file for file in os.listdir(folder2)])
    frames_folder = 'test_movie_frames/'
    with open('flistname_time_counter.txt') as f: lines = f.readlines()
    flistname_dates = [line.strip() for line in lines]
    for i in movie_files1:
        date = i[-13:-3]
        if date in flistname_dates: 
            print(date)
            da1 = xr.open_dataarray(i)
            NC2 = [j for j in movie_files2 if date in j] #there should only be one hit
            print(NC2[0])
            da2 = xr.open_dataarray(NC2[0])
            print('files opened')
            #minmax = LSmap.xrLSminmax(da,da.nav_lat_grid_T,da.nav_lon_grid_T)
            CBlabel = 'Heat flux diff. ($W$)'
            title = 'Heat flux diff through the bottom of the mixed layer\n ' + run1 + '-' + run2 + ' - ' + date
            fileName  = frames_folder + 'test_' + date
            LSmap.LSmap(da1-da2,da1.nav_lon_grid_T,da1.nav_lat_grid_T,(-1000,1000),CBlabel,title,fileName,scale='log')

if __name__ == "__main__":
    mle_movie_frames('LS','EPM151')
    mle_movie_frames('LS','EPM152')
    mle_movie_frames('LS','EPM155')
    mle_movie_frames('LS','EPM156')
    mle_movie_frames('LS','EPM157')
    mle_movie_frames('LS','EPM158')

    #mle_diff_frames_test('LS','EPM155','EPM157')

    #for i in range(30):
    #    print( 'EPM151_MLE/movie_NCs/EPM151_MLE_Q_map_LS_' + str(i) + '.nc' )
    #for i in ['EPM151','EPM152','EPM155','EPM156','EPM157','EPM158']:
        #mle_map(mask='LS', run1=i)
    #mld_map(variable='avg_MLD', mask='LS', run1='EPM158')
    #mld_map(variable='max_MLD', mask='LS', run1='EPM158')
