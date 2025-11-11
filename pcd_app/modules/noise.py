
import numpy as np
from PIL import Image

def gaussian(img: Image.Image, mean=0, std=20) -> Image.Image:
	arr = np.array(img)
	noise = np.random.normal(mean, std, arr.shape)
	noisy = np.clip(arr + noise, 0, 255)
	return Image.fromarray(noisy.astype('uint8'))

def rayleigh(img: Image.Image, scale=30) -> Image.Image:
	arr = np.array(img)
	noise = np.random.rayleigh(scale, arr.shape)
	noisy = np.clip(arr + noise, 0, 255)
	return Image.fromarray(noisy.astype('uint8'))

def erlang(img: Image.Image, shape=2, scale=20) -> Image.Image:
	arr = np.array(img)
	noise = np.random.gamma(shape, scale, arr.shape)
	noisy = np.clip(arr + noise, 0, 255)
	return Image.fromarray(noisy.astype('uint8'))

def exponential(img: Image.Image, scale=30) -> Image.Image:
	arr = np.array(img)
	noise = np.random.exponential(scale, arr.shape)
	noisy = np.clip(arr + noise, 0, 255)
	return Image.fromarray(noisy.astype('uint8'))

def uniform(img: Image.Image, low=0, high=50) -> Image.Image:
	arr = np.array(img)
	noise = np.random.uniform(low, high, arr.shape)
	noisy = np.clip(arr + noise, 0, 255)
	return Image.fromarray(noisy.astype('uint8'))

def impulse(img: Image.Image, amount=0.05) -> Image.Image:
	arr = np.array(img)
	noisy = arr.copy()
	num_salt = np.ceil(amount * arr.size * 0.5)
	coords = [np.random.randint(0, i-1, int(num_salt)) for i in arr.shape]
	noisy[tuple(coords)] = 255
	num_pepper = np.ceil(amount * arr.size * 0.5)
	coords = [np.random.randint(0, i-1, int(num_pepper)) for i in arr.shape]
	noisy[tuple(coords)] = 0
	return Image.fromarray(noisy.astype('uint8'))
