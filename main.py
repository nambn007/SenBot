import os
import webbrowser
from pyvi import ViTokenizer

class Action:
    OPEN = 1
    SEARCH = 2
    DO_NOTHING = -1

    map_text_to_action = {
        "mở": OPEN,
        "tìm kiếm": SEARCH,
        "mo": OPEN,
        "tim kiem": SEARCH,
        "tìm_kiếm": SEARCH,
        "tim_kiem": SEARCH
    }


class OBJECT:
    GOOGLE = 1
    YOUTUBE = 2
    FACEBOOK = 3
    SOUNDCLOUD = 4
    SPOTIFY = 5

    map_text_obj_to_obj = {
        "youtube": YOUTUBE,
        "facebook": FACEBOOK,
        "google": GOOGLE,
        "soundcloud": SOUNDCLOUD,
        "spotify": SPOTIFY
    }

    map_obj_to_link = {
        YOUTUBE: "https://www.youtube.com/",
        FACEBOOK: "https://www.facebook.com/",
        GOOGLE: "https://www.google.com/",
        SOUNDCLOUD: "https://soundcloud.com/",
        SPOTIFY: "https://www.spotify.com"
    }


class Assistant:
    def __init__(self):

        self.action = None
        self.object = None
        self.text = None

    """
    Extract information text action such as: action, object 
    Text: Vietnamese 
    """
    def preprocessing_text_action(self, text):
        if text:
            if len(text) > 0:
                words = ViTokenizer.tokenize(text.lower())

                action = None
                for act in list(Action.map_text_to_action.keys()):
                    if act in words:
                        action = Action.map_text_to_action[act]
                        break

                ob = None
                for obj in list(OBJECT.map_text_obj_to_obj.keys()):
                    if obj in words:
                        ob = OBJECT.map_text_obj_to_obj[obj]

                if action is not None:
                    return action, ob
        return None

    def recognition_action(self, text):
        self.text = text
        res = self.preprocessing_text_action(text)
        if res:
            self.action = res[0]
            self.object = res[1]

    def do_action(self, text):
        self.recognition_action(text)
        link = self.get_link()
        Assistant.open_browser(link)

    def get_link(self):
        link = None

        if self.action == Action.OPEN:
            link = OBJECT.map_obj_to_link[self.object]
        elif self.action == Action.SEARCH:
            # Search in here
            if self.text is not None:
                try:
                    text_search = self.text[self.text.find("tôi")+3:]
                    link = 'https://www.google.com/search?q=' + text_search
                    print('Tim kiem cho toi', text_search)
                except Exception as e:
                    link = None
        return link

    @staticmethod
    def open_browser(link):
        if link:
            webbrowser.open(link)
        print("Don't know you question")


if __name__ == '__main__':
    bot = Assistant()
    bot.do_action('mở facebook')
    # bot.do_action("tìm kiếm cho tôi Bac Ho sinh nam bao nhieu")
