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
    st.session_state.A_values = [10, 10, 9]
    st.session_state.B_values = [0, 0, 20]  # For Risk Option
    st.session_state.B_alt_values = [19, 19, 19]  # Risk high value
    st.session_state.P = [0.95, 0.95, 0.85]  # Probabilities for Option A
    st.session_state.P_risk = [0.5, 0.5, 0.5]  # Probabilities for Option B
    st.session_state.punishment = 0.33
    st.session_state.dice = random.randint(1, 6)
    st.session_state.user_dice = None
    st.session_state.punishment_applied = False
    st.session_state.stage_results = []

# -----------------------------
# Restart callback
# -----------------------------
def restart_game():
    keys = ["stage", "user_choices","A_values","B_values","stage_results",
            "dice","user_dice","punishment_applied"]
    for k in keys:
        st.session_state.pop(k, None)

# -----------------------------
# Stage-by-stage choices
# -----------------------------
stage = st.session_state.stage

if stage <= 3:
    st.subheader(f"--- Stage {stage} ---")

    # Show Option A probabilities
    A_prob_text = f"Option A (Safe Zone): {st.session_state.P[stage-1]*100:.0f}% of {st.session_state.A_values[stage-1]} OR {(1-st.session_state.P[stage-1])*100:.0f}% of {st.session_state.A_values[stage-1]-1}"
    st.write(A_prob_text)

    # Show Option B probabilities
    B_prob_text = f"Option B (Risk Zone): {st.session_state.P_risk[stage-1]*100:.0f}% of {st.session_state.B_values[stage-1]} OR {(1-st.session_state.P_risk[stage-1])*100:.0f}% of {st.session_state.B_alt_values[stage-1]}"
    st.write(B_prob_text)

    # Player chooses Option A or B
    col1, col2 = st.columns(2)
    if col1.button("Choose Option A"):
        st.session_state.user_choices.append("A")
        # Compute expected value for stage and store
        expected = st.session_state.P[stage-1]*st.session_state.A_values[stage-1] + (1-st.session_state.P[stage-1])*(st.session_state.A_values[stage-1]-1)
        st.session_state.stage_results.append(expected)
        st.session_state.stage += 1

    if col2.button("Choose Option B"):
        st.session_state.user_choices.append("B")
        # Compute expected value for stage and store
        expected = st.session_state.P_risk[stage-1]*st.session_state.B_values[stage-1] + (1-st.session_state.P_risk[stage-1])*st.session_state.B_alt_values[stage-1]
        st.session_state.stage_results.append(expected)
        st.session_state.stage += 1

# -----------------------------
# Dice Roll / Truth or Lie
# -----------------------------
elif stage == 4:
    st.subheader("🎲 Dice Roll Stage")
    st.write("The dice has been rolled!")
    dice_art = {
        1: "-----\n|   |\n| o |\n|   |\n-----",
        2: "-----\n|o  |\n|   |\n|  o|\n-----",
        3: "-----\n|o  |\n| o |\n|  o|\n-----",
        4: "-----\n|o o|\n|   |\n|o o|\n-----",
        5: "-----\n|o o|\n| o |\n|o o|\n-----",
        6: "-----\n|o o|\n|o o|\n|o o|\n-----",
    }
    st.text(dice_art[st.session_state.dice])
    st.session_state.user_dice = st.number_input("Declare the dice number (1-6, you may lie):", min_value=1, max_value=6, value=1)
    if st.button("Submit Dice"):
        if st.session_state.user_dice == st.session_state.dice:
            st.success("✅ You told the truth. SAFE.")
        else:
            st.warning("⚠️ You lied!")
            if st.session_state.user_dice >= 5:
                st.session_state.punishment_applied = True
                st.error("Lie with punishment! (+0.33 to all stages)")
        st.session_state.stage += 1

# -----------------------------
# Show Final Results
# -----------------------------
elif stage == 5:
    # Apply punishment if needed
    if st.session_state.punishment_applied:
        st.session_state.stage_results = [x + st.session_state.punishment for x in st.session_state.stage_results]

    st.subheader("📊 Stage Results")
    for i, val in enumerate(st.session_state.stage_results,1):
        st.write(f"Stage {i} - Expected Value of your choice: {val:.2f} (Option {st.session_state.user_choices[i-1]})")

    st.success("✅ Game Finished. Thank you for playing!")
    st.button("🔄 Restart Game", on_click=restart_game)
