from sherpa.astro.ui import*
from astropy.io import fits
from astropy.table import Table
import matplotlib.pyplot as plt
import numpy


set_conf_opt("max_rstat",1000)
RQ= fits.open('GammaF00.fits')
RQT=Table(RQ[1].data)
phafiles= RQT['PHA_files']
name_arr = []
data_sum_arr = []
data_cnt_rate_arr = []
bkg_sum_arr = []
bkg_cnt_rate_arr = []
bkg_scale=[]
goodness_arr = []
gamma_fit_arr=[]
#gamma_conf_arr=[]
gamma_min_arr=[]
gamma_max_arr=[]


set_stat("wstat")
lo=0.5 
hi=7.0

for i in range(len(phafiles)):
    load_data(i,str(phafiles[i]))

    #spectrum_characteristics
    name = phafiles[i]
    data_sum = calc_data_sum(lo,hi,id=i)
    print(data_sum)
    data_cnt_rate = calc_data_sum(lo,hi,id=i)/get_exposure(id=i)
    print(data_cnt_rate)
    #Back scale 
    bkg = get_bkg_scale(id=i)

    bkg_sum = calc_data_sum(lo,hi,id=i,bkg_id=1)*bkg 
    print(bkg_sum)
    bkg_cnt_rate = calc_data_sum(lo,hi,id=i,bkg_id=1)/get_exposure(id=i,bkg_id=1)
    print(bkg_cnt_rate)
    spec1 = plot_data(i)
    plt.savefig(f'spec1-id{i}.png')

    #Energy_filtering 
    notice_id(i,0.5, 7.0)
    spec2=plot_data(i)
    plt.savefig(f'spec2-id{i}.png')



    #choosing_fitting _model
    p = get_data_plot_prefs()
    p["xlog"] = True
    p["ylog"] = True
    s = set_source(i,xsphabs.abs1 * powlaw1d.p1) 
    NH = RQT['LOGNH'][i]
    abs1.nH = numpy.power(10,(NH -22.0))
    freeze(abs1.nH)
    g = guess(i,p1)

    fit(i)
    res = get_fit_results()
    dres = dict(zip(res.parnames, res.parvals))
    gamma_fit = dres['p1.gamma'] 

    #statistical_values_for_gamma
    c = get_stat_name()
    goodness = get_stat_info()[i].statval
    spec3 = plot_fit_ratio(i,xlog=True, ylog=True)
    plt.savefig(f'spec3-id{i}.png')

    conf(i)
    res1 = get_conf_results()    
    dres1 = dict(zip(res1.parnames,res1.parvals ))
    dres2 = dict(zip(res1.parnames,res1.parmins ))
    dres3 = dict(zip(res1.parnames,res1.parmaxes ))
    gamma_conf= dres1['p1.gamma']
    gamma_min= dres2['p1.gamma']
    gamma_max= dres3['p1.gamma']

   

    name_arr.append(name)
    data_sum_arr.append(data_sum)
    data_cnt_rate_arr.append(data_cnt_rate)
    bkg_sum_arr.append(bkg_sum)
    bkg_cnt_rate_arr.append(bkg_cnt_rate)
    bkg_scale.append(bkg)
    goodness_arr.append(goodness)
    gamma_fit_arr.append(gamma_fit)
    #gamma_conf_arr.append(gamma_conf)
    gamma_min_arr.append(gamma_min)
    gamma_max_arr.append(gamma_max)

gamma_min_arr = numpy.array(gamma_min_arr)
gamma_min_arr[gamma_min_arr == None] = numpy.nan
gamma_max_arr = numpy.array(gamma_max_arr)
gamma_max_arr[gamma_max_arr == None] = numpy.nan

save_arrays('ya_rab.fits', [name_arr , data_sum_arr, data_cnt_rate_arr, bkg_sum_arr, bkg_cnt_rate_arr,bkg_scale,goodness_arr, gamma_fit_arr, gamma_min_arr.tolist(), gamma_max_arr.tolist() ], ["sperctral_name" ,"total_cnts" ,"cnt_rate" , "bkg_cnts" , "bkg_cnt_rate","bkg_scale" ,"goodness" ,"Photon_index" ,"Photon_index_min","Photon_index_max" ], ascii=False, clobber=True)



#gamma_conf_arr,
#"Photon_index_conf", 

#TO_save_results
#save_arrays('ya_rab.fits', [name_arr , data_sum_arr, data_cnt_rate_arr, bkg_sum_arr, bkg_cnt_rate_arr,bkg_scale,goodness_arr, gamma_fit_arr,  gamma_min_arr, gamma_max_arr ], ["sperctral_name" ,"total_cnts" ,"cnt_rate" , "bkg_cnts" , "bkg_cnt_rate","bkg_scale " ,"goodness" ,"Photon_index" ,"Photon_index_min","Photon_index_max" ], ascii=False, clobber=True)
    







