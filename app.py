import streamlit as st
import config
from utils import read, filter, score, freq

if "inputs" not in st.session_state:
    st.session_state.inputs = [["" for _ in range(5)] for _ in range(5)]
if "color_states" not in st.session_state:
    st.session_state.color_states = [["default" for _ in range(5)] for _ in range(5)]
if "active_row" not in st.session_state:
    st.session_state.active_row = 0
if "entered_words" not in st.session_state:
    st.session_state.entered_words = []
if "remaining_words" not in st.session_state:
    st.session_state.remaining_words = []
if "predicted_word" not in st.session_state:
    st.session_state.predicted_word = None


def submit():
    ''' Submits user input '''
    correct_place = {}
    remove_letters = set()
    remove_letters_posn = {}
    entered_word = ""

    for row in range(5):
        row_word = "".join(st.session_state.inputs[row]).strip().lower()
        if row_word: 
            entered_word = row_word

        for col in range(5):
            char = st.session_state.inputs[row][col].strip().lower()
            color = st.session_state.color_states[row][col]
            if color == "green" and char:
                correct_place[col] = char
            elif color == "gray" and char:
                remove_letters.add(char)
            elif color == "yellow" and char:
                if char not in remove_letters_posn:
                    remove_letters_posn[char] = []
                remove_letters_posn[char].append(col)

    exclude_positions = set(correct_place.keys())

    words = read(config.WORD_LIST_PATH)
    frequencies = freq(words)
    filtered_words = filter(words, correct_place, remove_letters, remove_letters_posn)
    sorted_filtered_words = score(filtered_words, frequencies, exclude_positions)

    # store the current word entry and remaining words count
    if entered_word:
        st.session_state.entered_words.append(entered_word)
        st.session_state.remaining_words.append(len(sorted_filtered_words))

    if sorted_filtered_words:
        st.session_state.predicted_word = sorted_filtered_words[:4]
    else:
        st.session_state.predicted_word = None


def do_submit():
    submit()
    st.session_state.active_row = min(st.session_state.active_row + 1, 4)


def main():
    st.set_page_config(page_title="Wordle Solver", page_icon="🍓", layout="centered")
    st.markdown(
        # css by chatgippity cuz im too old for this
        """
        <style>
        /* Import Jost font */
        @import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;700&display=swap');

        :root {
          --primary: #6aaa64;
          --bg: #121213;
          --fg: #ffffff;
          --font: 'Jost', sans-serif;
        }

        /* Darken toolbar, app container, and sidebar */
        header, section[data-testid="stToolbar"],
        [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
          background-color: var(--bg) !important;
          color: var(--fg) !important;
          font-family: var(--font) !important;
        }

        /* Panel backgrounds */
        .css-1d391kg, .css-1v3fvcr {
          background-color: #3a3a3c !important;
        }

        /* Button styling */
        .stButton > button {
          background-color: var(--primary) !important;
          color: var(--fg) !important;
        }

        /* Custom title */
        .custom-title {
          color: var(--primary) !important;
          font-family: var(--font) !important;
        }

        /* Hide Streamlit footer */
        footer {
          visibility: hidden;
        }

        /* Enlarge and center the custom title */
        .custom-title {
          font-size: 5rem !important;
          text-align: center !important;
          margin: 1rem auto !important;
        }

        /* Sidebar instruction default styling */
        [data-testid="stSidebar"] p {
            background-color: rgba(255,255,255,0.05) !important;
            color: var(--fg) !important;
            padding: 0.75rem !important;
            border-radius: 4px !important;
            margin-bottom: 0.5rem !important;
        }
        /* Sidebar instruction hover styling */
        [data-testid="stSidebar"] p:hover {
            background-color: rgba(255,255,255,0.15) !important;
        }

        /* Subtle separator between sidebar and main */
        [data-testid="stSidebar"] {
          border-right: 1px solid rgba(255,255,255,0.2) !important;
        }

        /* Style select dropdown boxes to mimic tile size and Wordle colors */
        div[role="combobox"] {
          width: 3em !important;
          height: 3em !important;
        }
        div[role="combobox"] > div {
          background-color: var(--secondary-background-color) !important;
          color: var(--primary) !important;
          border-radius: 4px !important;
          text-align: center !important;
          padding: 0.5rem !important;
          font-family: var(--font) !important;
        }
        /* Style the dropdown arrow */
        div[role="combobox"] svg {
          fill: var(--primary) !important;
        }
        /* Tile transition */
        div[style*="width:3em"][style*="height:3em"] {
          transition: background-color 0.8s ease, color 0.8s ease;
        }
        /* Button hover effect */
        .stButton > button {
          transition: background-color 0.8s ease, transform 0.8s ease;
        }
        .stButton > button:hover {
          transform: translateY(-2px);
        }
        /* Center all Streamlit buttons */
        .stButton {
          display: flex !important;
          justify-content: center !important;
        }

        /* Pop-in animation for predictions */
        @keyframes popin {
          0% { transform: scale(0.8); opacity: 0; }
          100% { transform: scale(1); opacity: 1; }
        }
        .predictions {
          animation: popin 150ms ease-out forwards;
          font-family: var(--font) !important;
          font-weight: 200 !important;
          color: var(--primary) !important;
        }

        /* Dropdown options slide-down */
        @keyframes slideDown {
          0% { transform: translateY(-10%); opacity: 0; }
          100% { transform: translateY(0); opacity: 1; }
        }
        div[role="listbox"] div {
          animation: slideDown 200ms ease-out forwards;
        }

        /* Button press feedback */
        .stButton > button:active {
          transform: scale(0.95) !important;
        }

        /* Grid container for rows */
        .grid-container {
          display: grid;
          grid-template-columns: repeat(5, 3em);
          grid-gap: 0.5em;
          justify-content: center;
          margin-bottom: 0.5rem;
        }
        .grid-cell {
          width: 3em; height: 3em;
          line-height: 3em; text-align: center;
          font-weight: bold;
          border-radius: 4px;
        }
        /* Mobile font scaling */
        @media (max-width: 480px) {
          .predictions {
            font-size: 1.5rem !important;
          }
          .custom-title {
            font-size: 3rem !important;
          }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="custom-title">Wordle Solver</div>', unsafe_allow_html=True)

    # display predicted word 
    if st.session_state.predicted_word:
            preds = ", ".join([w.upper() for w in st.session_state.predicted_word])
            st.markdown(
                f"<h2 class='predictions' style='text-align: center;'>Predictions: {preds}</h2>",
                unsafe_allow_html=True
            )
    elif st.session_state.predicted_word is not None:
        st.markdown(
            "<h2 style='text-align: center; color: red;'>No words match the criteria!</h2>",
            unsafe_allow_html=True
        )

    for row in range(5):
        if row < st.session_state.active_row:
            # Static completed row as HTML grid
            row_html = "<div class='grid-container'>"
            for col in range(5):
                letter = st.session_state.inputs[row][col].upper()
                color = st.session_state.color_states[row][col]
                color_map = {
                    "default": "#d3a3a3c",
                    "gray": "#787c7e",
                    "yellow": "#c9b458",
                    "green": "#6aaa64"
                }
                row_html += (
                    f"<div class='grid-cell' "
                    f"style='background:{color_map[color]};color:#ffffff;'>"
                    f"{letter}</div>"
                )
            row_html += "</div>"
            st.markdown(row_html, unsafe_allow_html=True)
        # active row: clickable cells
        elif row == st.session_state.active_row:
            cols = st.columns(5)
            for col in range(5):
                with cols[col]:
                    # letter input
                    key_in = f"cell_input_{row}_{col}"
                    letter = st.text_input("", max_chars=1, key=key_in, label_visibility="collapsed").strip().upper()
                    if letter and letter.isalpha():
                        st.session_state.inputs[row][col] = letter.lower()
                    # color selector dropdown
                    color_key = f"color_select_{row}_{col}"
                    color_options = ["⬜ default", "⬛ gray", "🟨 yellow", "🟩 green"]
                    current_state = st.session_state.color_states[row][col]
                    initial_choice = next(opt for opt in color_options if opt.endswith(current_state))
                    if color_key not in st.session_state:
                        # First render: set via index (Glitching FIX)
                        choice = st.selectbox(
                            "",
                            color_options,
                            index=color_options.index(initial_choice),
                            key=color_key,
                            label_visibility="collapsed"
                        )
                    else:
                        # Subsequent renders: use stored value
                        choice = st.selectbox(
                            "",
                            color_options,
                            key=color_key,
                            label_visibility="collapsed"
                        )
                    st.session_state.color_states[row][col] = choice.split()[-1]

    # Centered submit button using on_click for immediate effect
    btn_cols = st.columns([1,2,1])
    with btn_cols[1]:
        st.button("Submit", on_click=do_submit)
    
    
    st.sidebar.header("How to Use the Solver")
    st.sidebar.markdown(
        """
        **1.** Type your 5-letter guess in the active row.

        **2.** For each tile, choose the feedback via the dropdown:  
        &nbsp;&nbsp;⬜ default &nbsp; ⬛ gray &nbsp; 🟨 yellow &nbsp; 🟩 green  

        **3.** Click **Submit** to get new suggestions.
        """
    )
    st.sidebar.title("Statistics")
    st.sidebar.write(f"- Words Entered: {len(st.session_state.entered_words)}")
    st.sidebar.write(f"- Remaining Words: {st.session_state.remaining_words[-1] if st.session_state.remaining_words else 'N/A'}")



if __name__ == "__main__":
    main()