import tkinter as tk
from tkinter import messagebox, ttk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# Download NLTK resources
import nltk
nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sid = SentimentIntensityAnalyzer()

class QuestionnaireApp(tk.Tk):
    def __init__(self, questions):
        super().__init__()

        self.title("Questionnaire Chatbot")

        self.questions = questions
        self.responses = []
        self.current_question_index = 0

        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#add8e6")  # Set light blue background color

        # Add image
        img = Image.open(r"C:\Users\mishr\OneDrive\Pictures\7_11.PNG")  # Change path to your image file
        img = img.resize((200, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        image_label = tk.Label(self, image=img)
        image_label.image = img
        image_label.pack(pady=20)

        self.question_label = tk.Label(self, text=self.questions[self.current_question_index], font=("Helvetica", 12))
        self.question_label.pack(pady=10)

        self.response_entry = tk.Entry(self, width=70, font=("Helvetica", 12))  # Larger input box
        self.response_entry.pack(pady=5)

        self.next_button = tk.Button(self, text="Next", command=self.next_question)
        self.next_button.pack(pady=5)

    def next_question(self):
        response = self.response_entry.get()
        self.responses.append(response)

        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.question_label.config(text=self.questions[self.current_question_index])
            self.response_entry.delete(0, tk.END)
        else:
            self.analyze_responses()

    def analyze_responses(self):
        feedback = self.analyze_responses_for_personality()
        self.show_feedback_page(feedback)

    def analyze_responses_for_personality(self):
        """Analyze responses to determine personality."""
        sentiment_scores = [self.sentiment_analysis(response) for response in self.responses]
        avg_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)

        if avg_sentiment_score >= 0.05:
            feedback = "You seem to have an optimistic and outgoing personality."
        elif avg_sentiment_score <= -0.05:
            feedback = "You seem to have a more reserved or introverted personality."
        else:
            feedback = "Your responses indicate a balanced personality."

        # Visualize sentiment distribution
        labels = ['Positive', 'Negative', 'Neutral']
        positive_count = sum(score > 0 for score in sentiment_scores)
        negative_count = sum(score < 0 for score in sentiment_scores)
        neutral_count = sum(score == 0 for score in sentiment_scores)
        sizes = [positive_count, negative_count, neutral_count]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.title('Sentiment Distribution')
        plt.show()

        return feedback

    def sentiment_analysis(self, text):
        """Perform sentiment analysis on the given text."""
        scores = sid.polarity_scores(text)
        return scores['compound']

    def show_feedback_page(self, feedback):
        self.question_label.destroy()
        self.response_entry.destroy()
        self.next_button.destroy()

        feedback_label = tk.Label(self, text="Personality Analysis", font=("Helvetica", 16, "bold"), bg="#add8e6")  # Set light blue background color
        feedback_label.pack(pady=10)

        feedback_text = tk.Text(self, height=10, width=50)
        feedback_text.insert(tk.END, feedback)
        feedback_text.config(state="disabled")
        feedback_text.pack(pady=5)

if __name__ == "__main__":
    questions = [
        "If you could have any superpower, what would it be and why?",
        "What's your favorite type of music, and does it reflect your personality?",
        "Would you rather explore the deep sea or outer space?",
        "What's your opinion on taking risks?",
        "If you could change one thing about the world, what would it be?",
        "Do you prefer spending time alone or with others?",
        "What's your most cherished childhood memory?",
        "If you could live in any era of history, which would you choose?",
        "How do you handle challenges and setbacks in life?",
        "What's the most important value in life, in your opinion?"
    ]

    app = QuestionnaireApp(questions)
    app.mainloop()
