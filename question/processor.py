import os
import pandas as pd
import random

class QuestionProcessor:
    def __init__(self, questionType,difficultyIndex):
        self.questionType = questionType
        
        self.difficultyIndex = difficultyIndex
        self.df = None
        self.variables = []
        self.oprands = []
        self.rowIndex = 0

    def process_file(self):
        file_path = os.path.join(os.getcwd(), "question", "question.xlsx")
        print(f"Processing file: {file_path}")

        # Load the Excel file
        self.df = pd.read_excel(file_path)
        self.df = pd.DataFrame(self.df)

        # Apply filters: question type and difficulty
        self.df = self.df[
            (self.df["type"].str.lower() == self.questionType.lower()) &
            (self.df["difficulty"] == self.difficultyIndex)
        ]

        self.df = self.df.sort_values(by="difficulty", ascending=True)
        self.current_question_index = 0

        print("Filtered DataFrame:")
        print(self.df)
    def get_random_question(self):
        if self.df.empty:
            return "No questions found.", None

        self.rowIndex = random.randint(0, len(self.df) - 1)

        # Get variable names and operand ranges from the format column (col 2)
        variable_string = str(self.df.iloc[self.rowIndex, 2])
        input_string = ''.join(c for c in variable_string if not c.isalpha())
        variable_names = [c for c in variable_string if c.isalpha()]
        operands = self.parseInputRange(input_string)

        # Store for debugging
        print(f"[DEBUG] Variables: {variable_names}")
        print(f"[DEBUG] Operands: {operands}")

        # Replace placeholders in question and formula
        question_template = str(self.df.iloc[self.rowIndex, 0])  # Column 0: questio
        formula_template = str(self.df.iloc[self.rowIndex, 5])   # Column 5: equation/formula

        for i, var in enumerate(variable_names):
            question_template = question_template.replace(f"{{{var}}}", str(operands[i]))
            formula_template = formula_template.replace(f"{{{var}}}", str(operands[i]))

        # Evaluate answer
        try:
            answer = eval(formula_template)
        except Exception as e:
            print(f"[ERROR] Evaluating equation: {formula_template}")
            print(f"[ERROR] {e}")
            answer = None
        print(f"Question shown: {question_template}")
        print(f"Formula evaluated: {formula_template}")
        print(f"Answer calculated: {answer}")
        return question_template, int(answer) if answer is not None else None



    def removeVariables(self, row, column):
        val = self.df.iloc[row, column]
        return ''.join(c for c in val if not c.isalpha())

    def allVariables(self, row, column):
        val = self.df.iloc[row, column]
        return [c for c in val if c.isalpha()]
    def parseInputRange(self, inputRange):
        operands = []
        current = ""
        for c in inputRange:
            if c == "*":
                operands.append(int(self.extractType(current)))
                current = ""
            else:
                current += c
        if current:
            operands.append(int(self.extractType(current)))
        return operands


    def extractType(self, inputRange):
        if "," in inputRange:
            return random.choice(list(map(int, inputRange.split(","))))
        elif ":" in inputRange:
            a, b = map(int, inputRange.split(":"))
            return random.randint(a, b)
        elif ";" in inputRange:
            a, b, c = map(int, inputRange.split(";"))
            return a * random.randint(b, c)
        return int(inputRange)

    def replaceVariables(self, rowIndex, columnIndex):
        val = str(self.df.iloc[rowIndex, columnIndex])  # Force string to allow .replace()

        for i, var in enumerate(self.variables):
            val = val.replace(f"{{{var}}}", str(self.oprands[i]))

        return val

    
