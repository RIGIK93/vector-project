def perform_action(option_name):
  """A function that is called by menu options 1-3."""
  print(f"\n-> You have selected '{option_name}'. This function has been called.\n")

def main_menu():
  """Displays the main menu and handles user input."""
  while True:
    # Display the menu options
    print("--- Main Menu ---")
    print("1. Call Option A")
    print("2. Call Option B")
    print("3. Call Option C")
    print("4. Exit Program")
    print("-----------------")
    
    # Get user input
    choice = input("Please enter your choice (1-4): ")

    # Process the user's choice
    if choice == '1':
      perform_action("Option A")
    elif choice == '2':
      perform_action("Option B")
    elif choice == '3':
      perform_action("Option C")
    elif choice == '4':
      print("\nExiting the program. Goodbye! 👋")
      break # Exit the while loop
    else:
      # Handle invalid input
      print(f"\n! Invalid input: '{choice}'. Please enter a number between 1 and 4.\n")
    input("Press enter to proceed...")

# Start the program by calling the main_menu function
main_menu()
