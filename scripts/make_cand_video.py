import imageio 
import os
from PIL import Image
from resizeimage import resizeimage
imageio.plugins.ffmpeg.download()

field = 'Antlia'
cand = 7565

path = '/fred/oz100/swebb/make_cand_images/candidates/cand_'+ str(cand) +'_'+ field +'/'


filelist = []
files = []
for filename in os.listdir(path):
	if filename.endswith('.jpeg'):
		files.append(filename)
		
files.sort()
#print(files)

writer = imageio.get_writer('/fred/oz100/swebb/make_cand_images/candidates/cand_'+str(cand)+'_'+field+'/cand_'+str(cand)+'_jpegs.mp4', fps = 5)

for im in files:
	test = path + im
	print(test)
	writer.append_data(imageio.imread(path + im))
writer.close() 

