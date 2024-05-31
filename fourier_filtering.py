import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import RangeSlider
from PIL import Image, ImageOps

IM_FILE = 'optical_resolution_test_chart.jpeg'

def filter_circle(max_dim, inner_radius, outer_radius):
    thickness = outer_radius - inner_radius
    xx, yy = np.mgrid[:max_dim, :max_dim]
    circle = (xx - max_dim/2) ** 2 + (yy - max_dim/2) ** 2
    donut = np.logical_and(circle < (outer_radius**2), circle > ((outer_radius - thickness)**2))
    return donut

def update(val):
    
    im = ImageOps.grayscale(Image.open(IM_FILE))
    dim = im.size[1]
    max_freq = dim * 1.5/2

    I = np.asarray(im)
    fft_exact = np.fft.fft2(I)
    fft_rep = np.log(np.abs(np.fft.fft2(I)))

    filt = filter_circle(dim,  val[0], val[1])

    fft_rep_shift_filt = np.fft.fftshift(fft_rep) * filt
    ax[0].imshow(fft_rep_shift_filt, cmap = "gray")

    fft_exact_filt = np.fft.fftshift(fft_exact)*filt
    filtered_image = np.real(np.fft.ifft2(np.fft.ifftshift(fft_exact_filt)))
    ax[1].imshow(filtered_image, cmap = "gray")
    fig.canvas.draw_idle()

im = ImageOps.grayscale(Image.open(IM_FILE))
dim = im.size[1]
max_freq = dim * 1.5/2

I = np.asarray(im)
fft_exact = np.fft.fft2(I)
fft_rep = np.log(np.abs(np.fft.fft2(I)))

filt = filter_circle(dim,  10, 500)
fig, ax = plt.subplots(1, 2, figsize = (10, 5))
fig.subplots_adjust(bottom = 0.25)

fft_rep_shift_filt = np.fft.fftshift(fft_rep) * filt
image = ax[0].imshow(fft_rep_shift_filt, cmap = "gray")

fft_exact_filt = np.fft.fftshift(fft_exact)*filt
filtered_image = np.real(np.fft.ifft2(np.fft.ifftshift(fft_exact_filt)))
image_2 = ax[1].imshow(filtered_image, cmap = "gray")

slider_ax = fig.add_axes([0.20, 0.1, 0.60, 0.03])
slider = RangeSlider(slider_ax, "Frequencies", 0, int(round(max_freq)))


slider.on_changed(update)
plt.show()