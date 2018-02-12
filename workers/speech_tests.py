from pocketsphinx import LiveSpeech

from bot.kik_bot import bot


speech = LiveSpeech(sampling_rate=16000, lm='9891.lm', dic='9891.dic')

def worker():
    for phrase in speech:
        text = phrase.hypothesis()
        print text

        if 'please' not in text:
            continue

        bot.handle_text(text)
