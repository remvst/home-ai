from pocketsphinx import LiveSpeech

from bot.kik_bot import bot
from workers.speech import add_to_queue

print 'Initializing speech things'
speech = LiveSpeech(sampling_rate=16000, lm='assets/dictionary/8586.lm', dic='assets/dictionary/8586.dic', audio_device='0')
print 'Initialized speech things'

def worker():
    for phrase in speech:
        text = phrase.hypothesis()
        print text

        if 'please' not in text:
            continue

        if not bot.handle_text(text):
            add_to_queue('unrecognized command')
