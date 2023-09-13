import tkinter as tk
from tkinter import filedialog, messagebox

class TextAnalyzerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text Analyzer")
        
        self.file_path = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # File Selection Frame
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)
        
        file_label = tk.Label(file_frame, text="Select a TXT file:")
        file_label.pack(side=tk.LEFT)
        
        browse_button = tk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_button.pack(side=tk.LEFT, padx=10)
        
        # Analysis Frame
        analysis_frame = tk.Frame(self.root)
        analysis_frame.pack(pady=10)
        
        top10_button = tk.Button(analysis_frame, text="Top 10 Words", command=self.analyze_top_10)
        top10_button.pack(side=tk.LEFT)
        
        wordcloud_button = tk.Button(analysis_frame, text="Generate Wordcloud", command=self.generate_wordcloud)
        wordcloud_button.pack(side=tk.LEFT, padx=10)
        
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
    
    def generate_wordcloud(self):
        if self.file_path:
            try:
                analyzer = TextAnalyzer(self.file_path)
                analyzer.display_wordcloud()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "Please select a TXT file.")
    
    
    def run(self):
        self.root.mainloop()

# Run the GUI
gui = TextAnalyzerGUI()
gui.run()