import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = np.random.randint(0, 65535, size=(1000, 10000))
log_data = np.log10(data ** 2)
log_data = 10 * log_data
final_array = np.where(log_data < 13, 2*(log_data ** 2), log_data)
plt.imshow(final_array, interpolation='nearest')
plt.savefig('image_raster.png')
