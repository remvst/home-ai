from pocketsphinx import LiveSpeech

from bot.kik_bot import bot


speech = LiveSpeech(sampling_rate=16000, lm='assets/dictionary/8586.lm', dic='assets/dictionary/8586.dic', audio_device='0')

def worker():
    for phrase in speech:
        text = phrase.hypothesis()
        print text

        if 'please' not in text:
            continue

        bot.handle_text(text)
