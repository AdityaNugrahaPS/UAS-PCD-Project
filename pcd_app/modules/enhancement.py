
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2
from skimage import exposure

def brightness(img: Image.Image, factor: float) -> Image.Image:
	enhancer = ImageEnhance.Brightness(img)
	return enhancer.enhance(factor)

def contrast(img: Image.Image, factor: float) -> Image.Image:
	enhancer = ImageEnhance.Contrast(img)
	return enhancer.enhance(factor)

def histogram_equalization(img: Image.Image) -> Image.Image:
	arr = np.array(img.convert('L'))
	eq = exposure.equalize_hist(arr)
	eq = (eq * 255).astype('uint8')
	return Image.fromarray(eq).convert('RGB')

def smoothing_spatial(img: Image.Image) -> Image.Image:
	return img.filter(ImageFilter.GaussianBlur(radius=2))

def smoothing_frequency(img: Image.Image) -> Image.Image:
	arr = np.array(img.convert('L'))
	f = np.fft.fft2(arr)
	fshift = np.fft.fftshift(f)
	rows, cols = arr.shape
	crow, ccol = rows//2, cols//2
	mask = np.zeros((rows, cols), np.uint8)
	r = 30
	mask[crow-r:crow+r, ccol-r:ccol+r] = 1
	fshift = fshift * mask
	f_ishift = np.fft.ifftshift(fshift)
	img_back = np.fft.ifft2(f_ishift)
	img_back = np.abs(img_back)
	return Image.fromarray(np.clip(img_back,0,255).astype('uint8')).convert('RGB')

def sharpening_spatial(img: Image.Image) -> Image.Image:
	kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
	return img.filter(ImageFilter.Kernel((3,3), kernel.flatten(), 1, 0))

def sharpening_frequency(img: Image.Image) -> Image.Image:
	arr = np.array(img.convert('L'))
	f = np.fft.fft2(arr)
	fshift = np.fft.fftshift(f)
	rows, cols = arr.shape
	crow, ccol = rows//2, cols//2
	mask = np.ones((rows, cols), np.uint8)
	r = 30
	mask[crow-r:crow+r, ccol-r:ccol+r] = 0
	fshift = fshift * mask
	f_ishift = np.fft.ifftshift(fshift)
	img_back = np.fft.ifft2(f_ishift)
	img_back = np.abs(img_back)
	return Image.fromarray(np.clip(img_back,0,255).astype('uint8')).convert('RGB')

def geometric_correction(img: Image.Image) -> Image.Image:
	# Example: simple affine transform (identity)
	return img
