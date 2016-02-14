import alsaaudio, wave, numpy
import os


class Recorder:
    def __init__(self):
        pass

    def __data_to_record(self, sampling_rate=8000, period_size=256, wav_title="record.wav"):
        self.__inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
        self.__inp.setchannels(1)
        self.__inp.setrate(sampling_rate)
        self.__inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.__inp.setperiodsize(period_size)

        self.__w = wave.open(wav_title, 'w')
        self.__w.setnchannels(1)
        self.__w.setsampwidth(2)
        self.__w.setframerate(sampling_rate)

    def record(self, time_to_run=2, args=[]):
        if len(args) > 1:
            self.__data_to_record(wav_title=str(args[2]) + ".wav")
        else:
            self.__data_to_record()

        beginning = os.times()[4]
        while beginning + time_to_run > os.times()[4]:
            l, data = self.__inp.read()
            a = numpy.fromstring(data, dtype='int16')
            self.__w.writeframes(data)

            print("_time elapsed: " + str(os.times()[4] - beginning) + " seconds")
