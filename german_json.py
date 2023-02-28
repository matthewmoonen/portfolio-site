
def main():
    return "error"

def lesson_json():

    return [
        {
        "lessonTitle": "Masculine Nominative and Accusative",
        "difficulty": 1,
        "posPointAggregate": 10,
        "negPointAggregate": 4,
        "lives": 5,
        "instructions": "The nominative case is the <em>subject</em> of a sentence; while the accusative is the <em>direct object</em>:</p><p><ul><li>Nominative => takes action</li><li>Accusative => receives action</li></ul><br>For masculine nouns:<ul><li>Der => Nominative</li><li>Den => Accusative</li></ul><br><h3>Example</h3><span style='color: blueviolet;'>The boy <em>(nominative)</em></span> throws <span style='color: yellow;'>the ball <em>(accusative)</em></span>.<br><span style='font-size: 0.85em'><em>In German: <span style='color: blueviolet;'>Der Junge</span> wirft <span style='color: yellow;'>den Ball</span></em></span>.",
        "reminder": "<h3>Reminder</h3><ul><li>Nominative => takes action</li><li>Accusative => receives action</li></ul><br>For masculine nouns:<ul><li>Der => Nominative</li><li>Den => Accusative</li></ul>",
        },
        {
        "questionID": "AAA01",
        "instructions": "Choose the <label class='question-highlight'>nominative</label> case",
        "hint": "",
        "question": "Der Hund jagt den Ball",
        "english": "The dog chases the ball",
        "options": [["Der Hund", True], ["Den Ball", False]],
        "type": "multiChoice",
        },
        {
        "questionID": "AAA02",
        "instructions": "Choose the <label class='question-highlight'>accusative</label> case",
        "hint": "",
        "question": "Der Hund jagt den Ball",
        "english": "The dog chases the ball",
        "options": [["Der Hund", False], ["Den Ball", True]],
        "type": "multiChoice",
        },
        {
        "questionID": "AAA03",
        "instructions": "Choose the <label class='question-highlight'>nominative</label> case",
        "hint": "",
        "question": "Der Hund beißt den Mann",
        "english": "The dog bites the man",
        "options": [["Der Hund", True], ["Den Mann", False],],
        "type": "multiChoice",
        },
        {"questionID": "AAA04",
        "instructions": "Choose the <label class='question-highlight'>accusative</label> case",
        "hint": "",
        "question": "Der Hund beißt den Mann",
        "english": "The dog bites the man",
        "options": [["Der Hund", False], ["Den Mann", True]],
        "type": "multiChoice",
        },
        {
        "questionID": "AAA05",
        "instructions": "Choose the <label class='question-highlight'>nominative</label> case",
        "hint": "",
        "question": "Der Hund und der Mann",
        "english": "The dog and the man",
        "options": [["Der Hund", False], ["Der Mann", False], ["Both are nominative", True]],
        "type": "multiChoice",
        },

        {
        "questionID": "AAA06",
        "instructions": "Choose the <label class='question-highlight'>accusative</label> case",
        "hint": "",
        "question": "Leg den Ball auf den Tisch",
        "english": "Put the ball on the table",
        "options": [["Den Ball", False], ["Den Tisch", False], ["Both are accusative", True]],
        "type": "multiChoice",
        },

        {
        "questionID": "AAA07",
        "instructions": "Choose the <label class='question-highlight'>nominative</label> case",
        "hint": "",
        "question": "Der Junge mag den Hund",
        "english": "The boy likes the dog",
        "options": [["Der Junge", True], ["Den Hund", False], ["Both are nominative", False]],
        "type": "multiChoice",
        },
        {
        "questionID": "AAA08",
        "instructions": "Choose the <label class='question-highlight'>nominative</label> case",
        "hint": "",
        "question": "Der Hund mag den Junge",
        "english": "The dog likes the boy",
        "options": [["Der Hund", True], ["Der Junge", False], ["Both are nominative", False]],
        "type": "multiChoice",
        },
        {
        "questionID": "AAA09",
        "instructions": "Choose the <label class='question-highlight'>nominative</label> definite article",
        "hint": "",
        "question": "Wo ist ___ Mann?",
        "english": "Where is the man?",
        "options": [["Der", True], ["Den", False]],
        "type": "multiChoice",
        },


        {
        "questionID": "AAA10",
        "instructions": "Choose the correct <label class='question-highlight'>definite article</label>",
        "hint": "",
        "question": "Der Junge und ___ Hund",
        "english": "The boy and the dog",
        "options": [["Der", True], ["Den", False],],
        "type": "multiChoice",
        },

        {
        "questionID": "AAA11",
        "instructions": "Choose the <label class='question-highlight'>nominative</label> case",
        "hint": "",
        "question": "Der Mann beißt den Hund!",
        "english": "The man bites the dog!",
        "options": [["Der Mann", True], ["Den Hund", False]],
        "type": "multiChoice",
        },
        {
        "questionID": "AAA12",
        "instructions": "Choose the <label class='question-highlight'>accusative</label> case",
        "hint": "",
        "question": "Der Hund beißt den Mann",
        "english": "The dog bites the man",
        "options": [["Der Hund", False], ["Den Mann", True]],
        "type": "multiChoice",
        },
        ]
    

# Legen Sie bitte den Ball auf den Tisch
# Er hat den Hund

if __name__ == "__main__":
    main()