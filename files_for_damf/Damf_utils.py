# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 14:14:16 2023

@author: Karolin Voss
"""

#Compilation of DAMF functions

import numpy as np
import pandas as pd
from datetime import datetime, timezone
from scipy.interpolate import interp1d


#%%
def Damf2SCDair(PATH_damf, prefix):
    AMF = np.loadtxt(PATH_damf + prefix + '.amf')
    VD = np.loadtxt(PATH_damf + prefix + '.vd',unpack=True)
    BZP = np.loadtxt(PATH_damf + prefix + '.bzp',unpack=True)
    balloon_altitude = BZP[-1]
    
    dVDair = VD[2] # VCD_air for each layer in seg
    # height = VD[-1] -0.5 * VD[-1,0]
    layerheight = VD[-1] - VD[-2]

    SCD_air = AMF @ (dVDair * layerheight *1e5) # factor for calculating VCD from number density in 1/cm^2
    return AMF, SCD_air, balloon_altitude, VD

def readDamf(PATH_damf, prefix):
    # write DAMF output from different files into one dictionary
    AMF = np.loadtxt(PATH_damf + prefix + '.amf')
    
    VD = pd.read_csv(PATH_damf + prefix + '.vd', header=1)
    day, month, year, hour, minute, sec, longitude, latitude, balloon_altitude = np.loadtxt(PATH_damf + prefix + '.bzp',unpack=True, skiprows=1)

    time_specs = []
    for i in len(day):
        dateandtime = datetime.datetime(int(year[i]), int(month[i]), int(day[i]), hour = int(hour[i]), minute=int(minute[i]), second= int(sec[i]))
        dateandtime = dateandtime.replace(tzinfo=timezone.utc)
        time_specs.append(dateandtime)
    # put all variables of interest into dictionary
    DAMF = {}
    DAMF['AMF'] = AMF
    DAMF['balloon_altitude'] = balloon_altitude
    DAMF['time_spec'] = time_specs
    DAMF['VD'] = VD
    DAMF['air number density'] = VD[2]

def CorrectAMFinBalloonLayer(AMF, vd, sza, altitude):
    '''
    corrects the AMF of the layer where the balloon is in for SZA < 85°

    Parameters
    ----------
    AMF : 2d array
        DESCRIPTION.
    vd : TYPE
        DESCRIPTION.
    sza : TYPE
        DESCRIPTION.
    altitude : TYPE
        DESCRIPTION.

    Returns
    -------
    AMF_corr : 2d array
        DESCRIPTION.

    '''
    AMF_corr = AMF.copy()
    for spec in range(10,len(AMF[:,0])):
        print('Spectrum number: ' + str(spec))
        h_balloon = altitude[spec]
        number_density = vd[2]
        height_layers = vd[-2] + (vd[-1]- vd[-2])/2
        height2number_density = interp1d(height_layers, number_density)
        print('The balloon is at ' + str(h_balloon) + ' km.')
        # find layer than balloon is in
        for layer_index in range(len(AMF[0,:])):
                hlayer_top = vd[-1, layer_index]
                hlayer_bottom = vd[-2,layer_index]
                # print('Layer goes from '+ str(hlayer_bottom)+ ' km up to ' + str(hlayer_top) + ' km.')
                if np.logical_and(h_balloon >= hlayer_bottom, h_balloon < hlayer_top):
                    print('balloon_layer found, index is '+ str(layer_index) + '.')
                    balloonlayer_index = layer_index
                    # calculate number density of air at specific points
                    n_balloon = height2number_density(h_balloon)
                    n_top = height2number_density(hlayer_top)
                    n_bottom = height2number_density(hlayer_bottom)
        corr_factor = (n_balloon - n_top) / (n_bottom - n_top)
        print('corr_factor is: ' + str(corr_factor))
                
        AMF_balloonlayer = AMF[spec, balloonlayer_index+1] * corr_factor
        print('this leads to an AMF of ' + str(AMF_balloonlayer))
        if sza[spec] < 85:
            AMF_corr[spec, balloonlayer_index] = AMF_balloonlayer
            print('before: ' + str(AMF[spec, balloonlayer_index]) + ', after: ' + str(AMF_corr[spec, balloonlayer_index]))
        else:
            print('no')
    return AMF_corr

def readTrajetory(PATH):
    """
    reads CNES trajectory file and returns time GPS height, pressure and Gas Temp

    Parameters
    ----------
    PATH : str

    Returns
    -------
    time : datetime array
    GPS_height_balloon : array
    pressure : array
    GasTemp : array

    """
    data = np.loadtxt(PATH, skiprows=3, usecols=(3, 4, 5), delimiter="\t")
    time_raw = np.loadtxt(PATH, skiprows=3, usecols=(0), delimiter="\t", dtype=str)

    time = []
    for i in time_raw:
        dummy = datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
        dummy = dummy.replace(tzinfo=timezone.utc)
        time.append(dummy.timestamp())

    # trajectory = np.vstack((time, data[:, 0], data[:, 1], data[:, 2]))
    GPS_height_balloon =  data[:, 0]
    pressure =  data[:, 1]
    GasTemp = data[:, 2]
    return time, GPS_height_balloon, pressure, GasTemp

def calc_SCDair(AMF, VD):
    dVDair = VD[2] # VCD_air for each layer in seg
    # height = VD[-1] -0.5 * VD[-1,0]
    layerheight = VD[-1] - VD[-2]

    SCD_air = AMF @ (dVDair * layerheight *1e5) # factor for calculating VCD from number density in 1/cm^2
    return SCD_air

def readStdAtmo(PATH):
    atmodata = np.loadtxt(PATH,skiprows=2) #,unpack=True)
    StdAtmo = pd.DataFrame(atmodata, columns=['height/km', 'temperature/K', 'pressure/mbar'])
    # StdAtmo = pd.read_csv(PATH, comment='#', names=['Height/km', 'Temperature/K', 'Pressure/mbar'], index_col=False, sep=' ')
    return StdAtmo

def readDamfAtmo(Path):
    df_atmo = pd.read_csv(Path,skiprows=2,  sep=' ', names=['height/km', 'temperature/K', 'pressure/mbar'], index_col=False)
    return df_atmo