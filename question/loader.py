def get_questions(section_name):
    questions = {
        "Story": ["What is the moral of the story?"],
        "Time": ["What time is shown on the clock?"],
        "Currency": ["How much money is there?"],
        "Distance": ["What is the distance between two places?"],
        "Bellring": ["When will the next bell ring?"],
        "Operations": ["What is 5 + 3?"]
    }
    return questions.get(section_name, ["No questions found."])
