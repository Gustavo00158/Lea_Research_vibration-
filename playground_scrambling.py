import matplotlib.pyplot as plt
import numpy as np
import scipy.io

from video_processing import Video, Video_Magnification
from video_processing import h5py_tools as ht

video_path = 'video_samples/Vid_btm/yuri_10_09.mp4'
number_components = 70
components_order = np.arange(number_components)
sources_order = np.arange(number_components)
# modal_coordinates_order = np.array([8, 9, 2, 3, 11, 12])
modal_coordinates_order = np.array([52,53])

# set the video object
video = Video(video_path)

# Start video magnification
video_magnification = Video_Magnification(video) # passa como um obj o video 
video_magnification.create_video_from_frames("frames_gray", frames=video.gray_frames) # cria um video em escala cinza

# Create time series
time_serie = video_magnification.create_time_series() # cria a serie temporal normal
'''
aqui criamos o processo para dividir a serie temporal 


time(frames, pixels) = [x,y]; exemplo: [200, 1.000.000]


'''
# Scrambling time serie
encryption_key = video_magnification.scramble()  # cria a imagem com o scramble 

# Remove background
video_magnification.remove_background()

# Hibert Transform
real_time_serie, imag_time_serie = video_magnification.apply_hilbert_transform()

# dimension reduction in the real and imaginary time series
eigen_vectors, eigen_values, components = video_magnification.dimension_reduction()

# blind source separation
mixture_matrix, sources = video_magnification.extract_sources(number_components)

# create mode shapes and modal coordinates
mode_shapes, modal_coordinates = video_magnification.create_mode_shapes_and_modal_coordinates(number_components,
                                                                                              modal_coordinates_order)

# vizualize principal components
video_magnification.visualize_components_or_sources('components', components_order)

# visualize sources
video_magnification.visualize_components_or_sources('sources', sources_order)

# visualize mode shapes without scrambling
video_magnification.visualize_mode_shapes_and_modal_coordinates(modal_coordinates_order, do_unscramble=True)

# visualize modal coordinates and mode shapes
video_magnification.visualize_mode_shapes_and_modal_coordinates(modal_coordinates_order)

# visualize only modal coordinates
video_magnification.visualize_components_or_sources('modal coordinates', np.arange(len(modal_coordinates_order)))

# video reconstruction
frames_0, frames_1 = video_magnification.video_reconstruction(number_of_modes=1, factors=[10], do_unscramble=False)
video_magnification.create_video_from_frames("mode0_U", frames=frames_0)
video_magnification.create_video_from_frames("mode1_U", frames=frames_1)


# video reconstruction
frames_0, frames_1 = video_magnification.video_reconstruction(number_of_modes=1, factors=[10], do_unscramble=True)
video_magnification.create_video_from_frames("mode0", frames=frames_0)
video_magnification.create_video_from_frames("mode1", frames=frames_1)


# Calculate error
'''error, norm = video_magnification.calculate_error()'''

ht.Vetor_save(modal_coordinates[:,0], '_[52]_70_comp', 'modal_coordinate/costa/')
ht.Vetor_save(modal_coordinates[:,1], '_[53]_70_comp', 'modal_coordinate/costa/')
