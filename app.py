import streamlit as st
import random

st.set_page_config(page_title="Risk Averse Game", page_icon="🎲")
st.title("🎲 Risk Averse Game: Risk vs Safe Choices")
st.write("At each stage, choose Option A (Safe) or Option B (Risk) based on the numbers shown.")

# Initialize session state
if "stage" not in st.session_state:
    st.session_state.stage = 1
    st.session_state.user_choices = []
    st.session_state.A_values = [10, 10, 9]
    st.session_state.B_values = [9.5, 9.5, 9.5]
    st.session_state.punishment_applied = False
    st.session_state.dice = random.randint(1, 6)
    st.session_state.user_dice = None

PUNISHMENT = 0.33

# Dice ASCII art
dice_art = {
    1: "-----\n|   |\n| o |\n|   |\n-----",
    2: "-----\n|o  |\n|   |\n|  o|\n-----",
    3: "-----\n|o  |\n| o |\n|  o|\n-----",
    4: "-----\n|o o|\n|   |\n|o o|\n-----",
    5: "-----\n|o o|\n| o |\n|o o|\n-----",
    6: "-----\n|o o|\n|o o|\n|o o|\n-----",
}

# Callback for choosing options
def choose_option(option):
    st.session_state.user_choices.append(option)
    st.session_state.stage += 1

# Callback for dice submission
def submit_dice():
    st.session_state.user_dice = st.session_state.dice_input
    if st.session_state.user_dice == st.session_state.dice:
        st.session_state.truth_message = "✅ You told the truth. SAFE."
        st.session_state.punishment_message = ""
    else:
        st.session_state.truth_message = "⚠️ You lied!"
        if st.session_state.user_dice >= 5:
            st.session_state.punishment_applied = True
            st.session_state.punishment_message = "Lie with punishment! (+0.33 to all stages)"
        else:
            st.session_state.punishment_message = "Lie without punishment."
    st.session_state.stage += 1

# Restart callback
def restart_game():
    for key in ["stage","user_choices","A_values","B_values","punishment_applied","dice","user_dice"]:
        st.session_state.pop(key, None)

# -----------------------------
# Stage 1-3: Show numbers and let player choose
# -----------------------------
if st.session_state.stage in [1,2,3]:
    idx = st.session_state.stage - 1
    st.subheader(f"--- Stage {st.session_state.stage} ---")
    st.write(f"Option A (Safe): {st.session_state.A_values[idx]:.2f}")
    st.write(f"Option B (Risk): {st.session_state.B_values[idx]:.2f}")
    st.write("Choose your option:")
    col1, col2 = st.columns(2)
    col1.button("Option A", on_click=choose_option, args=("A",))
    col2.button("Option B", on_click=choose_option, args=("B",))

# Stage 4: Dice roll
elif st.session_state.stage == 4:
    st.subheader("🎲 Dice Roll Stage")
    st.write("The dice has been rolled!")
    st.text(dice_art[st.session_state.dice])
    st.session_state.dice_input = st.number_input("Enter the dice number you want to declare (1-6, you may lie)", min_value=1, max_value=6, value=1)
    st.button("Submit Dice", on_click=submit_dice)

# Stage 5: Apply punishment and show final results
elif st.session_state.stage == 5:
    if st.session_state.punishment_applied:
        for i in range(3):
            st.session_state.A_values[i] += PUNISHMENT
            st.session_state.B_values[i] += PUNISHMENT

    st.write(st.session_state.truth_message)
    if st.session_state.punishment_message:
        st.warning(st.session_state.punishment_message)

    # Show final values
    st.subheader("📊 Final Values")
    for i in range(3):
        st.write(f"Stage {i+1}: Option A = {st.session_state.A_values[i]:.2f}, Option B = {st.session_state.B_values[i]:.2f}")

    # Show winners
    st.subheader("🏆 Winners by Stage")
    for i in range(3):
        if st.session_state.A_values[i] > st.session_state.B_values[i]:
            winner = "Option A"
        elif st.session_state.B_values[i] > st.session_state.A_values[i]:
            winner = "Option B"
        else:
            winner = "Draw"
        st.write(f"Stage {i+1} Winner: {winner}")

    # Show user choices
    st.subheader("🎮 Your Choices")
    for i, choice in enumerate(st.session_state.user_choices, 1):
        st.write(f"Stage {i}: Option {choice}")

    st.success("✅ Game Finished. Thank you for playing!")
    st.button("🔄 Restart Game", on_click=restart_game)
