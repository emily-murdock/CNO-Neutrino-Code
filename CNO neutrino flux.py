#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 15:42:47 2019

@author: emily
"""

import matplotlib.pyplot as plt
import numpy as np
import urllib.request
import scipy.integrate as integrate

# Pull data from N13 and scale it (also change from seconds to years)
f= urllib.request.urlopen("http://www.sns.ias.edu/~jnb/SNdata/Export/CNOspectra/n13.dat")
page1 = f.read().decode("utf-8")
f.close()

linesN = page1.splitlines()

rawflux_n13 = []
rawenergy_n13 = []
for line in range(len(linesN)):
    a = linesN[line]
    rawenergy_n13.append(float(a[3:13]))
    rawflux_n13.append(float(a[15:]))

flux_n13 = []
for n in range(len(rawflux_n13)):
    flux_n13.append(rawflux_n13[n]*2.78e8*31536000) 
    
#plt.plot(rawenergy_n13, flux_n13)
    
    
#Pull data from O15 and scale it
g = urllib.request.urlopen("http://www.sns.ias.edu/~jnb/SNdata/Export/CNOspectra/o15.dat")
page2 = g.read().decode("utf-8")
g.close()

linesO = page2.splitlines()

rawflux_o15 = []
rawenergy_o15 = []
for line in range(len(linesO)):
    a = linesO[line]
    rawenergy_o15.append(float(a[3:13]))
    rawflux_o15.append(float(a[15:]))
    
flux_o15 = []
for n in range(len(rawflux_o15)):
    flux_o15.append(rawflux_o15[n]*2.05e8*31536000)
    
#plt.plot(rawenergy_o15, flux_o15)    
    
#Pull data from F17 and scale it
h = urllib.request.urlopen("http://www.sns.ias.edu/~jnb/SNdata/Export/CNOspectra/f17.dat")
page3 = h.read().decode("utf-8")
h.close()

linesF = page3.splitlines()

rawflux_f17 = []
rawenergy_f17 = []
for line in range(len(linesF)):
    a = linesF[line]
    rawenergy_f17.append(float(a[3:13]))
    rawflux_f17.append(float(a[15:]))

flux_f17 = []
for n in range(len(rawflux_f17)):
    flux_f17.append(rawflux_f17[n]*5.92e6*31536000)
    
#plt.plot(rawenergy_f17, flux_f17)


#find polynomial approximations for each function

pn13 = np.polyfit(rawenergy_n13, flux_n13,5)
po15 = np.polyfit(rawenergy_o15, flux_o15,5)
pf17 = np.polyfit(rawenergy_f17, flux_f17,5)

#find total flux

energyuo = rawenergy_n13 + rawenergy_o15 + rawenergy_f17
energyuo.sort()

totenergy = []
totflux = []

for x in energyuo:
    if x <= 1.199:
        totenergy.append(x)
        a = np.polyval(pn13,x)
        b = np.polyval(po15,x)
        c = np.polyval(pf17,x)
        newflux = a + b + c
        totflux.append(newflux)
    elif x<= 1.732:
        totenergy.append(x)
        b = np.polyval(po15,x)
        c = np.polyval(pf17,x)
        newflux = b + c
        totflux.append(newflux)
    else:
        totenergy.append(x)
        c = np.polyval(pf17,x)
        newflux = c
        totflux.append(newflux)

#plt.plot(totenergy,totflux)


#cross section in cm^2 per MeV = 9.5e-45

events = []

for x in range(len(totenergy)):
    events.append(totflux[x]*totenergy[x]*9.5e-45)
    
plt.plot(totenergy,events)
plt.yscale('log')
plt.xlim(0.6,1.8)

















