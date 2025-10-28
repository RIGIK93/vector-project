def dms_to_decimal(dms_string):
    """
    Converts a Degree-Minute-Second string to Decimal Degrees.
    Handles N, S, E, W directions for sign.
    """
    try:
        parts = dms_string.strip().split()
        if len(parts) != 4:
            # Raises an error if the format is incorrect
            raise ValueError(
                "Invalid format. Please use 'D M S C' (e.g., '73 59 11 W')."
            )

        degrees = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        direction = parts[3].upper()  # Ensures direction is uppercase for comparison

        if direction not in ["N", "S", "E", "W"]:
            raise ValueError("Invalid direction. Must be N, S, E, or W.")

        # The conversion formula
        decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)

        # Apply negative sign for Southern and Western hemispheres
        if direction in ["S", "W"]:
            decimal_degrees *= -1

        return decimal_degrees

    except (ValueError, IndexError):
        # Catches errors from incorrect string parts or non-numeric values
        raise ValueError(
            "Invalid input. Ensure degrees, minutes, and seconds are numbers."
        )


def perform_action(option_name):
    """A function that is called by menu options 2-3."""
    print(f"\n-> You have selected '{option_name}'. This function has been called.\n")


def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        # Display the menu options
        print("--- Main Menu ---")
        print("1. Convert DMS to Decimal Degrees")
        print("2. Call Option B")
        print("3. Call Option C")
        print("4. Exit Program")
        print("-----------------")

        # Get user input
        choice = input("Please enter your choice (1-4): ")

        # Process the user's choice
        if choice == "1":
            try:
                dms_input = input("Enter DMS (e.g., 40 44 55 N or 73 59 11 W): ")
                decimal_result = dms_to_decimal(dms_input)
                print(
                    f"\n-> Decimal Degrees: {decimal_result:.6f}\n"
                )  # Formats to 6 decimal places
            except ValueError as e:
                print(f"\n! Error: {e}\n")  # Prints the specific error message

        elif choice == "2":
            perform_action("Option B")
        elif choice == "3":
            perform_action("Option C")
        elif choice == "4":
            print("\nExiting the program. Goodbye! 👋")
            break  # Exit the while loop
        else:
            # Handle invalid input
            print(
                f"\n! Invalid input: '{choice}'. Please enter a number between 1 and 4.\n"
            )
        input("Press enter to continue...")

# Start the program by calling the main_menu function
main_menu()
