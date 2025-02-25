import os
import datetime
import speech_recognition as sr
from mtranslate import translate
from gtts import gTTS
import pygame
import tkinter as tk
from tkinter import scrolledtext, Button, Label, ttk, Entry

pygame.init()

r = sr.Recognizer()

# Supported languages for translation
supported_languages = {
    'Afrikaans': 'af',
    'Albanian': 'sq',
    'Amharic': 'am',
    'Arabic': 'ar',
    'Armenian': 'hy',
    'Azerbaijani': 'az',
    'Basque': 'eu',
    'Belarusian': 'be',
    'Bengali': 'bn',
    'Bosnian': 'bs',
    'Bulgarian': 'bg',
    'Catalan': 'ca',
    'Cebuano': 'ceb',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Corsican': 'co',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Esperanto': 'eo',
    'Estonian': 'et',
    'Finnish': 'fi',
    'French': 'fr',
    'Frisian': 'fy',
    'Galician': 'gl',
    'Georgian': 'ka',
    'German': 'de',
    'Greek': 'el',
    'Gujarati': 'gu',
    'Haitian Creole': 'ht',
    'Hausa': 'ha',
    'Hawaiian': 'haw',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Hmong': 'hmn',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Igbo': 'ig',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Javanese': 'jv',
    'Kannada': 'kn',
    'Kazakh': 'kk',
    'Khmer': 'km',
    'Korean': 'ko',
    'Kurdish': 'ku',
    'Kyrgyz': 'ky',
    'Lao': 'lo',
    'Latin': 'la',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Luxembourgish': 'lb',
    'Macedonian': 'mk',
    'Malagasy': 'mg',
    'Malay': 'ms',
    'Malayalam': 'ml',
    'Maltese': 'mt',
    'Maori': 'mi',
    'Marathi': 'mr',
    'Mongolian': 'mn',
    'Myanmar (Burmese)': 'my',
    'Nepali': 'ne',
    'Norwegian': 'no',
    'Nyanja (Chichewa)': 'ny',
    'Odia (Oriya)': 'or',
    'Pashto': 'ps',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Punjabi': 'pa',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Samoan': 'sm',
    'Scots Gaelic': 'gd',
    'Serbian': 'sr',
    'Sesotho': 'st',
    'Shona': 'sn',
    'Sindhi': 'sd',
    'Sinhala (Sinhalese)': 'si',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Somali': 'so',
    'Spanish': 'es',
    'Sundanese': 'su',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tagalog (Filipino)': 'tl',
    'Tajik': 'tg',
    'Tamil': 'ta',
    'Tatar': 'tt',
    'Telugu': 'te',
    'Thai': 'th',
    'Turkish': 'tr',
    'Turkmen': 'tk',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Uyghur': 'ug',
    'Uzbek': 'uz',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Xhosa': 'xh',
    'Yiddish': 'yi',
    'Yoruba': 'yo',
    'Zulu': 'zu',
}

class TranslatorApp:
    def __init__(self):
        self.initialize_gui()
        self.setup_recognition()

    def initialize_gui(self):
        self.root = tk.Tk()
        self.root.title("Speech Translator")
        self.root.attributes('-fullscreen', True)

        self.setup_style()
        self.create_logo_label()
        self.create_text_widget()
        self.create_language_widgets()
        self.create_translate_and_exit_buttons()

        self.update_after_id = None

    def setup_style(self):
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TEntry", font=("Arial", 12))

    def create_logo_label(self):
        self.logo_label = ttk.Label(self.root, text="FluentFlow", font=("Arial", 50, "bold"))
        self.logo_label.pack(side=tk.TOP, pady=10)

    def create_text_widget(self):
        self.text_widget = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=15, font=("Arial", 12))
        self.text_widget.pack(padx=20, pady=10)

    def create_language_widgets(self):
        self.create_language_entry_and_label("Source", "search_source")
        self.create_language_dropdown("Source", "source")

        self.create_language_entry_and_label("Target", "search_target")
        self.create_language_dropdown("Target", "target")

    def create_language_entry_and_label(self, label_text, entry_name):
        label = ttk.Label(self.root, text=f"Search {label_text} Language:")
        label.pack()

        entry = ttk.Entry(self.root)
        entry.pack()
        entry.bind("<KeyRelease>", getattr(self, f"update_{entry_name}_dropdown_options"))

        setattr(self, f"{entry_name}_entry", entry)

    def create_language_dropdown(self, label_text, dropdown_name):
        label = ttk.Label(self.root, text=f"{label_text} Language:")
        label.pack()

        lang_var = tk.StringVar()
        lang_var.set("English")
        dropdown = ttk.Combobox(self.root, textvariable=lang_var, values=list(supported_languages.keys()))
        dropdown.pack()

        setattr(self, f"{dropdown_name}_lang", lang_var)
        setattr(self, f"{dropdown_name}_dropdown", dropdown)

    def create_translate_and_exit_buttons(self):
        translate_button = ttk.Button(self.root, text="Translate", command=self.translate_speech)
        translate_button.pack(pady=5)

        exit_button = ttk.Button(self.root, text="Exit", command=self.exit_program)
        exit_button.pack(pady=5)

    def setup_recognition(self):
        self.r = sr.Recognizer()

    def filter_languages(self, query):
        return [lang_name for lang_name in supported_languages.keys() if query.lower() in lang_name.lower()]

    def update_search_source_dropdown_options(self, event=None):
        self.update_dropdown_options("source")

    def update_search_target_dropdown_options(self, event=None):
        self.update_dropdown_options("target")

    def update_dropdown_options(self, dropdown_name):
        query = getattr(self, f"search_{dropdown_name}_entry").get()
        filtered_languages = self.filter_languages(query)
        if filtered_languages:
            getattr(self, f"{dropdown_name}_lang").set(filtered_languages[0])

    def translate_speech(self):
        self.source_lang_value = supported_languages[self.source_lang.get()]
        self.target_lang_value = supported_languages[self.target_lang.get()]

        source_folder = f"translated_audio/{self.source_lang_value}"
        target_folder = f"translated_audio/{self.target_lang_value}"
        os.makedirs(source_folder, exist_ok=True)
        os.makedirs(target_folder, exist_ok=True)

        def update_gui():
            self.update_status_message("Listening to you...")

            try:
                with sr.Microphone() as source:
                    audio = self.r.listen(source)

                speech_text = self.r.recognize_google(audio, language=self.source_lang_value)
                self.text_widget.insert(tk.END, f"Detected source language: {self.source_lang_value}\n")
                self.text_widget.insert(tk.END, f"{speech_text}\n")
                if speech_text.lower() == "exit":
                    return

                translated_text = translate(speech_text, self.target_lang_value)
                self.text_widget.insert(tk.END, f"Translated to {self.target_lang_value}: {translated_text}\n")

                current_datetime = datetime.datetime.now().strftime("%B.%d.%Y.%H.%M.%S")
                filename = f"translated_audio/{self.target_lang_value}/Voice.{current_datetime}.mp3"

                voice = gTTS(translated_text, lang=self.target_lang_value, slow=False)
                voice.save(filename)

                self.play_audio(filename)

                self.update_after_id = self.root.after(100, update_gui)

            except sr.UnknownValueError:
                self.text_widget.insert(tk.END, "Could not understand\n")
                self.update_after_id = self.root.after(100, update_gui)
            except sr.RequestError:
                self.text_widget.insert(tk.END, "Could not request result from Google\n")
                self.update_after_id = self.root.after(100, update_gui)

        update_gui()

    def exit_program(self):
        self.text_widget.insert(tk.END, "Exiting the program.\n")
        self.root.destroy()

    def update_status_message(self, message):
        self.text_widget.insert(tk.END, f"{message}\n")
        self.root.update_idletasks()

    def play_audio(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TranslatorApp()
    app.run()