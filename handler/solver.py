#!/usr/bin/env python
# coding=utf-8

import cv2
from filematcher import file_filter

class detector(object):
    def __init__(self,file):
        self.classifer = cv2.CascadeClassifier(file)
        
    def detect(self,img):
        return self.classifer.detectMultiScale(img,scaleFactor=1.1)
        
class shape(object):
    def __init__(self,area):
        self.area = area
        self.mouth = []
        self.nose = []

    def fall_in(self,area,lower=False):
        option = True
        if(lower):
            option = self.area[1]+self.area[3]*0.5 <= area[1]
        return option and self.area[0] <= area[0] and self.area[1] <= area[1] and self.area[0] + self.area[2] >= area[0] + area[2] and self.area[1] + self.area[3] >= area[1] + area[3]
        
    def get_best(self):
        if(len(self.mouth) > 0 and len(self.nose) > 0):
            width = self.mouth[0][2]*1.8
            height = 10
            x = self.nose[0][0] + self.nose[0][2]*0.5 - 0.5*width
            t = 0.5*(self.nose[0][1] + self.mouth[0][1])+0.25*(self.nose[0][3] + self.mouth[0][3])
            y = t - 0.5*height
            return int(x),int(y),int(width),int(height)
        elif(len(self.mouth) > 0):
            width = self.mouth[0][2]*1.8
            height = 10
            x = self.mouth[0][0] - 0.4*self.mouth[0][2]
            y = self.mouth[0][1] - 0.5*height
            return int(x),int(y),int(width),int(height)
            
        elif(len(self.nose) > 0):
            width = self.nose[0][2]*1.8
            height = 10
            x = self.nose[0][0] - 0.4*self.nose[0][2]
            y = self.nose[0][1] + 0.5*height
            return int(x),int(y),int(width),int(height)

# draw util functions
def draw(img,rects,color):
    for x,y,w,h in rects:
        cv2.rectangle(img,(x,y),(x+w,y+h),color,1)
    cv2.imshow('ff',img)

def draw_one(img,rect,color):
    if rect == None:
        return
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    cv2.rectangle(img,(x,y),(x+w,y+h),color,1)
    cv2.imshow('ff',img)

class Solver(object):
    def __init__(self,test=False):
        if(not test): 
            self.face_dector = detector('xml/haarcascade_frontalface_alt.xml')
            self.mouth_dector = detector('xml/haarcascade_mcs_mouth.xml')
            self.nose_dector = detector('xml/haarcascade_mcs_nose.xml')
        else:
            self.face_dector = detector('../xml/haarcascade_frontalface_alt.xml')
            self.mouth_dector = detector('../xml/haarcascade_mcs_mouth.xml')
            self.nose_dector = detector('../xml/haarcascade_mcs_nose.xml')


    def objects_filter(self,faces,parts,name='mouth'):
        for face in faces:
            for part in parts:
                if face.fall_in(part,lower=True):
                    #print part,' in ',face.area
                    if(name == 'mouth'):
                        face.mouth.append(part)
                    else:
                        face.nose.append(part)
    def solve(self,img):
        mouths = self.mouth_dector.detect(img)
        faces = self.face_dector.detect(img)
        noses = self.nose_dector.detect(img)
        #cp = img.copy()
        #draw(cp,faces,(0,255,255))
        #draw(cp,mouths,(0,255,255))
        
        all_faces = []
        for face in faces:
            all_faces.append(shape(face))
            #print 'face:', face
        
        self.objects_filter(all_faces,mouths,name='mouth')
        self.objects_filter(all_faces,noses,name='nose')
        
        for x in all_faces:
            if(len(x.mouth) > 0 or len(x.nose) > 0):
                #draw_one(cp,x.area,(0,255,0))
                #draw(cp,x.mouth,(0,0,255))
                #draw(cp,x.nose,(255,0,0))
                t = x.get_best()
                #draw_one(cp,t,(20,05,30))
                #cv2.waitKey(0)
                return t

        
"""
dct = {}
for face in ll:
    for mouth in mouths:
        if face.fall_in(mouth,lower=False):
            print mouth,' in ',face.area
            if(not dct.has_key(face)):
                dct[face] = []
            dct[face].append(mouth)

for k,v in dct.iteritems():
    print type(k.area),k.area
    draw_one(cp,k.area,(255,0,0))
    draw(cp,v,(0,0,255))
cv2.waitKey(0)
"""
if __name__ == "__main__":
    file = file_filter('../xx',['jpg'])
    solver = Solver(test=True)
    for name,format in file:
        print name
        #image = Image.open(name)
        #cv_image = np.array(image)
        cv_image = cv2.imread(name)
        print solver.solve(cv_image)
                    
