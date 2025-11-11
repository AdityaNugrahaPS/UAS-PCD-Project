import numpy as np
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
from io import BytesIO

def negative(img: Image.Image) -> Image.Image:
    arr = np.array(img)
    neg = 255 - arr
    return Image.fromarray(neg.astype('uint8'))

def arithmetic(img: Image.Image, value: int, op: str) -> Image.Image:
    arr = np.array(img, dtype=np.int32)
    if op == 'add':
        arr = np.clip(arr + value, 0, 255)
    elif op == 'subtract':
        arr = np.clip(arr - value, 0, 255)
    elif op == 'multiply':
        arr = np.clip(arr * value, 0, 255)
    elif op == 'divide':
        arr = np.clip(arr // max(value,1), 0, 255)
    return Image.fromarray(arr.astype('uint8'))

def boolean(img: Image.Image, value: int, op: str) -> Image.Image:
    arr = np.array(img, dtype=np.uint8)
    if op == 'not':
        arr = np.bitwise_not(arr)
    elif op == 'and':
        arr = np.bitwise_and(arr, value)
    elif op == 'or':
        arr = np.bitwise_or(arr, value)
    elif op == 'xor':
        arr = np.bitwise_xor(arr, value)
    return Image.fromarray(arr.astype('uint8'))

def geom_translate(img: Image.Image, dx: int, dy: int) -> Image.Image:
    arr = np.array(img)
    result = np.roll(arr, shift=(dy, dx), axis=(0, 1))
    return Image.fromarray(result)

def geom_rotate(img: Image.Image, angle: float) -> Image.Image:
    return img.rotate(angle, expand=True)

def geom_zoom(img: Image.Image, scale: float) -> Image.Image:
    w, h = img.size
    return img.resize((int(w*scale), int(h*scale)), Image.Resampling.LANCZOS)

def geom_flip(img: Image.Image, mode: str) -> Image.Image:
    if mode == 'horizontal':
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    elif mode == 'vertical':
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    return img

def geom_crop(img: Image.Image, box: tuple) -> Image.Image:
    return img.crop(box)

def thresholding(img: Image.Image, thresh: int) -> Image.Image:
    arr = np.array(img.convert('L'))
    arr = np.where(arr > thresh, 255, 0)
    return Image.fromarray(arr.astype('uint8')).convert('RGB')

def convolution(img: Image.Image, kernel: np.ndarray) -> Image.Image:
    from scipy.ndimage import convolve
    arr = np.array(img.convert('L'))
    result = convolve(arr, kernel, mode='reflect')
    return Image.fromarray(np.clip(result,0,255).astype('uint8')).convert('RGB')

def fourier_transform(img: Image.Image) -> Image.Image:
    arr = np.array(img.convert('L'))
    f = np.fft.fft2(arr)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift)+1)
    plt.figure(figsize=(5,4))
    plt.axis('off')
    plt.imshow(magnitude_spectrum, cmap='gray')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buf.seek(0)
    return Image.open(buf)

def colouring(img: Image.Image, mode: str) -> Image.Image:
    if mode == 'binary':
        arr = np.array(img.convert('L'))
        arr = np.where(arr > 127, 255, 0)
        return Image.fromarray(arr.astype('uint8')).convert('RGB')
    elif mode == 'grayscale':
        return img.convert('L').convert('RGB')
    elif mode == 'rgb':
        return img.convert('RGB')
    elif mode == 'hsv':
        return img.convert('HSV').convert('RGB')
    elif mode == 'cmy':
        arr = 255 - np.array(img.convert('RGB'))
        return Image.fromarray(arr.astype('uint8'))
    elif mode == 'yuv':
        from skimage.color import rgb2yuv
        arr = np.array(img.convert('RGB'))/255.0
        yuv = rgb2yuv(arr)
        yuv = (yuv*255).astype('uint8')
        return Image.fromarray(yuv, 'RGB')
    elif mode == 'yiq':
        from skimage.color import rgb2yiq
        arr = np.array(img.convert('RGB'))/255.0
        yiq = rgb2yiq(arr)
        yiq = (yiq*255).astype('uint8')
        return Image.fromarray(yiq, 'RGB')
    elif mode == 'pseudo':
        arr = np.array(img.convert('L'))
        pseudo = np.zeros((arr.shape[0], arr.shape[1], 3), dtype='uint8')
        pseudo[...,0] = arr
        pseudo[...,1] = 255-arr
        pseudo[...,2] = arr//2
        return Image.fromarray(pseudo)
    return img
