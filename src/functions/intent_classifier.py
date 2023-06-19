import pickle
import numpy as np
from re import sub

from tensorflow.python.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk import word_tokenize
from nltk.corpus import stopwords


class IntentClassifier:
    def __init__(self):
        self.classes = pickle.load(open('../models/intent_classifier/classes_CNN.pkl', 'rb'))
        self.tokenizer = pickle.load(open('../models/intent_classifier/tokenizer_CNN.pkl', 'rb'))
        self.label_encoder = pickle.load(open('../models/intent_classifier/label_encoder_CNN.pkl', 'rb'))
        self.classifier = load_model('../models/intent_classifier/intents.h5')


        # для запуска данного файла
        # self.classes = pickle.load(open('../../models/intent_classifier/classes_CNN.pkl', 'rb'))
        # self.tokenizer = pickle.load(open('../../models/intent_classifier/tokenizer_CNN.pkl', 'rb'))
        # self.label_encoder = pickle.load(open('../../models/intent_classifier/label_encoder_CNN.pkl', 'rb'))
        # self.classifier = load_model('../../models/intent_classifier/intents.h5')

    def get_intent(self,text):
        self.text = [text]
        self.test_keras = self.tokenizer.texts_to_sequences(self.text)
        self.test_keras_sequence = pad_sequences(self.test_keras, maxlen=16, padding='post')
        self.pred = self.classifier.predict(self.test_keras_sequence)

        return self.label_encoder.inverse_transform(np.argmax(self.pred,1))[0]


    def clear_text(self,text: str):
        text = text.lower()
        text = sub(r'[^а-яА-ЯёЁ ]', ' ', text)
        text = ' '.join(text.split())

        word_tokens = word_tokenize(text)
        stop_words = set(stopwords.words("russian"))

        new_stop_words = ['пожалуйста', 'вирта']

        for i in new_stop_words:
            stop_words.add(i)

        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        text = ' '.join(filtered_sentence)

        return text

#nlu = IntentClassifier()
#print(nlu.clear_text("Воыфлв игмшсщьббйцро"))