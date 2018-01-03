import numpy
import peakutils
import pyaudio

RATE = 44100

MIN_SPIKE_INTERVAL = 0.1
MAX_SPIKE_INTERVAL = 0.5

MIN_SPIKE_INTERVAL_FRAMES = int(MIN_SPIKE_INTERVAL * RATE)
MAX_SPIKE_INTERVAL_FRAMES = int(MAX_SPIKE_INTERVAL * RATE)

MIN_SPIKE_VOLUME = 20000


def record_microphone(duration, rate=44100, chunk_size=1024):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16, channels=1,
                        rate=rate, input=True,
                        frames_per_buffer=chunk_size,
                        input_device_index=1)

    frames = []
    for i in range(0, int(rate * duration), chunk_size):
        data = stream.read(chunk_size, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return numpy.fromstring(b''.join(frames), 'Int16')

def detect_volume_spikes(signal, min_interval, min_volume):
    indexes = peakutils.indexes(signal, thres=0.8, min_dist=MIN_SPIKE_INTERVAL_FRAMES)

    print indexes

    return [index for index in indexes if signal[index] > min_volume]

def contains_clap_clap(spike_indexes, max_spike_interval):
    intervals = []

    for i in xrange(1, len(spike_indexes)):
        previous_spike_index = spike_indexes[i - 1]
        current_spike_index = spike_indexes[i]

        intervals.append(current_spike_index - previous_spike_index)

    if len(intervals) == 0:
        return False

    return min(intervals) < max_spike_interval

def wait_for_clap_clap():
    while True:
        signal = record_microphone(duration=1, rate=RATE)

        spike_indexes = detect_volume_spikes(signal, min_interval=MIN_SPIKE_INTERVAL_FRAMES, min_volume=MIN_SPIKE_VOLUME)

        if contains_clap_clap(spike_indexes, MAX_SPIKE_INTERVAL_FRAMES):
            break

        print 'noclap'

while True:
    wait_for_clap_clap()
    print 'clap clap!'
    break
