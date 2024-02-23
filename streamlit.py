import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from PIL import Image
import nltk

# Download NLTK resources
nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sid = SentimentIntensityAnalyzer()

class QuestionnaireApp:
    def __init__(self, questions):
        self.questions = questions
        self.responses = []
        self.current_question_index = 0

    def next_question(self, response):
        self.responses.append(response)
        self.current_question_index += 1

    def analyze_responses(self):
        feedback = self.analyze_responses_for_personality()
        return feedback

    def analyze_responses_for_personality(self):
        """Analyze responses to determine personality."""
        sentiment_scores = [self.sentiment_analysis(response) for response in self.responses]
        avg_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)

        if avg_sentiment_score >= 0.05:
            return "You seem to have an optimistic and outgoing personality."
        elif avg_sentiment_score <= -0.05:
            return "You seem to have a more reserved or introverted personality."
        else:
            return "Your responses indicate a balanced personality."

    def sentiment_analysis(self, text):
        """Perform sentiment analysis on the given text."""
        scores = sid.polarity_scores(text)
        return scores['compound']

# Create an instance of the QuestionnaireApp
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

questionnaire = QuestionnaireApp(questions)

# Streamlit UI
st.title("Questionnaire Chatbot")
st.image(Image.open(r"C:\Users\mishr\OneDrive\Pictures\7_11.PNG"), caption='Image Caption', use_column_width=True)

if st.button("Start"):
    for question in questions:
        response = st.text_input(question)
        questionnaire.next_question(response)

    feedback = questionnaire.analyze_responses()
    st.subheader("Personality Analysis")
    st.write(feedback)
