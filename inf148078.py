from pylab import *
from numpy import *
from ipywidgets import *
from playsound import playsound
from scipy.io import wavfile
import sys
from os import listdir
from os.path import isfile, join

HPS_ITERATIONS = 5
maleRange = [85, 155]
femaleRange = [165, 255]


def main(args):
    samplerate, data = readSound(args[1])
    hps = HarmonicProductSpectrum(samplerate, data)
    isMale = getGenderByHPS(hps)
    print(isMale)

def HarmonicProductSpectrum(samplerate, dataVoice):
    T_MAX = 3
    T = len(dataVoice) / samplerate
    samplerate = int(samplerate)

    if T > T_MAX:
        startSample = len(dataVoice) // 2 - T_MAX * samplerate // 2
        endSample = len(dataVoice) // 2 + T_MAX * samplerate // 2
        dataVoice = dataVoice[startSample:endSample]
        T = T_MAX

    windows = [dataVoice[i*samplerate:(i+1)*samplerate] for i in range(int(T))]
    windowResults = []
    for window in windows:
        if (len(window) == 0):
            continue

        fftOriginal = abs(fft.fft(window)) / samplerate
        fftHarmonic = copy(fftOriginal)
        for i in range(2, HPS_ITERATIONS):
            squeezed = copy(fftOriginal[::i])
            fftHarmonic = fftHarmonic[:len(squeezed)]
            fftHarmonic *= squeezed

        windowResults.append(fftHarmonic)

    result = np.zeros(len(windowResults[0]))
    for windowResult in windowResults:
        if (len(windowResult) != len(result)):
            continue
        result += windowResult
    return result


def readSound(filename):
    samplerate, data = wavfile.read(filename)
    dataShape = np.shape(data)
    if len(dataShape) > 1:
        data = data[:, 0]
    return samplerate, data


def getGenderByHPS(hpsResult):
    maleSum = sum(hpsResult[maleRange[0]:maleRange[1]])
    femaleSum = sum(hpsResult[femaleRange[0]:femaleRange[1]])

    if (maleSum > femaleSum):
        return 'M'
    else:
        return 'K'

if __name__ == '__main__':
    main(sys.argv)