import cv2
import numpy as np
img = cv2.imread('xy.jpg')

mask = cv2.imread('b.png')
roi = img[20:20+mask.shape[0],200:200+mask.shape[1]]
roi = 0.8*mask + 0.2*roi
#res = cv2.bitwise_and(roi,roi,mask = mask)
#vis = np.concatenate((roi, mask), axis=1)
#cv2.imwrite('out.png', vis)
cv2.imshow('ff',img)
cv2.waitKey(0)
