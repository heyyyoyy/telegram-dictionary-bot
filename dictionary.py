from bs4 import BeautifulSoup
import requests
import settings

levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']


class Dictionary:
    @classmethod
    def response(cls, word, url):
        resp = requests.get(url + word.split()[-1])
        if resp.url == url:
            raise ValueError
        soup = BeautifulSoup(resp.text, features='lxml')
        return soup

    @classmethod
    def get_transcription(cls, soup):
        transc = soup.find('span', class_='pron').text
        return transc

    @classmethod
    def get_audio(cls, soup):
        audio = soup.find('span', class_='circle circle-btn sound audio_play_button uk').get('data-src-mp3')
        return audio

    @classmethod
    def get_title(cls, soup):
        pass

    @classmethod
    def get_labels(cls, soup):
        pass

    @classmethod
    def get_description(cls, soup):
        pass

    @classmethod
    def make_dict(cls, soup):
        title = cls.get_title(soup)
        labels = cls.get_labels(soup)
        audio = cls.get_audio(soup)
        transcr = cls.get_transcription(soup)
        descr = cls.get_description(soup)
        return {
            'title': title,
            'label': labels,
            'audio': audio,
            'transcr': transcr,
            'descr': descr
        }


class Interpretation(Dictionary):
    @classmethod
    def get_title(cls, soup):
        title = soup.find('span', class_='hw').text
        return title

    @classmethod
    def get_labels(cls, soup):
        try:
            label = soup.find('span', class_='pos').text
        except AttributeError:
            return 'Not label'
        else:
            return label

    @classmethod
    def get_description(cls, soup):
        descr = soup.find_all('div', class_='def-block pad-indent')
        description_list = []
        for d in descr:
            des = d.find('p', class_='def-head semi-flush').text
            if des != '' and des[:2] in levels:
                des = '*{}* {}'.format(des[:2], des[2:])
            example = d.find_all('span', class_='def-body')
            example = '\n'.join(map(lambda x: x.text, example))
            description_list.append([des, example])
        descriptions = list(map(lambda x: '\[Description] {}\n'
                                          '\[Example] {}\n'.format(x[0], x[1]), description_list))
        return descriptions

    @classmethod
    def get_dict(cls, word):
        try:
            soup = cls.response(word, settings.URL_INTERPRETATION)
        except ValueError:
            return False
        else:
            return cls.make_dict(soup)


class Translate(Dictionary):
    @classmethod
    def get_title(cls, soup):
        title = soup.find('h2', class_='di-title cdo-section-title-hw').text
        return title

    @classmethod
    def get_labels(cls, soup):
        try:
            label = soup.find('span', class_='posgram ico-bg').text
        except AttributeError:
            return 'Not label'
        else:
            return label

    @classmethod
    def get_description(cls, soup):
        descr = soup.find_all('div', class_='def-block pad-indent')
        description_list = []
        for d in descr:
            des = d.find('p', class_='def-head semi-flush').text
            if des != '' and des[:2] in levels:
                des = '*{}* {}'.format(des[:2], des[2:])
            trans = d.find('span', class_='trans').text.strip()
            ex = d.find_all('div', class_='examp emphasized')
            ex = '\n'.join(map(lambda x: x.text, ex))
            description_list.append([des, trans, ex])
        descriptions = list(map(lambda x: '\[Description] {}\n'
                                          '\[Translate] {}\n'
                                          '\[Example] {}\n'.format(x[0], x[1], x[2]), description_list))
        return descriptions

    @classmethod
    def get_dict(cls, word):
        try:
            soup = cls.response(word, settings.URL_TRANSLATE)
        except ValueError:
            return False
        else:
            return cls.make_dict(soup)
