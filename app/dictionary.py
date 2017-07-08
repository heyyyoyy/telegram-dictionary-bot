from bs4 import BeautifulSoup
import requests
import settings

levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']


class Dictionary:
    @classmethod
    def response(cls, word, url):
        response = requests.get(url + word, allow_redirects=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features='lxml')
            return soup

    @classmethod
    def get_transcription(cls, soup):
        try:
            transcription = soup.find('span', class_='pron').text
        except AttributeError:
            return 'Not transcription'
        return transcription

    @classmethod
    def get_audio(cls, soup):
        try:
            audio = soup.find('span', class_='circle circle-btn sound audio_play_button uk').get('data-src-mp3')
        except AttributeError:
            return
        return audio

    @classmethod
    def get_title(cls, soup):
        raise NotImplementedError

    @classmethod
    def get_labels(cls, soup):
        raise NotImplementedError

    @classmethod
    def get_description(cls, soup):
        raise NotImplementedError

    @classmethod
    def make_dict(cls, soup):
        title = cls.get_title(soup)
        labels = cls.get_labels(soup)
        audio = cls.get_audio(soup)
        transcription = cls.get_transcription(soup)
        description = cls.get_description(soup)
        return {
            'title': title,
            'label': labels,
            'audio': audio,
            'transcription': transcription,
            'description': description
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
        return label

    @classmethod
    def get_description(cls, soup):
        descriptions = soup.find_all('div', class_='def-block pad-indent')
        descriptions_text = []
        for part in descriptions:
            word_description = part.find('p', class_='def-head semi-flush').text
            if word_description != '' and word_description[:2] in levels:
                word_description = '*{0}* {1}'.format(word_description[:2], word_description[2:])
            examples = part.find_all('span', class_='def-body')
            example = '\n'.join(chunk.text for chunk in examples)
            descriptions_text.append([word_description, example])
        descriptions = ['\[Description] {0}\n\[Example] {1}\n'.format(description[0], description[1])
                        for description in descriptions_text]
        return descriptions

    @classmethod
    def get_dict(cls, word):
        soup = cls.response(word, settings.URL_INTERPRETATION)
        if soup:
            return cls.make_dict(soup)


class Translation(Dictionary):
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
        return label

    @classmethod
    def get_description(cls, soup):
        descriptions = soup.find_all('div', class_='def-block pad-indent')
        descriptions_text = []
        for part in descriptions:
            word_description = part.find('p', class_='def-head semi-flush').text
            if word_description != '' and word_description[:2] in levels:
                word_description = '*{0}* {1}'.format(word_description[:2], word_description[2:])
            transcription = part.find('span', class_='trans').text.strip()
            examples = part.find_all('div', class_='examp emphasized')
            example = '\n'.join(chunk.text for chunk in examples)
            descriptions_text.append([word_description, transcription, example])
        descriptions = ['\[Description] {0}\n'
                        '\[Translate] {1}\n'
                        '\[Example] {2}\n'.format(description[0], description[1], description[2])
                        for description in descriptions_text]
        return descriptions

    @classmethod
    def get_dict(cls, word):
        soup = cls.response(word, settings.URL_TRANSLATION)
        if soup:
            return cls.make_dict(soup)

