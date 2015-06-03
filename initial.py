from PIL import Image
import ImageEnhance
import ImageFilter
import ImageOps,ImageChops
import scipy
import numpy as np
from scipy import ndimage
from scipy.misc import imsave
from numpy import ndarray
import matplotlib.pyplot as plt

'''Notations used
   imw= image width
   imh= image height
   im.size[0] gives width of image
   im.size[1] gives height of image
'''

#function to darken the horizontal strip from pixel y1 to y2
def darkenHStrip(img,y1,y2):
 imn=img.copy()
 imw=img.size[0]
 for i in range(y1,y2):
   for j in range(1,imw):
     imn.putpixel((j,i),0)
 imn.show()


def Resize(img , bw):
 wpercent = (bw/ float(img.size[0]))
 hsize = int((float(img.size[1]) * float(wpercent)))
 img = img.resize((bw, hsize), Image.ANTIALIAS)
 return img

#binarization of image using global thresholding
def GBinarization(im):
  imw= im.size[0]
  imh= im.size[1]
  hs=im.histogram()
  th=0
  for i in range(len(hs)):
   th+=i*int(hs[i])
  th=th/(imw*imh)
  th+=10
  im = im.point(lambda i: i < th and 255)
  return im


#binarization of image using Local thresholding
def LBinarization(im):
  imw= im.size[0]
  imh= im.size[1]
  pix=im.load()
  winw=10
  winh=10
  x=0 
  y=0
  while(x <= (imh-winh)):
    print x
    y=0
    while(y<= (imw-winw)):
         th=0
         for i in range(x,x+winh):
            for j in range(y,y+winw):
               th+= pix[j,i]
         th=th/(winw*winh)
         #th=max(0,th-30) 
         for i in range(x,x+winh):
            for j in range(y,y+winw):
               if pix[j,i]<(th-10):
                  im.putpixel((j,i),0)
               else:
                  im.putpixel((j,i),255)
         y+=winw
    x+=winh
  return im 


def Process(i):
 src="cars/EX"+str(i)+".jpg"
 im = Image.open(src)
 im=Resize(im,600)
  
 im=im.convert('L') #converts image into grayscale
 
 im1 = ndimage.grey_erosion(im, size=(15,15))
 scipy.misc.imsave("eroded.jpg",im1)
 im1= Image.open("eroded.jpg")
 im=ImageOps.equalize(im,0)
 im=ImageChops.difference(im1, im)
 imw= im.size[0]
 imh= im.size[1]
 print ("image height %d and width %d\n"%(imh,imw))
 
 #im=LBinarization(im)#binarize the image
 im=GBinarization(im)
 #making a copy our original image
 new=im.copy()
 new.show()
 pix=new.load()


 #storing the values of disturbence along width for each row in array a[i]
 a = ndarray((imh+1,),int)
 a[0]=0
 maxm=0
 x=0
 for i in range(1,imh):
  a[i]=0;
  for j in range(1,imw-1):
     if pix[j,i]!=pix[j+1,i]:
 	a[i]+=1;
  if maxm<a[i]:
    maxm=a[i]
  #print a[i] 
 #print maxm
 a[imh]=0
 mean=sum(a)/imh
 print mean
 print max(a)
 

 #finding the most probable value of disturbence
 arr = ndarray((maxm+1,),int)
 for i in range(1,maxm+1):
    arr[i]=0
 for i in range(i,imh):
    arr[a[i]]+=1
 #for i in range(1,maxm+1):
    #print ("%d : %d"%(i,arr[i]))
 

 for i in range(1,imh):
       if a[i]<(max(a)) and a[i]>mean:
          for  k in range(1,imw):
             new.putpixel((k,i),0)
       print ("%d = %d"%(i,a[i]))
 new.show()
 
 
 xarr = ndarray((imh+1,),int)
 for i in range(1,imh):
   xarr[i]=i
 plt.xlabel(src)
 plt.plot(xarr,list(a))
 plt.axis([0,imh,0,maxm])
 plt.show()
 #darkenHStrip(im,250,300)
 

 








