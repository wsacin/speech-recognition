from copy import deepcopy
import matplotlib.pyplot as plt
import numpy
import scipy
from filters import butter_bandstop_filter


class Recognizer:
    def __init__(self):
        pass

    def __make_graph(self, data1, data2, filename):
        """
        Plots graph with signal from the base of records
        and the signal just recorded.
        """
        plt.plot(data1, label='Sinal+ruido,Tempo')
        plt.plot(data2, label='Sinal2+ruido,Tempo')
        plt.legend(loc='upper left')
        plt.savefig(filename)
        plt.clf()

    def __mean_signal(self, input_signal, ran=20):
        """

	    Function for smoothing signals.
        Given the input "ran", each "input_signal" in ran's index
        will recive the highest value of the "input_signal"
        """
        i = 0
        signal = deepcopy(input_signal)
        while i+ran < len(signal):
            max_on_index = max(signal[i:i+ran])
            for j in range(ran):
                signal[i+j] = max_on_index
            i += ran
        return signal

    def __best_position_freq(self, signal1, signal2):
        """
        Compare signal1 and signal2 and return the best value.
        The best value is the correlation between signal1 e signal2.
        """
        best_pos_left = (0,0)
        best_pos_right = (0,0)

        for i in range(0,400)[::50]:
            oh_list = [] if i==0 else [0 for j in range(i)]
            corr_left = scipy.stats.pearsonr(signal1, signal2[i:] + oh_list)
            if i == 0:
                corr_right = scipy.stats.pearsonr(signal1, signal2)
            else:
                corr_right = scipy.stats.pearsonr(signal1, oh_list + signal2[:-i])
            best_pos_left = (i,corr_left) if corr_right > best_pos_left[1] else best_pos_left
            best_pos_right = (i,corr_right) if corr_right > best_pos_right[1] else best_pos_right

        best_pos = best_pos_left if best_pos_left[1] > best_pos_right[1] else best_pos_right

        return best_pos

    def test_audio(self, audio_base_pos, input_signal1, wav_directory):
        """
        Filters, normalize and make the correlation on the input_signal with the 
        dictionary of audios.
        """
        cor_res = ("", 20)
        for key,input_signal2 in audio_base_pos.items():
            freq1, freq2 = numpy.fft.rfft(input_signal1), numpy.fft.rfft(input_signal2)

            filtered_signal1 = abs(butter_bandstop_filter(freq1, 300, 3400, 8000, order=6))
            filtered_signal2 = abs(butter_bandstop_filter(freq2, 300, 3400, 8000, order=6))

            mean1 = self.__mean_signal(filtered_signal1)
            mean2 = self.__mean_signal(filtered_signal2)
            max1 = max(mean1)
            max2 = max(mean2)
            factor = (max1+max2)/2
            norm1 = [(m1*factor)/max1 for m1 in mean1]
            norm2 = [(m2*factor)/max2 for m2 in mean2]

            self.__make_graph(filtered_signal1,
                              filtered_signal2,
                              wav_directory + "graficos/" + str(key) + "_filt_proc_time.png")

            freqnorm1, freqnorm2 = norm1, norm2

            pos, corr_value = self.__best_position_freq(freqnorm1[300:3000],freqnorm2[300:3000])

            if cor_res[1] < corr_value:
                cor_res = (key, corr_value)

        return cor_res
