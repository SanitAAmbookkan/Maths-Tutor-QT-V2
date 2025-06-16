import os
import pandas as pd
import random

class QuestionProcessor:
    def __init__(self, questionType):
        self.questionType = questionType
        self.df = None

    def process_file(self):
        # Automatically build the file path to the Excel file
        file_path = os.path.join(os.getcwd(), "question", "question.xlsx")
        print(f"Processing file: {file_path}")

        # Load the Excel file
        self.df = pd.read_excel(file_path)

        # Filter by question type
        self.df = self.df[self.df["type"] == self.questionType]

        print("Filtered DataFrame:")
        print(self.df)

    def get_random_question(self):
        if self.df is not None and not self.df.empty:
            return random.choice(self.df["question"].tolist())
        else:
            return "No matching questions found."
