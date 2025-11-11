
import numpy as np
from PIL import Image
import cv2
from skimage import segmentation, filters, measure, morphology

def thresholding(img: Image.Image, thresh: int = 127) -> Image.Image:
	arr = np.array(img.convert('L'))
	_, seg = cv2.threshold(arr, thresh, 255, cv2.THRESH_BINARY)
	return Image.fromarray(seg)

def region_growing(img: Image.Image, seed=None, tolerance=10) -> Image.Image:
	arr = np.array(img.convert('L'))
	if seed is None:
		seed = (arr.shape[0]//2, arr.shape[1]//2)
	mask = np.zeros_like(arr, dtype=bool)
	value = arr[seed]
	stack = [seed]
	while stack:
		x, y = stack.pop()
		if mask[x, y]:
			continue
		mask[x, y] = True
		for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
			nx, ny = x+dx, y+dy
			if 0<=nx<arr.shape[0] and 0<=ny<arr.shape[1]:
				if not mask[nx, ny] and abs(int(arr[nx, ny])-int(value))<=tolerance:
					stack.append((nx, ny))
	seg = (mask*255).astype('uint8')
	return Image.fromarray(seg)

def watershed(img: Image.Image) -> Image.Image:
	arr = np.array(img.convert('L'))
	# Threshold
	_, binary = cv2.threshold(arr, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	# Distance transform
	dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
	ret, sure_fg = cv2.threshold(dist, 0.7*dist.max(), 255, 0)
	sure_fg = np.uint8(sure_fg)
	unknown = cv2.subtract(binary, sure_fg)
	# Marker labelling
	ret, markers = cv2.connectedComponents(sure_fg)
	markers = markers+1
	markers[unknown==255] = 0
	markers = cv2.watershed(cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR), markers)
	seg = np.zeros_like(arr)
	seg[markers > 1] = 255
	return Image.fromarray(seg)
