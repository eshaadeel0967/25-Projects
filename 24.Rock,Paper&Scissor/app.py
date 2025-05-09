import random

def play_game():
    options = ["rock", "paper", "scissors"]
    user_score = 0
    computer_score = 0

    print("Welcome to Rock, Paper, Scissors!")
    print("Type 'exit' to quit the game.\n")

    while True:
        user_input = input("Choose rock, paper, or scissors: ").lower()

        if user_input == "exit":
            print("👋 Thanks for playing!")
            print(f"Final Score - You: {user_score} | Computer: {computer_score}")
            break

        if user_input not in options:
            print("❌ Invalid input. Try again.\n")
            continue

        computer_choice = random.choice(options)
        print(f"Computer chose: {computer_choice}")

        if user_input == computer_choice:
            print("It's a tie! 😐")
        elif (user_input == "rock" and computer_choice == "scissors") or \
             (user_input == "paper" and computer_choice == "rock") or \
             (user_input == "scissors" and computer_choice == "paper"):
            print("You win! 🎉")
            user_score += 1
        else:
            print("Computer wins! 🤖")
            computer_score += 1

        print(f"Score - You: {user_score} | Computer: {computer_score}\n")

# Run the game
play_game()
