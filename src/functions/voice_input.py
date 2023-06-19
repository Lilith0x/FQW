from PyQt5.QtCore import QThread, pyqtSignal
from vosk import Model, KaldiRecognizer
from json import loads
from pyaudio import PyAudio, paInt16


class VoiceInputThread(QThread):
    signal = pyqtSignal(list)
    handler_status = True

    model = Model("../models/voice_recognition_small_rus")
    # model = Model("..//models//voice_recognition_small_rus")
    rec = KaldiRecognizer(model, 16000)
    pA = PyAudio()
    stream = pA.open(format=paInt16, channels=1, rate=16000, input=True,
                     frames_per_buffer=8000)

    stream.start_stream()

    def run(self):

        while True:
            try:
                if self.handler_status:
                    try:
                        # stream.start_stream() - Попытка оптимизировать
                        data = VoiceInputThread.stream.read(4000, exception_on_overflow=False)
                        if VoiceInputThread.rec.AcceptWaveform(data) and len(data) > 0:
                            answer = loads(VoiceInputThread.rec.Result())['text']

                            self.signal.emit([1, answer])

                    except Exception as err:
                        self.signal.emit([-1, 'Ошибка распознавания. Попробуй проверить микрофон'])
                else:
                    break

            except Exception as err:

                self.signal.emit([-1, 'Ошибка распознавания. Попробуй проверить микрофон'])
                break
