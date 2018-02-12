from pocketsphinx import LiveSpeech

from bot.kik_bot import bot

def worker():
    speech = LiveSpeech(sampling_rate=16000)

    for phrase in speech:
        text = phrase.hypothesis()
        print text

        if 'please' not in text:
            continue

        bot.handle_text(text)
