#messy script I threw together to make figs for a conference 

import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import xarray as xr
import LSmap
import numpy as np
from matplotlib.lines import Line2D
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

def MLD_plot(variable,mask,time_slice,ARGO=False):

    for k in [1,2]: #for some reason, the cycler doesn't apply on the first loop, so here I'm plotting twice (which is the easiest fix)

        fig, ax = plt.subplots()
        #plt.grid(axis = 'x')

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))#'%m/%d/%Y'))
        interval = 1
        #if time_slice: interval=1
        ax.xaxis.set_major_locator(mdates.YearLocator(interval))#(interval=365)) #with YearLocator(1) the ticks are at the start of the year

        if ARGO==True:
            data2plot=xr.open_dataarray('./ARGO/mixedlayer_UCSD/ARGO_da_mld.nc')
            if time_slice: data2plot = data2plot.sel(date=slice('2010-01-01', '2014-01-01'))
            elif not time_slice: data2plot = data2plot.sel(date=slice('2010-01-01','2020-01-01')) # data2plot.time_counter[-1]))
            dates = data2plot.date
            argo1 = ax.scatter(dates,data2plot,c='k',s=5, label='ARGO da_mld')
            
            data2plot=xr.open_dataarray('./ARGO/mixedlayer_UCSD/ARGO_dt_mld.nc')
            if time_slice: data2plot = data2plot.sel(date=slice('2010-01-01', '2014-01-01'))
            elif not time_slice: data2plot = data2plot.sel(date=slice('2010-01-01','2020-01-01')) # data2plot.time_counter[-1]))
            dates = data2plot.date
            argo2 = ax.scatter(dates,data2plot,c='r',s=5, label='ARGO dt_mld')
            
            plt.legend(loc='lower left', bbox_to_anchor=(1, 0.2), title='Observations')

        lines = []
        for run in ['EPM157','EPM151','EPM155','EPM158','EPM152','EPM156']:
            path = run + '_MLD/' + run + '_' + variable + '_time_plot_' + mask + '.nc'# run + '_heat/' + run + path_variable + mask + depth + '.nc'
            data2plot = xr.open_dataarray(path,engine='netcdf4')
            print(run)
            if time_slice: data2plot = data2plot.sel(time_counter=slice('2010-01-01', '2014-01-01'))
            if not time_slice: data2plot = data2plot.sel(time_counter=slice('2010-01-01','2020-01-01')) # data2plot.time_counter[-1]))
            dates = data2plot.indexes['time_counter'].to_datetimeindex(unsafe=True) #Beware: warning turned off!!
            dates = [d.date() for d in dates]
            plt.rc('axes', prop_cycle=custom_cycler)
            lines += ax.plot(dates, data2plot, label=legend_dict[run])

        quit()

        #lines = []
        #for run in ['EPM157','EPM151','EPM155','EPM158','EPM152','EPM156']:
        #    path = run + '_MLD/' + run + '_' + variable + '_time_plot_' + mask + '.nc'
        #    data2plot = xr.open_dataarray(path)
        #    #if variable=='max_MLD': 
        #    #    data2plot = data2plot.where(data2plot <= -1000)#, drop=True)
        #    #    data2plot = -1*data2plot
        #    if time_slice: data2plot = data2plot.sel(time_counter=slice('2010-01-01', '2014-01-01'))
        #    if not time_slice: data2plot = data2plot.sel(time_counter=slice('2010-01-01','2020-01-01')) # data2plot.time_counter[-1]))
        #    dates = data2plot.indexes['time_counter'].to_datetimeindex(unsafe=True) #Beware: warning turned off!!
        #    dates = [d.date() for d in dates]
        #    plt.rc('axes', prop_cycle=custom_cycler)
        #    lines += ax.plot(dates, data2plot, label=legend_dict[run])

        labels = [l.get_label()[2:] for l in lines]
        linestyles = [l.get_linestyle() for l in lines]
        leg1 = plt.legend(lines[:3],labels[:3], loc='upper left', bbox_to_anchor=(1, 0.48), title='CGRF')
        leg2 = plt.legend(lines[3:], labels[3:], loc='lower left', bbox_to_anchor=(1, 0.53), title='ERA-Interim')
        ax.add_artist(leg1)
        ax.add_artist(leg2)

        #argo_circles = Line2D([0], [0], linestyle="none", marker="o", alpha

        ##labels = [l.get_label()[2:] for l in lines]
        ##linestyles = [l.get_linestyle() for l in lines]
        ##leg1 = plt.legend(lines[:3],labels[:3], loc='upper left', bbox_to_anchor=(1, 0.48), title='CGRF')
        ##plt.legend(lines[3:], labels[3:], loc='lower left', bbox_to_anchor=(1, 0.53), title='ERA-Interim')
        ##ax.add_artist(leg1)

        ###plt.xticks(rotation=45)
        ##if mask == 'LS2k': mask_description = 'interior'
        ##elif mask == 'LS': mask_description = ''
        ##elif mask == 'LSCR': mask_description = 'convection region'
        ##if variable=='max_MLD': titl = 'Max mixed layer depth in \nthe Labrador Sea ' + mask_description
        ##if variable=='avg_MLD': titl = 'Average mixed layer depth in \nthe Labrador Sea ' + mask_description
        ##plt.title(titl)
        ##plt.ylabel('MLD ($m$)')
        ##plt.xlabel('Time')
        ##name = 'pics_MLD/' + variable + '_' + mask + '_over_time'
        ##if time_slice: name = name + '_2010-2014'
        ##name = name + 'ARGO_test.png'
        ##plt.savefig(name, dpi=900, bbox_inches="tight")
        ##plt.close(fig)
        
        #labels = [l.get_label()[2:] for l in lines]
        #linestyles = [l.get_linestyle() for l in lines]
        #leg1 = plt.legend(lines[:3],labels[:3], loc='upper left', bbox_to_anchor=(1, 0.48), title='CGRF')
        #plt.legend(lines[3:], labels[3:], loc='lower left', bbox_to_anchor=(1, 0.53), title='ERA-Interim')
        #ax.add_artist(leg1)

        #plt.xticks(rotation=45)
        if mask == 'LS2k': mask_description = 'interior'
        elif mask == 'LS': mask_description = ''
        elif mask == 'LSCR': mask_description = 'convection region'
        if variable=='avg_MLD': titl = 'Average mixed layer depth in \nthe Labrador Sea ' + mask_description
        if variable=='max_MLD': titl = 'Max mixed layer depth in \nthe Labrador Sea ' + mask_description
        plt.title(titl)
        plt.ylabel('MLD ($m$)')
        plt.xlabel('Time')
        name = 'pics_MLD/AAAtestestest' + variable + '_' + mask + '_over_time.png'
        if time_slice: name = 'pics_MLD/AAAtestestest' + variable + '_' + mask + '_over_time_2010-2014.png'
        plt.savefig(name, dpi=900, bbox_inches="tight")
        plt.close(fig)


def MLD_bar(mask):

    runs = []
    MLDs = []
    for run in ['EPM157','EPM151','EPM155','EPM158','EPM152','EPM156']:
        path = run + '_MLD/' + run + '_' + variable + '_time_plot_' + mask + '.nc'
        da = xr.open_dataarray(path)
        da = da.sel(time_counter=slice('2010-01-01','2020-01-01')) # data2plot.time_counter[-1]))
        month = da.groupby('time_counter.month').mean(dim='time_counter')
        winter = month.where( (month.month > 11) | (month.month < 6), drop=True).mean(dim='month')
        runs.append(run)
        MLDs.append(round(float(winter.to_numpy()),1))
  
    #forcing = ('CGRF','ERA-Interim')
    #data2plot = {
    #    'control': (MLDs[0],MLDs[3]),
    #    'tides': (MLDs[1],MLDs[4]),
    #    'tides + SMLEs': (MLDs[2],MLDs[5])
    #}
#
#    x = np.arange(len(forcing)) 
#    width = 0.25
#    multiplier = 0
#    
#    fig,ax = plt.subplots(layout='constrained')
#    for attribute,depths in data2plot.items():
#        offset = width*multiplier
#        rects = ax.bar(x+offset, depths, width, label=attribute)
#        ax.bar_label(rects, padding=3)
#        multiplier += 1
    
    fig, ax = plt.subplots(layout="constrained")
    fig.set_figwidth(6.5)

    b1 = ax.bar(0.10, MLDs[0], 0.1, label=run[0], color=c1)
    ax.bar_label(b1, padding = 2)
    
    b2 = ax.bar(0.20, MLDs[1], 0.1, label=run[1], color=c2)
    ax.bar_label(b2, padding = 2)
    
    b3 = ax.bar(0.30, MLDs[2], 0.1, label=run[2], color=c3)
    ax.bar_label(b3, padding = 2)
    
    b4 = ax.bar(0.50, MLDs[3], 0.1, label=run[3], color=c4)
    ax.bar_label(b4, padding = 2)
    
    b5 = ax.bar(0.60, MLDs[4], 0.1, label=run[4], color=c5)
    ax.bar_label(b5, padding = 2)
    
    b6 = ax.bar(0.70, MLDs[5], 0.1, label=run[5], color=c6)
    ax.bar_label(b6, padding = 2)
    
    #labels = [l.get_label()[2:] for l in lines]
    #linestyles = [l.get_linestyle() for l in lines]
    #leg1 = plt.legend(lines[:3],labels[:3], loc='upper left', bbox_to_anchor=(1, 0.48), title='CGRF')
    #plt.legend(lines[3:], labels[3:], loc='lower left', bbox_to_anchor=(1, 0.53), title='ERA-Interim')
    #ax.add_artist(leg1)

    plt.legend([b1,b2,b3], ['control','tides','tides+SMLEs'], loc='lower left', bbox_to_anchor=(1, 0.53))

    if mask == 'LS2k': mask_description = 'interior'
    elif mask == 'LS': mask_description = ''
    elif mask == 'LSCR': mask_description = 'convection region'
    titl = 'Average winter mixed layer depth in \nthe Labrador Sea ' + mask_description
    plt.title(titl)
    plt.ylabel('Depth ($m$)')
    plt.xticks([0.2,0.6],['CGRF','ERA-Interim'])
    plt.ylim(0,2200)
    name = 'pics_MLD/winterBarChartMLD_' + mask
    name = name + '.png'
    plt.savefig(name, dpi=900, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    MLD_plot('avg_MLD','LS',time_slice=True,ARGO=True)
    quit()

    for variable in ['avg_MLD', 'max_MLD']:
        for mask in ['LSCR','LS2k','LS']:
            MLD_bar(mask)
            #for time_slice in [False,True]: #whether you want a shorter slice of time
            #    MLD_plot(variable, mask, time_slice)
                #MLD_plot_with_Argo(variable, mask)
