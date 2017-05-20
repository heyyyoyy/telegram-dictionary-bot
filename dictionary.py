from bs4 import BeautifulSoup
import requests
import const


class Dictionary:
    def __init__(self):
        self._word = ''
        self.soup = None

    def set_word(self, word):
        self._word = word

    def response(self, url):
        resp = requests.get(url + self._word)
        if resp.url == url:
            return ''
        self.soup = BeautifulSoup(resp.text, features='lxml')
        return resp.text

    def get_transcription(self):
        transc = self.soup.find('span', class_='pron').text
        return transc

    def get_audio(self):
        audio = self.soup.find('span', class_='circle circle-btn sound audio_play_button uk').get('data-src-mp3')
        return audio


class Interpretation(Dictionary):
    def __init__(self):
        super().__init__()

    def get_title(self):
        title = self.soup.find('span', class_='hw').text
        return title

    def get_labels(self):
        try:
            label = self.soup.find('span', class_='pos').text
        except AttributeError:
            return 'Not label'
        else:
            return label

    def description(self):
        descr = self.soup.find_all('div', class_='def-block pad-indent')
        lst = []
        for d in descr:
            des = d.find('p', class_='def-head semi-flush').text
            if des != '' and des[:2] in const.levels:
               des = '*{}* {}'.format(des[:2], des[2:])
            example = d.find_all('span', class_='def-body')
            example = '\n'.join(map(lambda x: x.text, example))
            lst.append([des, example])
        return lst

    def get_dict(self):
        title = self.get_title()
        labels = self.get_labels()
        audio = self.get_audio()
        transcr = self.get_transcription()
        descr = self.description()
        return {
            'title': title,
            'label': labels,
            'audio': audio,
            'transcr': transcr,
            'descr': descr
        }


class Translate(Dictionary):
    def __init__(self):
        super().__init__()

    def get_title(self):
        title = self.soup.find('h2', class_='di-title cdo-section-title-hw').text
        return title

    def get_labels(self):
        try:
            label = self.soup.find('span', class_='posgram ico-bg').text
        except AttributeError:
            return 'Not label'
        else:
            return label

    def description(self):
        descr = self.soup.find_all('div', class_='def-block pad-indent')
        lst = []
        for d in descr:
            des = d.find('p', class_='def-head semi-flush').text
            if des != '' and des[:2] in const.levels:
                des = '*{}* {}'.format(des[:2], des[2:])
            trans = d.find('span', class_='trans').text.strip()
            ex = d.find_all('div', class_='examp emphasized')
            ex = '\n'.join(map(lambda x: x.text, ex))
            lst.append([des, trans, ex])
        return lst

    def get_dict(self):
        title = self.get_title()
        labels = self.get_labels()
        audio = self.get_audio()
        transcr = self.get_transcription()
        descr = self.description()
        return {
            'title': title,
            'label': labels,
            'audio': audio,
            'transcr': transcr,
            'descr': descr
        }
