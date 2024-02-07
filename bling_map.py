#simple throwaway script making maps of data 

import xarray as xr
import LSmap 
import numpy as np 
import math

def bling_map(mask, tracer, d, run1, run2=False):
    
    path1 = run1 + '_bling/' + run1 + '_' + tracer + '_map_' + mask + d + '.nc'
    da1 = xr.open_dataarray(path1)

    if run2!=False:
        path2 = run2 + '_bling/' + run2 + '_' + tracer + '_map_' + mask + d + '.nc'
        da2 = xr.open_dataarray(path2)
        da = 100*(da1-da2)/da2    
    else:
        da = da1

    minmax = LSmap.xrLSminmax(da,da.nav_lat_grid_T,da.nav_lon_grid_T)

    if run2!=False:
        CBlabel = 'Difference ($\%$)'
        title = 'Difference in avg. conc. of ' + tracer + ' in the top ' + d + ' m \nthe Labrador Sea, ' + run1 + '-' + run2
        fileName  = 'pics_bling/' + run1 + '-' + run2 + '_' + tracer + '_diff_map_' + mask + d
    else:
        CBlabel = 'Concentration ($mol$, probably)'
        title = 'Avg. conc. of ' + tracer + ' in the top ' + d + ' m, ' + run1 
        fileName  = 'pics_bling/' + run1 + '_' + tracer + '_map_' + mask + d
    
    LSmap.LSmap(da,da.nav_lon_grid_T,da.nav_lat_grid_T,minmax,CBlabel,title,fileName)#,scale='log') (0e10,-4e10)

if __name__ == "__main__":
    #for i in ['EPM151','EPM152','EPM155','EPM156','EPM157','EPM158']:
    #    for j in ['LS2k']:#,'LS2k','LSCR']:
    #        bling_map(mask=j,tracer='vooxy',d='50',run1=i)

    bling_map(mask='LS2k',tracer='vooxy',d='50',run1='EPM155',run2='EPM157')

    #air_map(mask='LS',run1='EPM151',run2='EPM155')
    #air_map(mask='LS',run1='EPM151',run2='EPM157')
    #air_map(mask='LS',run1='EPM155',run2='EPM157')
    #air_map(mask='LS',run1='EPM152',run2='EPM156')
    #air_map(mask='LS',run1='EPM152',run2='EPM158')
    #air_map(mask='LS',run1='EPM156',run2='EPM158')
    

    #for i in ['EPM151','EPM152','EPM155','EPM156','EPM157','EPM158']:
    #    mle_map(mask='LS', run1=i)
    #mld_map(variable='avg_MLD', mask='LS', run1='EPM158')
    #mld_map(variable='max_MLD', mask='LS', run1='EPM158')
