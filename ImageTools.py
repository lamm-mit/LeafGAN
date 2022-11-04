#Image processing tools

#MJ Buehler, LAMM/MIT, 2021
#Edited Sabrina Shen, LAMM/MIT, 2021

Shen, S.C., Buehler, M.J. Nature-inspired Architected materials using unsupervised deep learning. Accepted (2022).

import os,sys
import matplotlib.pyplot as plt
 
import numpy as np
import cv2
import PIL 
from PIL import Image, ImageOps

def thresh_smooth_images (path = "./source/", dest="./output/", thresh=127, ress=1024 ): 
 #
 dirs = os.listdir(path)
 
 i=0
 for item in dirs:
        fullpath = os.path.join(path,item)         #corrected
        print (item)
        if os.path.isfile(fullpath):
 
            img_rgb = cv2.imread(fullpath)
            
            img_rgb=cv2.resize(img_rgb, (ress,ress), interpolation = cv2.INTER_AREA)
            img_rgb = cv2.GaussianBlur(img_rgb, (3,3), 0)

            img_rgb = cv2.addWeighted( img_rgb,  1.2, img_rgb, 0,  0)
            
            img_rgb = cv2.bilateralFilter(img_rgb, 32,256,128)

            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            #(threshi, img_bw) = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)# | cv2.THRESH_OTSU)
            (threshi, img_gray) = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            print  (threshi)
            
            
            cv2.imwrite(dest +'%4.4d'%i+ '_smoothed.png', img_gray)
          
            i=i+1
 


 return 

def remove_small (path2 = "./source/", dest="./output/",darea=2000,ress=1024, mirrorcopy=0, ressfinal=1024, filt1=32, thicken=0, rect=10): 
 
 names=[]
 density=[]
 seeds=[]
 dirs = os.listdir(path2)

 isExist = os.path.exists(dest)

 if not isExist:
  
  # Create a new directory because it does not exist 
  os.makedirs(dest)
  print("The new directory is created: ", dest)

 i=0
 for item in dirs:
        fullpath = os.path.join(path2,item)         #corrected
        print (item)
        if os.path.isfile(fullpath):
 
             
            
            image = cv2.imread(fullpath)
            
            image=cv2.resize(image, (ress,ress), interpolation = cv2.INTER_AREA)
            #image = cv2.bilateralFilter(image, 32,256,128)
            #image = cv2.bilateralFilter(image, 32,64,64)
            image = cv2.bilateralFilter(image, filt1,256,128)
            image = cv2.bilateralFilter(image, filt1,64,64)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3,3), 0)
            #thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY  + cv2.THRESH_OTSU)[1]

            # Filter using contour area and remove small noise
            cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            for c in cnts:
                area = cv2.contourArea(c)
                #print (area)
                if area < darea:
                    cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

            # Morph close and invert image
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
            close = 255 - cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
            
            
            img_gray=close
            img_gray = (255-img_gray)
            
            #if mirrorcopy=0 just original, otherwise generate copies of unit cell (1=one unit cell, 2, 3...)
            if mirrorcopy>0:
             for ijj in range (mirrorcopy):
                flipHorizontal = cv2.flip(img_gray, 1)
                vis = np.concatenate((img_gray, flipHorizontal), axis=1)
                
                flipVertical = cv2.flip(vis, 0)
                img_gray = np.concatenate((vis, flipVertical), axis=0)
            
            
            if thicken>0:
                print ("Thickening resulting structure using dilation...iterations: ", thicken)
                kernel = np.ones((5,5),np.uint8)
                img_gray = cv2.dilate(img_gray,kernel,iterations = thicken)
            
            #resize to final desired dimension...
            img_gray=cv2.resize(img_gray, (ressfinal,ressfinal), interpolation = cv2.INTER_AREA)
            
            
            if rect>0:
            #    #add rectangle - for better 3D processing
                #rcolor = (255, 255, 255) #black
                rcolor = (0, 0, 0) #white
                cv2.rectangle(img_gray, (0,0), (img_gray.shape[0], img_gray.shape[1]), rcolor, thickness=10)
            
           
            #calculate number of white vs black pixels for density
            count = cv2.countNonZero(img_gray)
            density_l=count/(ressfinal*ressfinal)
            print("number white: ",count, "density: ",density_l)
            
            fnamee=dest +'%4.4d'%i+ '_smoothed.png'
            cv2.imwrite(fnamee, img_gray)
            
            names.append(fnamee)
            density.append (density_l)
            
            seed_=int(''.join(filter(str.isdigit, item)))
            #print (seed_)
            
            seeds.append(seed_)
             
            i=i+1
 


 return names, seeds, density

#stack images in x-y 

#ycopy = number of copues in y before assembling
#dir=1 means x, dir=2 means y (all files in directory are stiched in that way in 1D)
def stack_xy (path2 = "./source/", dest="./output/", ress=1024, mirrorcopy=0, ressfinal=1024, xcopy=0, ycopy=0, dir=1, thicken=0, rect=0, destfile=None): 
 #
 names=[]
 density=[]
 seeds=[]
 dirs = os.listdir(path2)

 isExist = os.path.exists(dest)

 if not isExist:
  
  # Create a new directory because it does not exist 
  os.makedirs(dest)
  print("The new directory is created: ", dest)
 print("Initial res: ", ress, "final max res: ", ressfinal)

 i=0
 for item in dirs:
        fullpath = os.path.join(path2,item)         #corrected
        if os.path.isfile(fullpath):
 
            print (fullpath, i)
             
            
            image = cv2.imread(fullpath)
            
            img_gray_T=cv2.resize(image, (ress,ress), interpolation = cv2.INTER_AREA)
            
            if i==0: #create initial array if starting off
                img_gray=cv2.resize(image, (ress,ress), interpolation = cv2.INTER_AREA)
                
                #if mirrorcopy=0 just original, otherwise generate copies of unit cell (1=one unit cell, 2, 3...)
                if xcopy>0:
                 for ijj in range (xcopy):
                    img_gray = np.concatenate((img_gray, img_gray), axis=1)
                if ycopy>0:
                 for ijj in range (ycopy):
                    img_gray = np.concatenate((img_gray, img_gray), axis=0)

            
            

            if i!=0:            
            #if mirrorcopy=0 just original, otherwise generate copies of unit cell (1=one unit cell, 2, 3...)
            	if xcopy>0:
             		for ijj in range (xcopy):
                		img_gray_T = np.concatenate((img_gray_T, img_gray_T), axis=1)
            	if ycopy>0:
             		for ijj in range (ycopy):
                		img_gray_T = np.concatenate((img_gray_T, img_gray_T), axis=0)
                 
            

            	if dir==1:
                 	img_gray = np.concatenate((img_gray, img_gray_T), axis=1)
            	if dir==2:
                 	img_gray = np.concatenate((img_gray, img_gray_T), axis=0)
            
            
            i=i+1
 
            
 if thicken>0:
                print ("Thickening resulting structure using dilation...iterations: ", thicken)
                kernel = np.ones((2,5),np.uint8)
                img_gray = cv2.dilate(img_gray,kernel,iterations = thicken)           
 if rect>0:
                #add rectangle - for better 3D processing
                #rcolor = (255, 255, 255) #black
                rcolor = (0, 0, 0) #white
                cv2.rectangle(img_gray, (0,0), (img_gray.shape[1], img_gray.shape[0]), rcolor, thickness=10)
            
            
 #resize to final desired dimension...

 #current res:
 resx=img_gray.shape[0]
 resy=img_gray.shape[1]
    
 minres=min (resx, resy)
 maxres=max (resx, resy)
 print ("Largest res in final image: ", maxres, "... but should be: ", ressfinal, "... ratio: ", ressfinal/maxres)
    
 #img_gray=cv2.resize(img_gray, (int(ressfinal/maxres*resy),int(ressfinal/maxres*resx)), interpolation = cv2.INTER_AREA)
            
            
            
            
 #calculate number of white vs black pixels for density
 #count = cv2.countNonZero(img_gray)
 #density_l=count/(ressfinal*ressfinal)
 #print("number white: ",count, "density: ",density_l)
            
 
 fnamee=dest +'%4.4d'%i+ '_smoothed.png'
 if destfile != None:
    fnamee=dest +'%4.4d'%destfile+ '_smoothed.png'
    print ("Writing file name with provided number: ",fnamee )
 cv2.imwrite(fnamee, img_gray)
            
 #names.append(fnamee)
 #density.append (density_l)
            
 #seed_=int(''.join(filter(str.isdigit, item)))
 #print (seed_)
            
 #seeds.append(seed_)
             


 return  

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
  