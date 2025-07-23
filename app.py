import streamlit as st
import pandas as pd

# Constants
MIN_REPS = 4
MAX_REPS = 20
MIN_SETS = 2
MAX_SETS = 6

# Weekly progression pattern
def get_weekly_weights(start_weight):
    return [start_weight, start_weight + 2, start_weight + 4, start_weight + 5]

# Define exercises for each day
workout_plan = {
    "Day 1": ["Deadlift", "Row", "Flat bench", "Shoulder press", "Leg raise", "Standing calf raise", "Bicep curls"],
    "Day 2": ["Squat", "Pulldowns", "Incline bench", "Seated calf raises", "Machine ab crunch", "Lateral raises + Front raises", "Overhead tricep extensions"],
    "Day 3": ["Leg press", "Leg curl", "Chest fly", "Low row", "Shoulder press", "Forearms (front)", "Forearms (back)"]
}

# Initialize session state
if "cycle" not in st.session_state:
    st.session_state.cycle = 1
if "week" not in st.session_state:
    st.session_state.week = 1
if "weights" not in st.session_state:
    st.session_state.weights = {day: {ex: 100.0 for ex in exercises} for day, exercises in workout_plan.items()}
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🏋️ Workout Progress Tracker")

# Select workout day
selected_day = st.selectbox("Select Workout Day", list(workout_plan.keys()))
st.subheader(f"Cycle {st.session_state.cycle} - Week {st.session_state.week} - {selected_day}")

# Display input form
form = st.form(key="workout_form")
inputs = {}
for exercise in workout_plan[selected_day]:
    base_weight = st.session_state.weights[selected_day][exercise]
    expected_weight = float(get_weekly_weights(base_weight)[st.session_state.week - 1])
    col1, col2, col3, col4 = form.columns(4)
    with col1:
        sets = form.number_input(f"{exercise} - Sets", min_value=MIN_SETS, max_value=MAX_SETS, value=3, key=f"{exercise}_sets")
    with col2:
        reps = form.number_input(f"{exercise} - Reps", min_value=MIN_REPS, max_value=MAX_REPS, value=10, key=f"{exercise}_reps")
    with col3:
        weight = form.number_input(f"{exercise} - Actual Weight", min_value=0.0, value=expected_weight, step=0.5, key=f"{exercise}_weight")
    with col4:
        form.markdown(f"**Expected: {expected_weight:.1f} lb**")
    inputs[exercise] = {"sets": sets, "reps": reps, "weight": weight, "expected": expected_weight}

submitted = form.form_submit_button("Submit Workout")

# Process submission
if submitted:
    day_history = []
    for exercise, data in inputs.items():
        volume = data["sets"] * data["reps"] * data["weight"]
        expected_volume = data["sets"] * data["reps"] * data["expected"]
        day_history.append({
            "Cycle": st.session_state.cycle,
            "Week": st.session_state.week,
            "Day": selected_day,
            "Exercise": exercise,
            "Sets": data["sets"],
            "Reps": data["reps"],
            "Weight": data["weight"],
            "Expected Weight": data["expected"],
            "Volume": volume,
            "Expected Volume": expected_volume
        })
        # Update base weight for next cycle if actual volume >= expected
        if volume >= expected_volume and st.session_state.week == 4:
            st.session_state.weights[selected_day][exercise] += 2.0

    st.session_state.history.extend(day_history)

    # Advance week and cycle
    if st.session_state.week < 4:
        st.session_state.week += 1
    else:
        st.session_state.week = 1
        st.session_state.cycle += 1

    st.success("Workout submitted and progress updated!")

# Display history
if st.session_state.history:
    st.subheader("📈 Workout History")
    df_history = pd.DataFrame(st.session_state.history)
    st.dataframe(df_history)
