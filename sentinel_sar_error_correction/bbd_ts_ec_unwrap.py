from PIL import Image, ImageOps
from matplotlib import pyplot as plt
import sentinel1helper as sh
import numpy as np
import pandas as pd
import geopandas as gpd

#bbd time series error correction unwrapping errors

half_wave_length = 5.56/2
max_wrap_cycles = 5

num_of_ts = 12
in_file = '/media/hog/fringe1/dev/data/testn.csv'
in_file = '/media/hog/fringe1/dev/data/tl5_l2b_044_02_0001-0200.csv'
#in_file = '/media/hog/fringe1/sc/MSCDATA/Roenne-Overview/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
#in_layer = 'tl5_a_044_01_mscaoi'
#in_file = '/media/nas01/hog/sc/sc_data/BBD_TL5/schleswig-holstein/l2b_schleswig-holstein_clipped.gpkg'
#in_layer = 'ASCE_044_02'
#df = sh.read_geofile(in_file, layer=in_layer, engine='pyogrio')
df = pd.read_csv(in_file)

dates, dats, nodats = sh.get_datatime_dates(df.columns)
data = df.loc[:,'date_20150406':'date_20211230'].to_numpy()
print(data.shape)
print(df.head())

#plt.imshow(data, cmap="gray")

this_markerdict = {}
#data.shape[0]
#for idx in range(0,len(data)):
for idx in range(0,200):
    print(idx)
    num_of_ts = idx
    sig_diff = [j-i for i,j in zip(data[num_of_ts,0:-1], data[num_of_ts,1:])]
    sig_diff = [0] + sig_diff
    #print('idx: ', idx, ' len sig_diff: ', len(sig_diff), ' len ts: ', len(data[num_of_ts,:]))


    for gm, d in zip(sig_diff, dates):
        wrap = int(abs(gm)//half_wave_length)
        if wrap > max_wrap_cycles:        
            if d in this_markerdict.keys():
                this_markerdict[d] = this_markerdict[d]+1
            else:
                this_markerdict[d] = 1
        

        
print(np.mean(sig_diff), np.std(sig_diff))
print(len(data))

plt.figure()
plt.bar(this_markerdict.keys(), this_markerdict.values(), bottom=0, width=0.5)
#plt.xticks(dates, range(0,len(dates)))
bx=plt.gca()
bx.axes.xaxis.set_ticklabels([])

plt.figure()
plt.plot(dates, data[num_of_ts,:])
plt.figure()
plt.hist(data[num_of_ts,0:-1], bins=20)


plt.figure()
sig_diff_corr = []
for gm, d in zip(sig_diff, dates):
    wrap = int(abs(gm)//half_wave_length)
    if wrap >= max_wrap_cycles:        
        sig_diff_corr.append(gm-half_wave_length*np.sign(gm)*(wrap-1))
        #print(gm, (gm%bw_half_pi)*np.sign(gm))
    else:
        sig_diff_corr.append(gm)
        #print(gm)

ax = plt.gca()
#ax.grid(which='major', color='#DDDDDD', alpha=0.5)
#ax.grid(which='minor', color='#DDDDDD', alpha=0.5)
#ax.minorticks_on()
this_upper_bound = [np.mean(sig_diff) +  half_wave_length + np.std(sig_diff) for i in dates]
this_lower_bound = [np.mean(sig_diff) -  half_wave_length - np.std(sig_diff) for i in dates]
#plt.fill_between(dates, this_lower_bound, this_upper_bound, color='lightgray', alpha=0.5)
plt.plot(dates, data[num_of_ts,:], label='data')
#plt.stem(dates, sig_diff, label='sig_diff')
#plt.stem(dates, sig_diff_corr, linefmt='darkred',label='sig_diff_corr')
plt.plot(dates, np.cumsum(sig_diff_corr), label='cumsum sig_diff_corr')
# #plt.plot(dates, np.cumsum(sig_diff), label='cumsum sig_diff')
plt.legend()
#
# #'plt.grid(axis='x', which='minor')
print(dates, df.iloc[num_of_ts,0:-1])
plt.show()

