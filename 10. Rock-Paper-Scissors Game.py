import random

def get_user_choice():
    """Prompts the user for their choice (rock, paper, or scissors)."""
    while True:
        user_choice = input("Enter your choice (rock, paper, or scissors): ").lower()
        if user_choice in ["rock", "paper", "scissors"]:
            return user_choice
        else:
            print("Invalid choice. Please enter rock, paper, or scissors.")

def get_computer_choice():
    """Generates a random choice for the computer."""
    choices = ["rock", "paper", "scissors"]
    return random.choice(choices)

def determine_winner(user_choice, computer_choice):
    """Determines the winner of the round using a dictionary."""
    rules = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock",
    }
    if user_choice == computer_choice:
        return "tie"
    elif rules[user_choice] == computer_choice:
        return "user"
    else:
        return "computer"

def display_results(user_choice, computer_choice, winner, round_num):
    """Displays the choices and the result of the round."""
    print(f"\n--- Round {round_num} ---")
    print(f"Your choice: {user_choice.capitalize()}")
    print(f"Computer's choice: {computer_choice.capitalize()}")

    if winner == "tie":
        print("Result: It's a tie!")
    elif winner == "user":
        print("Result: You win this round!")
    else:
        print("Result: Computer wins this round!")

def play_again():
    """Asks the user if they want to play another round."""
    while True:
        play_again_input = input("Play again? (yes/no): ").lower()
        if play_again_input in ["yes", "no"]:
            return play_again_input == "yes"
        else:
            print("Invalid input. Please enter yes or no.")

def rock_paper_scissors_game():
    """Main function to run the Rock-Paper-Scissors game."""
    user_score = 0
    computer_score = 0
    round_num = 0

    print("Welcome to Rock-Paper-Scissors!")

    while True:
        round_num += 1
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()
        winner = determine_winner(user_choice, computer_choice)
        display_results(user_choice, computer_choice, winner, round_num)

        if winner == "user":
            user_score += 1
        elif winner == "computer":
            computer_score += 1

        print(f"--- Scores ---")
        print(f"Your Score: {user_score}")
        print(f"Computer Score: {computer_score}")

        if not play_again():
            break

    print("\nThanks for playing!")

if __name__ == "__main__":
    rock_paper_scissors_game()