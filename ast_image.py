from __future__ import division, print_function

import numpy as np
from astropy import wcs
from astropy.io import fits
import sys
import math
import os
import glob
import sys
import datetime as dt 



#--------DEFS---------------
def RAdec_to_RAsex(fRAdec):
    fratotsec = (math.fabs(float(fRAdec))*3600.0)
    frah2 = (math.modf(fratotsec/3600.0)[1])
    fram2 = (math.modf((fratotsec-(frah2*3600.0))/60.0)[1])
    fras2 = (fratotsec-(frah2*3600.0)-(fram2*60.0))
    if round(fras2, 2) == 60.00:
        fram2 = fram2 + 1
        fras2 = 0
        if round(fram2, 2) == 60.00:
            frah2 = frah2 + 1
            fram2 = 0
    if round(fram2, 2) == 60.00:
        frah2 = frah2 + 1
        fram2 = 0
    if int(frah2) == 24 and (int(fram2) != 0 or int(fras2) != 0):
        frah2 = frah2 - 24
    fRAsex = '%02i' % frah2 + ' ' + '%02i' % fram2 + ' ' + ('%.3f' % float(fras2)).zfill(6)
    return fRAsex



def DEdec_to_DEsex(fDEdec):
    fdetotsec = (math.fabs(float(fDEdec))*3600.0)
    fded2 = (math.modf(fdetotsec/3600.0)[1])
    fdem2 = (math.modf((fdetotsec-(fded2*3600.0))/60.0)[1])
    fdes2 = (fdetotsec-(fded2*3600.0)-(fdem2*60.0))
    if float(fDEdec) < 0:
        fded2sign = '-'
    else:
        fded2sign = '+'
    fDEsex = fded2sign + '%02i' % fded2 + ' ' + '%02i' % fdem2 + ' ' + ('%.2f' % float(fdes2)).zfill(5)
    return fDEsex
    
    
def RAsex_to_RAdec(fRAsex):
    frah = float(fRAsex[0:2])
    fram = float(fRAsex[3:5])
    fras = float(fRAsex[6:])
    fRAdec = (frah*3600.0+fram*60.0+fras)/3600.0
    return fRAdec

def DEsex_to_DEdec(fDEsex):
    fded = float(fDEsex[0:3])
    fdem = float(fDEsex[4:6])
    fdes = float(fDEsex[7:])    
    fDEdec = (math.fabs(fded)*3600.0+fdem*60.0+fdes)/3600.0
    if fDEsex[0] == '-':
        fDEdec = fDEdec * -1
    return fDEdec
    
    
    
############---------Commend line imputs ----------##########
print(sys.argv)
if len(sys.argv)>1:

    objid =sys.argv[1]
    #day = sys.argv[2]
    #sci_sub = sys.argv[3]
    




f=open('/fred/oz100/swebb/open_cands/transients_coo_DWFJun18_RT.txt')
for line in f:
    line = line.split()
    if line[0]==objid:
         ra, dec, field, ccd_num = str(line[1]), str(line[2]), str(line[3]), str(line[6])
		
f.close()
print(ra, dec, field, ccd_num) 


path ='/fred/oz100/pipes/DWF_PIPE/MARY_WORK/'+ field + '_18060*_mrt1_*/ccd'+ccd_num+'/images_resampled/sci_*.resamp.fits'

print(path)
path_insidefield=[]

fitsfileslist=glob.glob(path)
#print(fitsfileslist)
mydic={}

for path in fitsfileslist: 
	hdulist = fits.open(path)
	w = wcs.WCS(hdulist[0].header) 
	head = hdulist[0].header
	print(head)
	xlim=head['NAXIS1']
	ylim=head['NAXIS2']
	date= dt.datetime.strptime(head['DATE'], '%Y-%m-%dT%H:%M:%S')
	
	pixcrd = np.array([[ra, dec]], np.float_)
	print(pixcrd)
	
	worldpix = w.wcs_world2pix(pixcrd, 1)
	pixx, pixy= worldpix[0][0], worldpix[0][1]
	print(pixx, pixy)
        
	if pixy < ylim and pixy > 0 and pixx < xlim and pixx > 0:
		path_insidefield.append(path)
		mydic[date]= path
	

path2_insidefield = []
datelist = []
for key in sorted(mydic.keys()):
	path2_insidefield.append(mydic[key])
	datelist.append(key)
	
print(path2_insidefield)





ds9string='ds9 -zscale '



for i in range(len(path2_insidefield)):
    
    ds9string=ds9string+path2_insidefield[i]+' -crosshair '+str(ra)+' '+str(dec)+' wcs fk5 -match wcs -pan to '+str(ra)+' '+str(dec)+' wcs fk5 '
    
    
ds9string=ds9string+' -saveimage /fred/oz100/swebb/open_cands/TEST_images/'+objid+'_ast.jpeg &'


os.system(ds9string)
    
    

 

