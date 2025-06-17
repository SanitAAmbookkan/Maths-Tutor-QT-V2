# question/loader.py
from question.processor import QuestionProcessor

def get_questions(section_name, difficulty_index):
    processor = QuestionProcessor(section_name.lower(), difficulty_index)
    processor.process_file()
    return [processor.get_random_question()]
