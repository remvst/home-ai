import logging
from datetime import datetime, timedelta
from time import sleep

import numpy
import peakutils
import pyaudio

RATE = 44100

MIN_SPIKE_INTERVAL = 0.1
MAX_SPIKE_INTERVAL = 0.5

MIN_SPIKE_VOLUME = 20000


def find_input_device(audio, search_string=None):
    device_index = None
    for i in xrange(audio.get_device_count()):
        device = audio.get_device_info_by_index(i)

        if device['name'] and search_string and search_string not in device['name']:
            continue

        if device['maxInputChannels'] == 0:
            continue

        return device

    return None

def wait_for_clap_clap(rate=44100, chunk_size=1024, device_search_string=None):
    audio = pyaudio.PyAudio()

    try:
        device = find_input_device(audio, device_search_string)
        if device is None:
            raise Exception('Unable to find input device')

        stream = audio.open(format=pyaudio.paInt16, channels=1,
                            rate=rate, input=True,
                            frames_per_buffer=chunk_size,
                            input_device_index=device['index'])

        last_spike = datetime.utcnow()
        spike_count = 0

        while True:
            data = stream.read(chunk_size, exception_on_overflow=False)

            signal = numpy.fromstring(data, 'Int16')

            peak = numpy.max(numpy.abs(signal)) * 2
            # bars="#"*int(50*peak/2**16)
            # print("%05d %s"%(peak,bars))

            if peak < MIN_SPIKE_VOLUME:
                continue

            now = datetime.utcnow()
            interval = now - last_spike
            last_spike = now

            if timedelta(seconds=MIN_SPIKE_INTERVAL) < interval < timedelta(seconds=MAX_SPIKE_INTERVAL):
                spike_count += 1
                if spike_count >= 3:
                    break
            else:
                spike_count = 0


        stream.stop_stream()
        stream.close()
    finally:
        audio.terminate()

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

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    while True:
        wait_for_clap_clap(device_search_string='Microsoft')
