import matplotlib.pyplot as plt
import numpy as np


def plot_components_or_sources(rows, columns, t, freq, visualize, order, name):

    fig, axs = plt.subplots(rows, 3, figsize=(12,5))
    plt.rcParams['font.family'] = 'Times New Roman' 
    plt.subplots_adjust(wspace=0.4, hspace=0.5)
    tam = 110

    for row in range(rows):
            if (row + 1) % 2 != 0:
                cor = 'red'
            else:
                cor = '#069AF3'
            axs[row][0].tick_params(axis='x', labelsize=10)  # Ajusta a fonte do eixo X

            # Para os números no eixo Y
            axs[row][0].tick_params(axis='y', labelsize=10)  # Ajusta a fonte do eixo Y
            axs[row][0].set_title( "Modal Coordinates {}".format(row + 1), fontsize = 10 )
            axs[row][0].set_xlabel("time(s)", fontsize = 10)
            axs[row][0].plot(t, visualize[:, order[row]], color=cor)

                
            aux = (np.abs(np.fft.fft(visualize[:, order[row]]))) ** 2
            indice_pico = np.argmax(aux[2:tam])
            freq_pico = float(freq[2:tam][indice_pico])
            
            axs[row][1].set_title( "Power spectral density {}".format(row + 1), fontsize = 10 )   
            axs[row][1].set_xlabel("Frequency (Hz)", fontsize = 10)
            axs[row][1].set_ylabel("Power", fontsize = 10)
            axs[row][1].plot(freq[2:tam], aux[2:tam], color = '#000000')
            axs[row][1].scatter(freq_pico, aux[2:tam][indice_pico], color='black', label = 'Hz: {:.2f}'.format(freq_pico,row) )  
            axs[row][1].legend()
            axs[row][1].tick_params(axis='x', labelsize=10)
            axs[row][1].tick_params(axis='y', labelsize=10)

            
            axs[row][2].set_title( "Phase", fontsize = 10)
            axs[row][2].set_xlabel("time(s)", fontsize = 10)
            axs[row][2].tick_params(axis='x', labelsize=10)
            axs[row][2].tick_params(axis='y', labelsize=10)
            aux = (np.angle(np.fft.fft(visualize[:, order[row]]))) ** 2
            axs[row][2].plot(freq[2:tam], aux[2:tam], color="#069AF3")
            print("Componente:{}, valor(hz):{:.4}".format(row, freq_pico))

    plt.savefig('figures/' + name)
    #plt.show()


def plot_mode_shapes_and_modal_coordinates(info, columns, t, do_unscramble):
    fig2, axs2 = plt.subplots(1, columns, figsize=((20, 10)))
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['font.family'] = 'Times New Roman' 
    for column in range(columns):
        if not do_unscramble:
            axs2[column].set_title("Mode shape: {}".format(column + 1), fontsize=22, fontname='Times New Roman')
            
            img = axs2[column].imshow(info.mode_shapes[:, column].reshape(info.video.frames_shape, order="F"), cmap='gray', aspect='auto')
            
            axs2[column].tick_params(axis='both', which='major', labelsize=22, labelfontfamily='Times New Roman') 

            cbar = fig2.colorbar(img, ax=axs2[column])
            cbar.ax.tick_params(labelsize=22)
            plt.savefig("figures/mode shapes and modal coordinates")

        else:
            axs2[column].set_title("Mode shape: {}".format(column + 1), fontsize=22, fontname='Times New Roman')

            mode_shape = info.mode_shapes[info.encryption_key, column]
            img = axs2[column].imshow(mode_shape.reshape(info.video.frames_shape, order="F"), 'gray', aspect='auto')
            axs2[column].tick_params(axis='both', which='major', labelsize=22, labelfontfamily='Times New Roman') 

            cbar = fig2.colorbar(img, ax=axs2[column])
            cbar.ax.tick_params(labelsize=22)
            plt.savefig("figures/mode_shapes_and_modal_coordinates_scramble")

    #plt.show()

