from PyQt5 import QtCore
import torch
import sounddevice as sd
import time


class VoiceAssistantThread(QtCore.QThread):
    language = 'ru'
    model_id = 'ru_v3'
    sample_rate = 48000  # 48000
    speaker = 'xenia'  # aidar, baya, kseniya, xenia, random
    put_accent = True
    put_yo = True
    device = torch.device('cpu')  # cpu или gpu
    # text = "Хауди Хо, друзья!!!"
    model, _ = torch.hub.load(repo_or_dir='../models/snakers4_silero-models_master',
                                   model='silero_tts',
                                   source='local',
                                   language=language,
                                   speaker=model_id)
    model.to(device)

    def __init__(self):
        super(VoiceAssistantThread, self).__init__()
        self.audio = VoiceAssistantThread.model.apply_tts(text="начинаем",
                                                     speaker=VoiceAssistantThread.speaker,
                                                     sample_rate=VoiceAssistantThread.sample_rate,
                                                     put_accent=VoiceAssistantThread.put_accent,
                                                     put_yo=VoiceAssistantThread.put_yo)

    def set_text_say(self, text):
        self.audio = VoiceAssistantThread.model.apply_tts(text=text + "..",
                                                          speaker=VoiceAssistantThread.speaker,
                                                     sample_rate=VoiceAssistantThread.sample_rate,
                                                     put_accent=VoiceAssistantThread.put_accent,
                                                     put_yo=VoiceAssistantThread.put_yo)

    # воспроизводим
    def run(self):
        sd.play(self.audio, VoiceAssistantThread.sample_rate * 1.05)
        time.sleep((len(self.audio) / VoiceAssistantThread.sample_rate) + 0.5)
        sd.stop()
        self.audio = None

#     def test(self):
#         sd.play(self.audio, VoiceAssistantThread.sample_rate * 1.05)
#         time.sleep((len(self.audio) / VoiceAssistantThread.sample_rate) + 0.5)
#         sd.stop()
#         self.audio = None
#
#
# test = VoiceAssistantThread()
# test.set_text_say('проверка')
# test.test()