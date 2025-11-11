
import numpy as np
from PIL import Image
import cv2
from skimage import filters

def sobel(img: Image.Image) -> Image.Image:
	arr = np.array(img.convert('L'))
	edge = filters.sobel(arr)
	edge = (edge * 255).astype('uint8')
	return Image.fromarray(edge)

def prewitt(img: Image.Image) -> Image.Image:
	arr = np.array(img.convert('L'))
	edge = filters.prewitt(arr)
	edge = (edge * 255).astype('uint8')
	return Image.fromarray(edge)

def roberts(img: Image.Image) -> Image.Image:
	arr = np.array(img.convert('L'))
	edge = filters.roberts(arr)
	edge = (edge * 255).astype('uint8')
	return Image.fromarray(edge)

def laplacian(img: Image.Image) -> Image.Image:
	arr = np.array(img.convert('L'))
	edge = cv2.Laplacian(arr, cv2.CV_64F)
	edge = np.absolute(edge)
	edge = np.clip(edge, 0, 255).astype('uint8')
	return Image.fromarray(edge)

def log(img: Image.Image) -> Image.Image:
	arr = np.array(img.convert('L'))
	blur = cv2.GaussianBlur(arr, (3,3), 0)
	edge = cv2.Laplacian(blur, cv2.CV_64F)
	edge = np.absolute(edge)
	edge = np.clip(edge, 0, 255).astype('uint8')
	return Image.fromarray(edge)

def canny(img: Image.Image) -> Image.Image:
	arr = np.array(img.convert('L'))
	edge = cv2.Canny(arr, 100, 200)
	return Image.fromarray(edge)

def compass(img: Image.Image) -> Image.Image:
	arr = np.array(img.convert('L'))
	# Kirsch compass kernels
	kernels = [
		np.array([[5,5,5],[-3,0,-3],[-3,-3,-3]]),
		np.array([[-3,5,5],[-3,0,5],[-3,-3,-3]]),
		np.array([[-3,-3,5],[-3,0,5],[-3,-3,5]]),
		np.array([[-3,-3,-3],[-3,0,5],[-3,5,5]]),
		np.array([[-3,-3,-3],[-3,0,-3],[5,5,5]]),
		np.array([[-3,-3,-3],[5,0,-3],[5,5,-3]]),
		np.array([[5,-3,-3],[5,0,-3],[5,-3,-3]]),
		np.array([[5,5,-3],[5,0,-3],[-3,-3,-3]])
	]
	responses = [cv2.filter2D(arr, -1, k) for k in kernels]
	edge = np.max(responses, axis=0)
	edge = np.clip(edge, 0, 255).astype('uint8')
	return Image.fromarray(edge)
