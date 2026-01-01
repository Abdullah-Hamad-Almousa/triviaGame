import requests
import random
import html


def get_categories():

    try:
        response = requests.get("url to fetch the data")
        response.raise_for_status()
        data = response.json()
        return data.get("trivia_categories", [])
    except requests.RequestException as e:
        print(f"Error fetching categories: {e}")
        return []


def fetch_questions(difficulty, category_id, amount=5):

    url = "url to fetch the data"
    params = {
        "amount": amount,
        "category": category_id,
        "difficulty": difficulty,
        "type": "multiple"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["response_code"] != 0:
            print(f"API Error Code: {data['response_code']}")
            return []

        return data.get("results", [])
    except requests.RequestException as e:
        print(f"Error fetching questions: {e}")
        return []


def start_quiz(questions):

    score = 0
    total_questions = len(questions)

    print(f"\nStarting Quiz! ({total_questions} questions)\n")

    for i, q in enumerate(questions, 1):
        print(f"Question {i}: {html.unescape(q['question'])}")

        correct_answer = html.unescape(q['correct_answer'])
        incorrect_answers = [html.unescape(ans) for ans in q['incorrect_answers']]
        options = incorrect_answers + [correct_answer]
        random.shuffle(options)

        for idx, option in enumerate(options, 1):
            print(f"  {idx}. {option}")

        while True:
            try:
                user_choice = int(input("Your answer (number): "))
                if 1 <= user_choice <= len(options):
                    selected_option = options[user_choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(options)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        if selected_option == correct_answer:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect. The right answer was: {correct_answer}\n")

    return score, total_questions


def display_results(score, total):

    print("=" * 30)
    print("\tQUIZ COMPLETED")
    print("=" * 30)
    print(f"Final Score: {score} / {total}")

    percentage = (score / total) * 100 if total > 0 else 0
    print(f"Percentage: {percentage:.1f}%")

    if percentage == 100:
        print("Perfect Score! You're a Trivia Master!")
    elif percentage >= 70:
        print("Great job! Well done.")
    elif percentage >= 50:
        print("Good effort. Keep practicing!")
    else:
        print("Better luck next time!")
    print("=" * 30)


def main():

    print("Welcome to the Trivia Quiz Game!")

    print("\nFetching categories...")
    categories = get_categories()

    if not categories:
        print("Could not load categories. Exiting.")
        return

    print("\nAvailable Categories:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat['name']}")

    while True:
        try:
            cat_choice = int(input("\nSelect a category number (0 for random): "))
            if 0 <= cat_choice <= len(categories):
                if cat_choice == 0:
                    category_id = None
                    print("Selected Random Category.")
                else:
                    category_id = categories[cat_choice - 1]['id']
                    print(f"Selected Category: {categories[cat_choice - 1]['name']}")
                break
            else:
                print(f"Please enter a number between 0 and {len(categories)}.")
        except ValueError:
            print("Invalid input.")

    difficulties = ["easy", "medium", "hard"]
    print("\nSelect Difficulty:")
    for i, diff in enumerate(difficulties, 1):
        print(f"{i}. {diff.capitalize()}")

    while True:
        try:
            diff_choice = int(input("Select difficulty number: "))
            if 1 <= diff_choice <= 3:
                difficulty = difficulties[diff_choice - 1]
                break
            else:
                print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input.")

    print("\nFetching questions...")
    questions = fetch_questions(difficulty, category_id)

    if not questions:
        print("No questions found. Try a different category or difficulty.")
        return

    score, total = start_quiz(questions)

    display_results(score, total)


if __name__ == "__main__":
    main()