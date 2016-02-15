"""
    This is an example of application using
    the tools from this package. It's a ticket-
    by-voice purchase app.

    The Recorder class was used to store the wav
    samples in /audio_files which composes the data
    for new input signals to be compared with here.
"""
import scikits.audiolab as audio
from Recorder import Recorder
from Recognizer import Recognizer
from os import environ

# setting .wav's directory
wav_directory = environ.get("HOME") + "/speech-recognition/audio_files/"

audio_base = range(6)
audio_base[0] = {
    "comprar_ingresso": audio.wavread(wav_directory + 'comprar_ingresso.wav')[0],
    "sair": audio.wavread(wav_directory + 'sair.wav')[0]
}
audio_base[1] = {
    "meia": audio.wavread(wav_directory + 'meia.wav')[0],
    "inteira": audio.wavread(wav_directory + 'inteira.wav')[0],
}
audio_base[2] = {
    "um": audio.wavread(wav_directory + 'um.wav')[0],
    "dois": audio.wavread(wav_directory + 'dois.wav')[0],
}
audio_base[3] = {
    "matrix": audio.wavread(wav_directory + 'matrix.wav')[0],
    "braveheart": audio.wavread(wav_directory + 'braveheart.wav')[0],
    "constantine": audio.wavread(wav_directory + 'constantine.wav')[0],
}
audio_base[4] = {
    "dinheiro": audio.wavread(wav_directory + 'dinheiro.wav')[0],
    "cartao": audio.wavread(wav_directory + 'cartao.wav')[0],
}
audio_base[5] = {
    "finalizar_compra": audio.wavread(wav_directory + 'finalizar_compra.wav')[0],
    "sair": audio.wavread(wav_directory + 'sair.wav')[0],
}

if __name__ == "__main__":
    for i in range(6):
        recorder = Recorder()
        recognizer = Recognizer()

        recorder.record(time_to_run=2)
        (input_signal1, sampling_rate1, bits1) = audio.wavread('record.wav')
        Recognizer.test_audio(audio_base[i], input_signal1, wav_directory)

    fs = sampling_rate1
    lowcut = 300
    highcut = 3400
