# question/loader.py
from question.processor import QuestionProcessor



def get_questions(section_name):
    processor = QuestionProcessor(section_name)
    processor.process_file()
    return [processor.get_random_question()]
