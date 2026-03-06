import streamlit as st
import random

st.set_page_config(page_title="Risk Averse Game", page_icon="🎲")
st.title("🎲 Risk Averse Game: Stage-by-Stage Choices")

# -----------------------------
# Initialize session state
# -----------------------------
if "stage" not in st.session_state:
    st.session_state.stage = 1
    st.session_state.user_choices = []
    st.session_state.stage_results = []
    st.session_state.A_values = [10, 10, 9]
    st.session_state.B_values = [0, 0, 20]
    st.session_state.B_alt_values = [19, 19, 19]
    st.session_state.P = [0.95, 0.95, 0.85]
    st.session_state.P_risk = [0.5, 0.5, 0.5]
    st.session_state.punishment_applied = False
    st.session_state.dice = random.randint(1, 6)
    st.session_state.user_dice = None
    st.session_state.truth_message = ""
    st.session_state.punishment_message = ""

PUNISHMENT = 0.33

# -----------------------------
# Restart Game
# -----------------------------
def restart_game():
    keys = ["stage","user_choices","stage_results","A_values","B_values",
            "punishment_applied","dice","user_dice","truth_message","punishment_message"]
    for k in keys:
        st.session_state.pop(k, None)

# -----------------------------
# Callback Functions
# -----------------------------
def choose_option(option):
    idx = st.session_state.stage - 1
    if option == "A":
        expected = st.session_state.P[idx]*st.session_state.A_values[idx] + (1-st.session_state.P[idx])*(st.session_state.A_values[idx]-1)
    else:
        expected = st.session_state.P_risk[idx]*st.session_state.B_values[idx] + (1-st.session_state.P_risk[idx])*st.session_state.B_alt_values[idx]
    st.session_state.stage_results.append(expected)
    st.session_state.user_choices.append(option)
    st.session_state.stage += 1

def submit_dice():
    st.session_state.user_dice = st.session_state.dice_input
    if st.session_state.user_dice == st.session_state.dice:
        st.session_state.truth_message = "✅ You told the truth. SAFE."
        st.session_state.punishment_message = ""
    else:
        st.session_state.truth_message = "⚠️ You lied!"
        if st.session_state.user_dice >= 5:
            st.session_state.punishment_applied = True
            st.session_state.punishment_message = f"Lie with punishment! (+{PUNISHMENT} to all stages)"
        else:
            st.session_state.punishment_message = "Lie without punishment."
    st.session_state.stage += 1

# -----------------------------
# Dice ASCII
# -----------------------------
dice_art = {
    1: "-----\n|   |\n| o |\n|   |\n-----",
    2: "-----\n|o  |\n|   |\n|  o|\n-----",
    3: "-----\n|o  |\n| o |\n|  o|\n-----",
    4: "-----\n|o o|\n|   |\n|o o|\n-----",
    5: "-----\n|o o|\n| o |\n|o o|\n-----",
    6: "-----\n|o o|\n|o o|\n|o o|\n-----",
}

# -----------------------------
# Stage Logic
# -----------------------------
stage = st.session_state.stage

# Stage 1-3: choose options
if stage <= 3:
    idx = stage - 1
    st.subheader(f"--- Stage {stage} ---")
    st.write(f"Option A (Safe Zone): {st.session_state.P[idx]*100:.0f}% of {st.session_state.A_values[idx]} OR {(1-st.session_state.P[idx])*100:.0f}% of {st.session_state.A_values[idx]-1}")
    st.write(f"Option B (Risk Zone): {st.session_state.P_risk[idx]*100:.0f}% of {st.session_state.B_values[idx]} OR {(1-st.session_state.P_risk[idx])*100:.0f}% of {st.session_state.B_alt_values[idx]}")
    col1, col2 = st.columns(2)
    col1.button("Choose Option A", on_click=choose_option, args=("A",))
    col2.button("Choose Option B", on_click=choose_option, args=("B",))

# Stage 4: Dice roll input
elif stage == 4:
    st.subheader("🎲 Dice Roll Stage")
    st.text(dice_art[st.session_state.dice])
    st.session_state.dice_input = st.number_input("Enter dice number (1-6, you may lie):", min_value=1, max_value=6, value=1)
    st.button("Submit Dice", on_click=submit_dice)

# Stage 5: Final results
elif stage == 5:
    # Apply punishment if player lied with >=5
    if st.session_state.punishment_applied:
        st.session_state.stage_results = [x + PUNISHMENT for x in st.session_state.stage_results]

    # Show truth/lie
    st.write(st.session_state.truth_message)
    if st.session_state.punishment_message:
        st.warning(st.session_state.punishment_message)

    st.subheader("📊 Stage Results (your choices after punishment if any)")
    for i, val in enumerate(st.session_state.stage_results,1):
        st.write(f"Stage {i} - Expected Value: {val:.2f} (Option {st.session_state.user_choices[i-1]})")

    st.success("✅ Game Finished. Thank you for playing!")
    st.button("🔄 Restart Game", on_click=restart_game)
