import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import timedelta
import random
from exam_functions import *
from streamlit_option_menu import option_menu
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.app_logo import add_logo
from streamlit_extras.let_it_rain import rain
from streamlit_gsheets import GSheetsConnection
from pathlib import Path


def show_countdown(deadline):
    # Calculate the remaining time in seconds
    # deadline = datetime.datetime.strptime(deadline, '%d/%m/%Y, %H:%M:%S')
    now = datetime.datetime.now()
    time_left = int((deadline - now).total_seconds())
    if time_left < 0:
        time_left = 0

    # JavaScript and HTML for countdown
    countdown_html = f"""
    <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; font-family: 'Roboto', 'sans-serif'; font-size: 1.5rem; font-weight: 600; color: #31333f;">
        <div id="countdown" style="text-align: center;">Loading...</div>
    </div>

    <script>
    var timeLeft = {time_left};
    var countdownElement = document.getElementById('countdown');

    function updateCountdown() {{
        var days = Math.floor(timeLeft / (60 * 60 * 24));
        var hours = Math.floor((timeLeft % (60 * 60 * 24)) / (60 * 60));
        var minutes = Math.floor((timeLeft % (60 * 60)) / 60);
        var seconds = Math.floor(timeLeft % 60);

        countdownElement.innerHTML = 
            "Time Remaining ⏳: " + days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

        if (timeLeft <= 0) {{
            clearInterval(timer);
            countdownElement.innerHTML = "⏰ Time's up!";
            countdownElement.style.color = "red";  // Change text color to red
            window.parent.postMessage({{ type: 'TIME_UP' }}, '*');
        }}
        timeLeft--;
    }}

    var timer = setInterval(updateCountdown, 1000);
    updateCountdown();
    </script>
    """

    # Display the countdown
    components.html(countdown_html, height=120)

    # Initialize session state for time_up
    if 'time_up' not in st.session_state:
        st.session_state.time_up = False

    # JavaScript to listen for the TIME_UP message
    components.html("""
    <script>
    window.addEventListener('message', (event) => {
        if (event.data.type === 'TIME_UP') {
            const streamlitEvent = new CustomEvent("streamlit:rerun");
            window.parent.document.dispatchEvent(streamlitEvent);
        }
    });
    </script>
    """, height=0)

    # Check if time is up
    if time_left == 0:
        st.session_state.time_up = True

THIS_DIR = Path(__file__).parent
ASSETS = THIS_DIR / "assets"
LOGO = ASSETS / "savila_games_logo.png"

st.set_page_config(
        page_title='AGILE PM 13767 FINAL EXAM', # agregamos el nombre de la pagina, este se ve en el browser
        page_icon='📅' # se agrega el favicon, tambien este se ve en el browser
    )


if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ''

if 'first_name' not in st.session_state:
    st.session_state['first_name'] = ''

if 'last_name' not in st.session_state:
    st.session_state['last_name'] = ''

if 'password' not in st.session_state:
    st.session_state['password'] = ''

if 'n_submissions' not in st.session_state:
    st.session_state['n_submissions'] = ''

if 'student_seed' not in st.session_state:
    st.session_state['student_seed'] = ''

if 'student_deadline' not in st.session_state:
    st.session_state['student_deadline'] = ''

if 'student_answers' not in st.session_state:
    st.session_state['student_answers'] = ''

if 'student_grade' not in st.session_state:
    st.session_state['student_grade'] = 0

# Initialize session state for time_up
if 'time_up' not in st.session_state:
    st.session_state.time_up = False

if 'disable_submit' not in st.session_state:
    st.session_state['disable_submit'] = False



# ------------------------------------------------------------------------
# Disable copy pasting
# ------------------------------------------------------------------------ 

# --- Place this at the very top of your app to deactivate copy pasting---
disable_copy_js = """
<style>
body {
    -webkit-user-select: none; /* Safari */
    -moz-user-select: none;    /* Firefox */
    -ms-user-select: none;     /* IE10+/Edge */
    user-select: none;         /* Standard */
}
</style>
<script>
document.addEventListener('contextmenu', event => event.preventDefault());
</script>
"""

st.markdown(disable_copy_js, unsafe_allow_html=True)

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

# Countdown & sidebar options

# Set your deadline here
# deadline = datetime.datetime(2025, 4, 28, 10, 55)  # Example: April 28, 2025, 15:00

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------ 

login = None
df_n_cols = 24

with st.sidebar:
    # st.image("./assets/savila_games_logo.png")
    st.image("./IESEG_logo.png")
    selected = option_menu(
        menu_title='AGILE PM 3736',
        options= ['Login','Exam'],
        icons=['bi bi-person-fill-lock', '123'], menu_icon="cast"
    )
    
    add_vertical_space(1) 

    if selected == 'Login' and st.session_state['user_name'] == '':

        user_name = st.text_input('User email', placeholder = 'username@ieseg.fr')
    #st.caption('Please enter your IESEG email address')
        password =  st.text_input('Password', placeholder = '12345678',type="password")
        login = st.button("Login", type="primary")
        add_vertical_space(1)

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
users_existing_data =  conn.read(worksheet="users", usecols=list(range(8)), ttl=1)
users_existing_data = users_existing_data.dropna(how="all")
users_existing_data.index = users_existing_data['email']

gs_user_db = users_existing_data.T.to_dict()

# st.write(gs_user_db)

#---------------------------------------------
# Question bank
#---------------------------------------------


if selected == 'Login':
    st.title('📘 Agile Project Management 3767 Exam')
    st.header('Welcome to your Final Exam')
    # if login:
        # show_countdown(st.session_state['student_deadline'])

if login:
    if user_name not in gs_user_db.keys():
        st.error('Username not registered')
    else:
        real_password = gs_user_db[user_name]['password']
        if password.lower() != real_password:
            st.error('Sorry wrong password')
        else:
            user_first_name = gs_user_db[user_name]['name']
            user_last_name = gs_user_db[user_name]['last name']
            group = gs_user_db[user_name]['group']
            student_seed = int(gs_user_db[user_name]['seed'])
            student_n_submissions = int(gs_user_db[user_name]['n_submissions'])
            student_deadline = gs_user_db[user_name]['deadline']
            student_deadline = datetime.datetime.strptime(student_deadline, '%d/%m/%Y, %H:%M:%S')
            # print(student_deadline, type(student_deadline))

            st.session_state['user_name'] = user_name
            st.session_state['first_name'] = user_first_name
            st.session_state['last_name'] = user_last_name
            st.session_state['password'] = real_password
            st.session_state['group'] =  group
            st.session_state['n_submissions'] = student_n_submissions
            st.session_state['student_seed'] = student_seed
            st.session_state['student_deadline'] = student_deadline

            # show_countdown(st.session_state['student_deadline'])

            with st.sidebar:
                st.success(f'{user_first_name} - ({student_seed}) from group ({group}) succesfully log-in', icon="✅")

if selected == 'Login':
    if login:
        st.markdown(f"Welcome {st.session_state['first_name']} {st.session_state['last_name']} ✅")
        st.markdown("Please click on the \"Exam\" tab to start your exam")

with st.sidebar:
    if st.session_state['user_name'] != '':
        st.write(f"User: {st.session_state['user_name']} - ({st.session_state['student_seed']})")
        st.write(f"Group: {st.session_state['group']} ")
        logout = st.button('Logout')
        if logout:
            st.session_state['user_name'] = ''
            st.session_state['password'] = ''
            st.session_state['group'] = ''
            st.session_state['n_submissions'] = ''
            st.session_state['student_deadline'] = ''
            st.session_state['student_seed'] = ''
            st.session_state['student_answers'] = ''
            st.session_state['time_up'] = False
            st.session_state['first_name'] = ''
            st.session_state['last_name'] = ''
            st.session_state['student_grade'] = 0
            st.rerun()
    else:
        st.write(f"User: Not logged in ")

if selected == 'Exam':

    st.session_state['disable_submit'] = False
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

# Quiz

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------ 
    if st.session_state['user_name'] == '':
        st.warning('Please log in to be able to submit your project solution')
    else:

        seed = st.session_state['student_seed']
        show_countdown(st.session_state['student_deadline'])

        question_funcs = [
            ("Forecasting with Average Velocity", question_forecasting_release_date_average, seed),
            ("Forecasting with Optimistic Velocity", question_forecasting_release_date_optimistic, seed),
            ("Forecasting with Pessimistic Velocity",question_forecasting_release_date_pessimistic,seed),
            ("Forecasting Backlog Increase",question_forecasting_release_date_backlog_increase,seed),
            ("Forecasting Decision to hire more resources",question_forecasting_release_date_roi_new_team_member,seed),
            ("Upper Control Limit Velocity",question_control_limits_ucl,seed),
            ("Lower Control Limit Velocity",question_control_limits_lcl,seed),
            ("Investigation with Control Limits",question_control_limits_investigation,seed),
            ("Little's Law Cicle Time",question_littles_law_1,seed),
            ("Little's Law Throughput",question_littles_law_2,seed),
            ("Kanban Bottleneck detection",question_kanban_bottleneck,seed),
            ("Kanban Throughput estimation",question_kanban_throughput_estimation,seed),
            ("Kanban average WIP",question_kanban_average_wip,seed),
            ("Kanban Cycle Time",question_kanban_cycle_time,seed),
            ("VUT utilization",question_kingman_utilization,seed),
            ("VUT Queue Time",question_kingman_wait_time,seed),
            ("VUT WIP in Queue",question_kingman_inventory_in_line,seed),
            ("VUT Total Time",question_kingman_total_time,seed),
            ("VUT Total WIP",question_kingman_inventory_total,seed),
            ("VUT resource estimation",question_kingman_team_size,seed)
        ]

        st.title("📘 Agile Project Management 3767 Exam")

        logs_df = conn.read(worksheet="exam", usecols=list(range(df_n_cols)), ttl=1).dropna(how="all")
        n_submissions = len(logs_df[logs_df['user'] == st.session_state['user_name']])

        if not st.session_state.time_up:
            if n_submissions < st.session_state['n_submissions']:
                with st.form("quiz_form"):
                    st.markdown("## Please answer all questions and click **Submit** when done.")

                    user_answers = {}
                    correct_answers = {}

                    ref = 0
                    for i, (title, func, seed) in enumerate(question_funcs):
                        question = func(seed)

                        display_mode = question.get("display_mode", "full_text")  # default to full_text

                        with st.expander(f"#### Q{i+1}: {title}"):

                        # st.markdown(f"#### Q{i+1}: {title}")

                            if display_mode == "table":

                                st.markdown(question['question_half_1'])
                                st.dataframe(question['data']['df'], use_container_width=True)
                                st.markdown(question['question_half_2'])
                            
                            elif display_mode == "full_text":
                                st.markdown(question['question'])

                            options = question['options']  # {date: letter}
                            answer = question['answer']
                            correct_answers[i] = answer

                            # Build display options: "a) 13-06-2027" -> "13-06-2027"
                            display_options = {f"{letter}) {date}": date for date, letter in options.items()}

                            selected_display = st.radio(
                                f"Choose your answer for Q{i+1+ref}:",
                                options=list(display_options.keys()),
                                key=f"q{i}"
                            )

                            # Save selected date directly
                            user_answers[i] = display_options[selected_display]
                        add_vertical_space(1)

                    submitted = st.form_submit_button(
                                        label="Submit",
                                        disabled = st.session_state.time_up
                                        )

                    if submitted:
                        with st.spinner("Submitting results..."):
                            timestamp = datetime.datetime.now()
                            timestamp = timestamp.strftime("%d/%m/%Y, %H:%M:%S")
                            solution_dict = dict()
                            score = 0
                            solution_dict['user'] = st.session_state['user_name']
                            solution_dict['group'] = st.session_state['group']
                            solution_dict['time'] = timestamp
                            for i in user_answers:
                                user_ans = user_answers[i]
                                correct_ans = correct_answers[i]
                                solution_dict[f'Q{i+1}'] = user_ans
                                is_correct = user_ans == correct_ans
                                score += int(is_correct)
                            solution_dict['Grade'] = score
                            st.session_state['student_grade'] = score
                            logs_df = conn.read(worksheet="exam", usecols=list(range(df_n_cols)), ttl=1).dropna(how="all")


                            solution = pd.DataFrame([solution_dict])
                            updated_log = pd.concat([logs_df,solution],ignore_index=True)
                            conn.update(worksheet="exam",data = updated_log)

                            st.success(f"✅ Your quiz has been submitted successfully! on {timestamp}")
                            st.balloons()
                            valid_submission = True

                        add_vertical_space(1)
                        with st.expander(f"#### Results ({st.session_state['student_grade']}/20)"):
                            st.subheader("")

                            # print(user_answers)
                            # print(correct_answers)

                            score = 0
                            for i in user_answers:
                                user_ans = user_answers[i]
                                correct_ans = correct_answers[i]
                                is_correct = user_ans == correct_ans
                                st.write(f"**Q{i+1}:** {'✅ Correct' if is_correct else '❌ Incorrect'}")
                                # if not is_correct:
                                #     st.write(f"Your answer: {user_ans} — Correct answer: {correct_ans}")
                                score += int(is_correct)

                            total_questions_len = len(question_funcs) 
                            if score >= 10:
                                st.success(f"You scored {score} out of {total_questions_len}.")
                            elif score < 10:
                                st.error(f"You scored {score} out of {total_questions_len}.")


            else:
                st.error(f"❌ Sorry you have already submitted {n_submissions} times, you cannot longer take a new exam")

        else:
            st.markdown("❌ The deadline has passed. You can no longer take the quiz.")
  
        # if submitted and not st.session_state.time_up:
        #     valid_submission = False
        #     with st.spinner("Submitting results..."):
        #         timestamp = datetime.datetime.now()
        #         timestamp = timestamp.strftime("%d/%m/%Y, %H:%M:%S")
        #         solution_dict = dict()
        #         score = 0
        #         solution_dict['user'] = st.session_state['user_name']
        #         solution_dict['group'] = st.session_state['group']
        #         solution_dict['time'] = timestamp
        #         for i in user_answers:
        #             user_ans = user_answers[i]
        #             correct_ans = correct_answers[i]
        #             solution_dict[f'Q{i+1}'] = user_ans
        #             is_correct = user_ans == correct_ans
        #             score += int(is_correct)
        #         solution_dict['Grade'] = score
        #         st.session_state['student_grade'] = score
        #         logs_df = conn.read(worksheet="exam", usecols=list(range(df_n_cols)), ttl=1).dropna(how="all")

        #         n_submissions = len(logs_df[logs_df['user'] == st.session_state['user_name']])
        #         print(n_submissions)

        #         if n_submissions < st.session_state['n_submissions']:

        #             solution = pd.DataFrame([solution_dict])
        #             updated_log = pd.concat([logs_df,solution],ignore_index=True)
        #             conn.update(worksheet="exam",data = updated_log)

        #             st.success(f"✅ Your quiz has been submitted successfully! on {timestamp}")
        #             st.balloons()
        #             valid_submission = True
                
        #         elif n_submissions >= st.session_state['n_submissions']:
        #             st.error(f"❌ Sorry you have already submitted {n_submissions} times, you cannot longer submit a new exam")

        # elif st.session_state.time_up:
        #     st.error("❌ The deadline has passed. You can no longer submit the quiz.")

        # if submitted and not st.session_state.time_up and valid_submission:

        #     add_vertical_space(1)
        #     with st.expander(f"### ✅ Results ({st.session_state['student_grade']}/20)"):
        #         st.subheader("")

        #         # print(user_answers)
        #         # print(correct_answers)

        #         score = 0
        #         for i in user_answers:
        #             user_ans = user_answers[i]
        #             correct_ans = correct_answers[i]
        #             is_correct = user_ans == correct_ans
        #             st.write(f"**Q{i+1}:** {'✅ Correct' if is_correct else '❌ Incorrect'}")
        #             if not is_correct:
        #                 st.write(f"Your answer: {user_ans} — Correct answer: {correct_ans}")
        #             score += int(is_correct)

        #         total_questions_len = len(question_funcs) 

        #         st.success(f"You scored {score} out of {total_questions_len}.")