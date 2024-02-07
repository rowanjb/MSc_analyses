#simple throwaway script making plots of data 

import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import xarray as xr
import LSmap 
import numpy as np
import pandas as pd
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

def heat(variable,mask,time_slice):
    for i in [1,2]:
        for depth in ['2000']:#['50','200','1000','2000']:

            fig, (ax1, ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]}, layout="constrained")
            fig.set_figwidth(8.5)
            #fig.suptitle(')
            #plt.grid(axis = 'x')

            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))#'%m/%d/%Y'))
            interval = 1
            #if time_slice: interval=1
            ax1.xaxis.set_major_locator(mdates.YearLocator(interval))#(interval=365)) #with YearLocator(1) the ticks are at the start of the year

            lines = []
            avg_values = []
            runs = ['EPM157','EPM151','EPM155','EPM158','EPM152','EPM156']
            for run in runs:
                if variable=='votemper': path_variable = '_votemper_spaceAvg_'
                if variable=='HC': path_variable = '_HC_spaceSum_'
                path = run + '_heat/' + run + path_variable + mask + depth + '.nc'
                data2plot = xr.open_dataarray(path)
                if variable=='HC': data2plot = data2plot.where(data2plot > 1000)#, drop=True)
                if time_slice: data2plot = data2plot.sel(time_counter=slice('2010-01-01', '2014-01-01'))
                if not time_slice: data2plot = data2plot.sel(time_counter=slice('2007-12-01','2018-04-01')) # data2plot.time_counter[-1]))
                dates = data2plot.indexes['time_counter'].to_datetimeindex(unsafe=True) #Beware: warning turned off!!
                dates = [d.date() for d in dates]
                avg_values.append(data2plot.mean().to_numpy())
                plt.rc('axes', prop_cycle=custom_cycler)
                lines += ax1.plot(dates, data2plot, label=legend_dict[run])

            #labels = [l.get_label()[2:] for l in lines]
            #linestyles = [l.get_linestyle() for l in lines]
            #leg1 = plt.legend(lines[:3],labels[:3], loc='upper left', bbox_to_anchor=(1, 0.48), title='CGRF')
            #plt.legend(lines[3:], labels[3:], loc='lower left', bbox_to_anchor=(1, 0.53), title='ERA-Interim')
            #ax.add_artist(leg1)
            
            #plt.xticks(rotation=45)
            if mask == 'LS2k': mask_description = 'interior where depth > 2000 m'
            elif mask == 'LS': mask_description = ''
            elif mask == 'LSCR': mask_description = 'convection region'
            elif mask == 'LS3k': mask_description = 'interior where depth > 3000 m'
            if variable=='votemper': titl = 'Average temperature in the top ' + depth + ' m of \nthe Labrador Sea ' + mask_description
            if variable=='HC': titl = 'Heat content in the top ' + depth + ' m of \nthe Labrador Sea ' + mask_description
            fig.suptitle(titl,fontsize=16)
            ax1.set_title('Rolling mean')
            if variable=='HC': ax1.set_ylabel('Heat Content ($J$)')
            if variable=='votemper': ax1.set_ylabel('Temperature ($\degree C$)') 
            #ax1.set_xlabel('Time')

            #adding bar plots
            #runs = ['EPM157','EPM151','EPM155','EPM158','EPM152','EPM156']
            labels = [legend_dict[run][2:] for run in runs]
            data2plot = pd.DataFrame({'runs': labels, 'val': avg_values},index=runs)
            data2plot['val']=data2plot['val'].astype(float)
            data2plot = data2plot.reindex(['EPM157','EPM158','EPM151','EPM152','EPM155','EPM156'])
            h = "///"
            data2plot.plot.bar(x='runs',y='val',edgecolor='w',color=[c1,c1,c2,c2,c3,c3], hatch=["",h,"",h,"",h], ax=ax2, width=1, legend=False, rot=35, xlabel='', ylabel='')
            ax2.set_title('Long-term\nmean')
            ax2.set_xticks([0.5,2.5,4.5], ['Control','Tides','Tides + \nSMLEs'],rotation=0)
            #ax2.set_ylim(bottom=min(avg_values)-(max(avg_values)-min(avg_values))*0.2)
            labels = ['CGRF','ERA-I']
            hatches = ['',h]
            handles = [plt.Rectangle((0,0),1,1, fill=0, hatch=hatches[n]) for n,label in enumerate(labels)]
            ax2.legend(handles, labels, loc='upper left')
            ax2.set_ylim(bottom=min(avg_values)-100000000, top=max(avg_values)+300000000)
            def perc_diff(run1,run2):
                y0=data2plot.loc[run1,'val']
                y1=data2plot.loc[run2,'val']
                return 100*(y0-y1)/y1
            labls = [perc_diff('EPM157','EPM157'),perc_diff('EPM158','EPM158'),perc_diff('EPM151','EPM157'),perc_diff('EPM152','EPM158'),perc_diff('EPM155','EPM157'),perc_diff('EPM156','EPM158')]
            kwargs = {'rotation':90}
            ax2.bar_label(ax2.containers[0], labels=[f'{i:+.2f}%' for i in labls],padding=3,**kwargs)# [''] + [f'{(y1 - y0) / y0 * 100:+.2f}%' for y0, y1 in zip(y[:-1], y[1:])])
            name = 'pics_heat/' + variable + '_' + mask + depth + '_over_time.png'
            if time_slice: name = 'pics_heat/' + variable + '_' + mask + depth + '_over_time_2010-2014.png' 
            plt.savefig(name, dpi=900, bbox_inches="tight")
            plt.close(fig)

if __name__ == "__main__":
    for variable in ['HC']:#,'votemper']:
        for mask in ['LS3k']:#['LS','LSCR','LS2k']:
            for time_slice in [False]:#,True]:
                heat(variable,mask,time_slice)
