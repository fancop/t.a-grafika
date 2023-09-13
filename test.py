import tkinter as tk
from tkinter import filedialog, messagebox
import os
from typing import NoReturn
from string import punctuation
from collections import Counter
import re
import pymorphy3



class TextAnalyzer:
    def __init__(self, file_name, mode="r", encoding="UTF-8", pos_list=["VERB", "NOUN"]):
        if file_name is None:
            raise Exception("Не указан файл для анализа!")
        self.file_name = file_name
        self.mode = mode
        self.encoding = encoding
        self.pos_list = pos_list
        self.read_file()
        self.check_empty_file()
        self.prepare_text()
        self.sorting_words()
        self.print_text()

    def read_file(self):
        """ Пытается открыть файл и считать его в строку """
        try:
            with open(self.file_name, self.mode, encoding=self.encoding) as file:
                self.content = file
                self.text = self.content.read()
        except FileNotFoundError:
            raise Exception(f"Файл {self.file_name} не найден!")

    def check_empty_file(self):
        """ проверяет пустой ли файл """
        if not self.text:
            raise RuntimeError(f"Файл {self.file_name} пустой!")

    def prepare_text(self):
        """ Приводит текст к нижнему регистру и убирает все лишние знаки препинания """
        self.text = self.text.lower()
        self.words = re.findall(r'\b[\w-]+\b', self.text)

    def sorting_words(self) -> list:
        morph = pymorphy3.MorphAnalyzer()
        self.words_by_pos = []

        for word in self.words:
            parsed_word = morph.parse(word)[0]
            pos = parsed_word.tag.POS
            if pos in self.pos_list:
                self.words_by_pos.append(parsed_word.normal_form)

        self.top_words = Counter(self.words_by_pos).most_common(10)

    def print_text(self):
        """ Выводит строку текста на экран """
        print(self.words_by_pos)


class TextAnalyzerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("800x600")
        self.window.title("Text Analyzer")
        self.file_path = None
        self.create_widgets()

    def create_widgets(self):
        # File Selection Frame
        file_frame = tk.Frame(self.window)
        file_frame.pack(pady=10)

        file_label = tk.Label(file_frame, text="Select a TXT file:")
        file_label.pack(side=tk.LEFT)

        browse_button = tk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_button.pack(side=tk.LEFT, padx=10)

        # Analysis Frame
        analysis_frame = tk.Frame(self.window)
        analysis_frame.pack(pady=10)

        top10_button = tk.Button(analysis_frame, text="Top 10 Words", command=self.analyze_top_10)
        top10_button.pack(side=tk.LEFT)

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt')])

    def analyze_top_10(self):
        if self.file_path:
            try:
                analyzer = TextAnalyzer(self.file_path)
                top_words = analyzer.top_words

                # Display top 10 words in a messagebox
                words_str = "\n".join([f"{i+1}. {word}: {count}" for i, (word, count) in enumerate(top_words)])
                messagebox.showinfo("Top 10 Words", f"Top 10 words in the text:\n\n{words_str}")

            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "Please select a TXT file.")

    def run(self):
        self.window.mainloop()


# Run the GUI
gui = TextAnalyzerGUI()
gui.run()