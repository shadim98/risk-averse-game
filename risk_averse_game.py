import random

print("===================================")
print("      Welcome to Risk Averse Game")
print("===================================\n")


# -----------------------------------
# Stage Values (Expected Values)
# -----------------------------------

A_values = [10, 10, 9]  # Option A
B_values = [9.5, 9.5, 9.5]  # Option B
PUNISHMENT = 0.33


# -----------------------------------
# Show Rules
# -----------------------------------

print("Game Rules:\n")

print("Option A (Safe Zone):")
print(" Stage 1: 95% of 10 OR 5% of 9")
print(" Stage 2: 95% of 10 OR 5% of 9")
print(" Stage 3: 85% of 10 OR 15% of 9\n")

print("Option B (Risk Zone):")
print(" Stage 1: 50% of 0 OR 50% of 19")
print(" Stage 2: 50% of 0 OR 50% of 19")
print(" Stage 3: 50% of 20 OR 50% of 19\n")


# -----------------------------------
# User Choice in Each Stage
# -----------------------------------

user_choices = []

for stage in range(3):
    print(f"--- Stage {stage + 1} ---")
    print("Choose Option A or B")
    choice = input("Enter A or B: ").upper()
    while choice not in ["A", "B"]:
        print("Invalid choice! Please enter A or B.")
        choice = input("Enter A or B: ").upper()
    user_choices.append(choice)
    print()


# -----------------------------------
# Roll Dice
# -----------------------------------

dice = random.randint(1, 6)

print("\nDice Rolled:")

dice_art = {
    1: """
    -----
    |   |
    | o |
    |   |
    -----
    """,
    2: """
    -----
    |o  |
    |   |
    |  o|
    -----
    """,
    3: """
    -----
    |o  |
    | o |
    |  o|
    -----
    """,
    4: """
    -----
    |o o|
    |   |
    |o o|
    -----
    """,
    5: """
    -----
    |o o|
    | o |
    |o o|
    -----
    """,
    6: """
    -----
    |o o|
    |o o|
    |o o|
    -----
    """
}

print(dice_art[dice])


# -----------------------------------
# User Dice Input (Safe Input)
# -----------------------------------

while True:
    try:
        user_dice = int(input("Enter the dice number (you can lie): "))
        if 1 <= user_dice <= 6:
            break
        else:
            print("Please enter a number between 1 and 6.")
    except ValueError:
        print("Invalid input. Enter a number.")


# -----------------------------------
# Truth or Lie Check (BOLD and Separate)
# -----------------------------------

print("\n\033[1m===== TRUTH OR LIE CHECK =====\033[0m\n")  # Bold Header

def truth_or_lie_check(real_dice, user_dice):
    punishment = False
    if user_dice == real_dice:
        print("\033[1mYou told the truth. SAFE.\033[0m\n")
    else:
        print("\033[1mYou lied!\033[0m")
        if user_dice >= 5:
            print("\033[1mLie with punishment!\033[0m")
            punishment = True
        else:
            print("\033[1mLie without punishment.\033[0m")
    return punishment

punishment_applied = truth_or_lie_check(dice, user_dice)


# -----------------------------------
# Apply Punishment
# -----------------------------------

if punishment_applied:
    for i in range(3):
        A_values[i] += PUNISHMENT
        B_values[i] += PUNISHMENT
    print("\n\033[1mPunishment added (+0.33 to all stages)\033[0m\n")


# -----------------------------------
# Show Final Values
# -----------------------------------

print("Final Values:")

print("\nOption A:")
for i in range(3):
    print(f" Stage {i+1}: {A_values[i]:.2f}")

print("\nOption B:")
for i in range(3):
    print(f" Stage {i+1}: {B_values[i]:.2f}")


# -----------------------------------
# Final Result
# -----------------------------------

print("\n==============================")
print("        Final Results")
print("==============================\n")

for i in range(3):
    print(f"Stage {i+1}:")
    print(f" Option A: {A_values[i]:.2f}")
    print(f" Option B: {B_values[i]:.2f}")
    if A_values[i] > B_values[i]:
        print(" Winner: Option A")
    elif B_values[i] > A_values[i]:
        print(" Winner: Option B")
    else:
        print(" Result: Draw")
    print()


# -----------------------------------
# Show User Choices
# -----------------------------------

print("Your Choices:")
for i in range(3):
    print(f" Stage {i+1}: Option {user_choices[i]}")

print("\nGame Finished. Thank you for playing!")
