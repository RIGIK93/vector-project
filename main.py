import math

# --- Constants ---
# Earth's circumference in meters for a simplified, flat-Earth projection
EARTH_CIRCUMFERENCE = 40_000_000
# The distance in meters corresponding to 1 degree of longitude/latitude
DEGREES_TO_METERS = EARTH_CIRCUMFERENCE / 360

# --- NEW CONSTANT FOR HAVERSINE ---
# Average Earth radius in meters (used for Haversine distance)
EARTH_RADIUS_METERS = 6_371_000 
# -----------------------------------

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

        # --- Added Input Validation for Minutes/Seconds ---
        if not (0 <= minutes < 60) or not (0 <= seconds < 60):
             raise ValueError("Minutes and seconds must be between 0 and 59.99...")
        # ------------------------------------------------

        if direction not in ["N", "S", "E", "W"]:
            raise ValueError("Invalid direction. Must be N, S, E, or W.")

        # The conversion formula
        decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)

        # Apply negative sign for Southern and Western hemispheres
        if direction in ["S", "W"]:
            decimal_degrees *= -1

        return decimal_degrees

    except (ValueError, IndexError) as e:
        # Re-raise a more specific error based on the initial check
        if isinstance(e, ValueError) and "Invalid format" in str(e):
             raise
        # Catches errors from incorrect string parts or non-numeric values
        raise ValueError(
            "Invalid input. Ensure degrees, minutes, and seconds are numbers."
        )


def calculate_flat_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance (in meters), standard angle (in degrees),
    and the i (E/W) and j (N/S) components between two points.
    
    Arguments:
        lat1, lon1 (float): Latitude and Longitude of Point 1 (Decimal Degrees).
        lat2, lon2 (float): Latitude and Longitude of Point 2 (Decimal Degrees).

    Returns:
        tuple: (distance_meters, angle_degrees, component_i, component_j)
    """
    
    # Delta Longitude (East/West displacement, corresponds to 'i' component)
    # i component (x-axis) = change in Lon * Scale
    component_i = (lon2 - lon1) * DEGREES_TO_METERS

    # Delta Latitude (North/South displacement, corresponds to 'j' component)
    # j component (y-axis) = change in Lat * Scale
    component_j = (lat2 - lat1) * DEGREES_TO_METERS

    # 1. Calculate distance using Pythagorean theorem: distance = sqrt(i^2 + j^2)
    distance_meters = math.sqrt(component_i**2 + component_j**2)

    # 2. Calculate standard angle (0 degrees = East, 90 degrees = North)
    # The result is in radians. Arguments for atan2 are (y, x) -> (component_j, component_i)
    angle_radians = math.atan2(component_j, component_i)
    angle_degrees = math.degrees(angle_radians)
    
    # Normalize angle to 0 to 360
    if angle_degrees < 0:
        angle_degrees += 360

    return distance_meters, angle_degrees, component_i, component_j


# --- NEW FUNCTION: HAVERSINE DISTANCE ---
def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two points on a sphere 
    (Earth) using the Haversine formula.
    
    Arguments:
        lat1, lon1 (float): Latitude and Longitude of Point 1 (Decimal Degrees).
        lat2, lon2 (float): Latitude and Longitude of Point 2 (Decimal Degrees).

    Returns:
        float: Distance in meters.
    """
    # Convert decimal degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    
    lambda1 = math.radians(lon1)
    lambda2 = math.radians(lon2)

    # Delta latitude and longitude
    d_phi = phi2 - phi1
    d_lambda = lambda2 - lambda1
    
    # Haversine formula: a = sin²(Δφ/2) + cos(φ1) * cos(φ2) * sin²(Δλ/2)
    # The haversine function is defined as hav(θ) = sin²(θ/2)
    a = math.sin(d_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(d_lambda / 2)**2
        
    # Central angle: c = 2 * atan2(sqrt(a), sqrt(1-a))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance = R * c
    distance_meters = EARTH_RADIUS_METERS * c
    
    return distance_meters
# ----------------------------------------


def perform_action(option_name):
    """A function that is called by menu options 3-4."""
    print(f"\n-> You have selected '{option_name}'. This function has been called.\n")


def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        # Display the menu options
        print("--- Main Menu ---")
        print("1. Convert DMS to Decimal Degrees")
        print("2. Calculate Flat-Earth Distance (Pythagorean)")
        print("3. Calculate Great-Circle Distance (Haversine)") # Option 3 is now Haversine
        print("4. Call Option B") # Renamed from Option 3
        print("5. Call Option C") # Renamed from Option 4
        print("6. Exit Program") # Renamed from Option 5
        print("-----------------")

        # Get user input
        choice = input("Please enter your choice (1-6): ")

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
            # Flat-Earth Distance Block
            try:
                print("\nEnter coordinates for Point 1 (P1):")
                lat1 = float(input("Enter Latitude (e.g., 40.7128): "))
                lon1 = float(input("Enter Longitude (e.g., -74.0060): "))

                print("\nEnter coordinates for Point 2 (P2):")
                lat2 = float(input("Enter Latitude (e.g., 40.7130): "))
                lon2 = float(input("Enter Longitude (e.g., -74.0055): "))

                distance, angle, i_comp, j_comp = calculate_flat_distance(lat1, lon1, lat2, lon2)

                print("\n--- Results (Flat-Earth Approximation) ---")
                print(f"**Distance:** {distance:,.2f} meters")
                print(f"**Standard Angle:** {angle:.2f} degrees (0° = East, 90° = North)")
                print(f"**i Component (East/West):** {i_comp:,.2f} meters")
                print(f"**j Component (North/South):** {j_comp:,.2f} meters")
                print("------------------------------------------\n")

            except ValueError:
                print("\n! Error: Invalid input. Please ensure coordinates are numeric.\n")
            
        elif choice == "3":
            # --- NEW HAVERSINE FUNCTIONALITY BLOCK ---
            try:
                print("\nEnter coordinates for Point 1 (P1):")
                lat1 = float(input("Enter Latitude (e.g., 40.7128): "))
                lon1 = float(input("Enter Longitude (e.g., -74.0060): "))

                print("\nEnter coordinates for Point 2 (P2):")
                lat2 = float(input("Enter Latitude (e.g., 40.7130): "))
                lon2 = float(input("Enter Longitude (e.g., -74.0055): "))

                distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)

                print("\n--- Results (Haversine Great-Circle Distance) ---")
                print(f"**Distance:** {distance:,.2f} meters")
                print(f"**Approximation:** Assumes a perfect sphere with $R \approx 6,371\text{ km}$.")
                print("---------------------------------------------------\n")

            except ValueError:
                print("\n! Error: Invalid input. Please ensure coordinates are numeric.\n")
            # -------------------------------------------

        elif choice == "4":
            perform_action("Option B")
        elif choice == "5":
            perform_action("Option C")
        elif choice == "6":
            print("\nExiting the program. Goodbye! 👋")
            break  # Exit the while loop
        else:
            # Handle invalid input
            print(
                f"\n! Invalid input: '{choice}'. Please enter a number between 1 and 6.\n"
            )
        input("Press enter to continue...")

# Start the program by calling the main_menu function
main_menu()
