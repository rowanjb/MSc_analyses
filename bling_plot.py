#simple throwaway script making plots of data 

import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import xarray as xr
import LSmap 
import numpy as np 
from cycler import cycler

legend_dict = {
    'EPM151': 'C tides',
    'EPM152': 'E tides',
    'EPM155': 'C tides + SMLEs',
    'EPM156': 'E tides + SMLEs',
    'EPM157': 'C control',
    'EPM158': 'E control'
}

c1, c2, c3, c4, c5, c6 = plt.cm.viridis([0, 0.5, 0.8, 0, 0.5, 0.8])
custom_cycler = (cycler(color=[c1, c2, c3, c4, c5, c6]) +
                 cycler(ls=['-', '-', '-', '--', '--', '--']) +
                 cycler(lw=[1.2, 1.2, 1.2, 1.2, 1.2, 1.2]))

def bling_plot(mask, tracer, d, time_slice=False):

    fig, ax = plt.subplots()
    #plt.grid(axis = 'x')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))#'%m/%d/%Y'))
    interval = 1
    #if time_slice: interval=1
    ax.xaxis.set_major_locator(mdates.YearLocator(interval))#(interval=365)) #with YearLocator(1) the ticks are at the start of the year

    #plt.style.use('tableau-colorblind10')
    #DSICE['heat_flux_timeplot'] = DSICE.heat_flux_in_each_cell.sum(dim=['x','y'])
    #DSICE.heat_flux_timeplot.to_netcdf(run + '_air/' + run + '_air_timeplot_' + mask_choice + '.nc')

    lines = []
    for run in ['EPM157','EPM151','EPM155','EPM158','EPM152','EPM156']:
        path = run + '_bling/' + run + '_' + tracer + '_timeplot_' + mask + d + '.nc' 
        data2plot = xr.open_dataarray(path)
        print(data2plot)
        quit()
        #data2plot = data2plot.where(data2plot > 0, drop=True)
        if time_slice: data2plot = data2plot.sel(time_counter=slice('2010-01-01', '2014-01-01'))
        if not time_slice: data2plot = data2plot.sel(time_counter=slice('2010-01-01','2020-01-01')) # data2plot.time_counter[-1]))
        dates = data2plot.indexes['time_counter'].to_datetimeindex(unsafe=True) #Beware: warning turned off!!
        dates = [date.date() for date in dates]
        print(dates)
        quit()
        plt.rc('axes', prop_cycle=custom_cycler)
        lines += ax.plot(dates, data2plot, label=legend_dict[run])

    labels = [l.get_label()[2:] for l in lines]
    linestyles = [l.get_linestyle() for l in lines]
    leg1 = plt.legend(lines[:3],labels[:3], loc='upper left', bbox_to_anchor=(1, 0.48), title='CGRF')
    plt.legend(lines[3:], labels[3:], loc='lower left', bbox_to_anchor=(1, 0.53), title='ERA-Interim')
    ax.add_artist(leg1)

    #plt.xticks(rotation=45)
    if mask == 'LS2k': mask_description = 'interior'
    elif mask == 'LS': mask_description = ''
    elif mask == 'LSCR': mask_description = 'convection region'
    if tracer == 'vooxy': titl = 'Concentration of oxygen in the\nLabrador Sea ' + mask_description
    elif tracer == 'vodic': titl = 'Concentration of carbon in the\nLabrador Sea ' + mask_description
    plt.title(titl)
    plt.ylabel('Concentration ($mol$)') 
    plt.xlabel('Time')
    name = 'pics_bling/' + tracer + '_timeplotTEST_' + mask + d + '_over_time.png'
    if time_slice: name = 'pics_bling/' + tracer + '_timeplot_' + mask + d + '_over_time_2010-2014.png' 
    plt.savefig(name, dpi=900, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    for mask in ['LS','LSCR','LS2k']:
        for tracer in ['vooxy','vodic']:
            for depth in ['2000','1000','200','50']:
                bling_plot(mask,tracer,depth)

    #for i in ['LS2k']:#,'LSCR','LS']:
    #    for j in ['50','200','1000','2000']:
    #        bling_plot(mask=i,tracer='vooxy',d=j)

    #for mask in ['LSCR','LS2k','LS']:
    #    for time_slice in [True, False]:
    #        MLE_plot(mask, time_slice)

