import logging

import numpy
import peakutils
import pyaudio

RATE = 44100

MIN_SPIKE_INTERVAL = 0.1
MAX_SPIKE_INTERVAL = 0.5

MIN_SPIKE_INTERVAL_FRAMES = int(MIN_SPIKE_INTERVAL * RATE)
MAX_SPIKE_INTERVAL_FRAMES = int(MAX_SPIKE_INTERVAL * RATE)

MIN_SPIKE_VOLUME = 10000


def record_microphone(duration, rate=44100, chunk_size=1024):
    audio = pyaudio.PyAudio()

    input_device_index = None
    for i in xrange(audio.get_device_count()):
        device = audio.get_device_info_by_index(i)
        logging.debug(u'#{}: {} (input channels: {})'.format(i,device['name'],device['maxInputChannels']))

        if device['maxInputChannels'] > 0:
            input_device_index = i
            # break

    if input_device_index is None:
        logging.info('No input device')
        return None

    input_device = audio.get_device_info_by_index(input_device_index)
    logging.debug(u'Using {} as input device (#{})'.format(input_device['name'], input_device_index))

    stream = audio.open(format=pyaudio.paInt16, channels=1,
                        rate=rate, input=True,
                        frames_per_buffer=chunk_size,
                        input_device_index=input_device_index)

    frames = []
    for i in range(0, int(rate * duration), chunk_size):
        data = stream.read(chunk_size, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return numpy.fromstring(b''.join(frames), 'Int16')

def detect_volume_spikes(signal, min_interval, min_volume):
    indexes = peakutils.indexes(signal, thres=0.2, min_dist=MIN_SPIKE_INTERVAL_FRAMES)

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

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    while True:
        wait_for_clap_clap()
