import json
import os # The os module helps check if the file exists

# Name of the file where we store the data
FILE_NAME = "flashcards.json"

def load_flashcards():
    """
    Loads flashcards from the JSON file.
    Returns a list of dictionaries.
    """
    # 1. Check if the file exists
    if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:
        # If the file is missing or empty, return an empty list
        print("INFO: Flashcard file not found or is empty. Starting with default/empty list.")
        return []

    # 2. Load data from the file
    try:
        with open(FILE_NAME, 'r') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError:
        # Handles cases where the file exists but has corrupted JSON data
        print("ERROR: Could not decode JSON data. Starting with an empty list.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading: {e}")
        return []

def save_flashcards(card_list):
    """
    Saves the current list of flashcards to the JSON file.
    Takes a list of dictionaries (card_list) as input.
    """
    try:
        with open(FILE_NAME, 'w') as file:
            # Use json.dump to write the list to the file
            # indent=4 makes the file human-readable
            json.dump(card_list, file, indent=4)
        print("INFO: Flashcards saved successfully.")
    except Exception as e:
        print(f"ERROR: Could not save flashcards: {e}")

# Example of how you would use the load/save functions
if __name__ == '__main__':
    # Initial load
    my_cards = load_flashcards()
    print("Loaded cards:", my_cards)
    
    # Add a new card
    new_card = {"question": "What is Python's GUI library?", "answer": "Tkinter"}
    my_cards.append(new_card)
    print("Cards after adding:", my_cards)

    # Save the updated list
    save_flashcards(my_cards)
    