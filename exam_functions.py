import random
import datetime
from datetime import timedelta, date
import pandas as pd
import numpy as np

def question_forecasting_release_date_average(seed):
    random.seed(seed)

    # Step 1: Generate sprint duration and start date
    sprint_durations = [7, 14, 21, 28]
    sprint_duration = random.choice(sprint_durations)
    start_day = random.randint(1, 28)
    start_month = random.randint(1, 12)
    start_date = datetime.date(2025, start_month, start_day)

    # Step 2: Generate data for sprints
    num_sprints = random.randint(2, 8)
    backlog = 400
    velocities = [random.randint(14, 20) for _ in range(num_sprints)]
    dates = [start_date + timedelta(days=sprint_duration * i) for i in range(num_sprints)]

    cumulative_velocity = sum(velocities)
    remaining_backlog = backlog - cumulative_velocity
    avg_velocity = cumulative_velocity / num_sprints
    sprints_needed = round(remaining_backlog / avg_velocity)
    days_needed = round(sprints_needed * sprint_duration)
    last_sprint_date = dates[-1]
    release_date = last_sprint_date + timedelta(days=days_needed)

    # Step 3: Build question text
    table_rows = "\n".join(
        [f"sprint {i+1}\t{dates[i].strftime('%d-%m-%Y')}\t{velocities[i]}\t{backlog}" for i in range(num_sprints)]
    )
    question_text = f"""A project starts on {start_date.strftime('%d-%m-%Y')} with sprints of duration {sprint_duration} days.

    The table below shows the velocity per sprint and the fixed backlog of {backlog} points.

    \tdate\tsprint velocity\tbacklog
    {table_rows}

    Estimate the expected release date assuming the team continues with the same average velocity.

    What is the expected release date?"""

    q_half_1 = f"""A project starts on **{start_date.strftime('%d-%m-%Y')}** with sprints of duration **{sprint_duration}** days.The table below shows the velocity per sprint and the fixed backlog of **{backlog}** points."""

    q_half_2 = f"""Estimate the expected release date assuming the team continues with the same **average** velocity. What is the expected release date?"""

    # Step 4: Generate options
    correct_answer = release_date.strftime('%d-%m-%Y')
    distractors = set()
    while len(distractors) < 3:
        variation_days = random.choice([-28, -14, -10, -7, -2, 2,  7, 10, 14, 28])
        distractor_date = release_date + timedelta(days=variation_days)
        formatted = distractor_date.strftime('%d-%m-%Y')
        if formatted != correct_answer:
            distractors.add(formatted)
    options = list(distractors) + [correct_answer]

    random.seed(seed + 1)
    random.shuffle(options)

    # Step 5: Build DataFrame for question table
    df = pd.DataFrame({
        'sprint': [f'sprint {i+1}' for i in range(num_sprints)],
        'date': dates,
        'velocity': velocities,
        'backlog': [backlog] * num_sprints
    })

    data = {"start_date":start_date.strftime('%d-%m-%Y'),
            "sprint_duration":sprint_duration,
            "df":df}

    return {
        "question": question_text,
        "question_half_1": q_half_1,
        "question_half_2": q_half_2,
        "options": {x:let for let,x in zip('abcdefg',options)},
        "answer": correct_answer,
        "data": data,
        "display_mode":"table"
    }

def question_forecasting_release_date_optimistic(seed):
    random.seed(seed)

    # Step 1: Generate sprint duration and start date
    sprint_durations = [7, 14, 21, 28]
    sprint_duration = random.choice(sprint_durations)
    start_day = random.randint(1, 28)
    start_month = random.randint(1, 12)
    start_date = datetime.date(2025, start_month, start_day)

    # Step 2: Generate data for sprints
    num_sprints = random.randint(2, 8)
    backlog = 400
    velocities = [random.randint(14, 20) for _ in range(num_sprints)]
    dates = [start_date + timedelta(days=sprint_duration * i) for i in range(num_sprints)]

    cumulative_velocity = sum(velocities)
    remaining_backlog = backlog - cumulative_velocity
    max_velocity = max(velocities)
    sprints_needed = round(remaining_backlog / max_velocity)
    days_needed = round(sprints_needed * sprint_duration)
    last_sprint_date = dates[-1]
    release_date = last_sprint_date + timedelta(days=days_needed)

    # Step 3: Build question text
    table_rows = "\n".join(
        [f"sprint {i+1}\t{dates[i].strftime('%d-%m-%Y')}\t{velocities[i]}\t{backlog}" for i in range(num_sprints)]
    )
    question_text = f"""A project starts on {start_date.strftime('%d-%m-%Y')} with sprints of duration {sprint_duration} days.

    The table below shows the velocity per sprint and the fixed backlog of {backlog} points.

    \tdate\tsprint velocity\tbacklog
    {table_rows}

    Estimate the Optimistic release date assuming the team continues with the MAXIMUM velocity achieved so far.

    What is the Optimistic release date?"""


    q_half_1 = f"""A project starts on **{start_date.strftime('%d-%m-%Y')}** with sprints of duration **{sprint_duration}** days.The table below shows the velocity per sprint and the fixed backlog of **{backlog}** points."""

    q_half_2 = f"""Estimate the Optimistic release date assuming the team continues with the **MAXIMUM** velocity achieved so far. What is the **Optimistic** release date?"""

    # Step 4: Generate options
    correct_answer = release_date.strftime('%d-%m-%Y')
    distractors = set()
    while len(distractors) < 3:
        variation_days = random.choice([-28, -14, -10, -7, -2, 2,  7, 10, 14, 28])
        distractor_date = release_date + timedelta(days=variation_days)
        formatted = distractor_date.strftime('%d-%m-%Y')
        if formatted != correct_answer:
            distractors.add(formatted)
    options = list(distractors) + [correct_answer]
    random.seed(seed + 2)
    random.shuffle(options)

    # Step 5: Build DataFrame for question table
    df = pd.DataFrame({
        'sprint': [f'sprint {i+1}' for i in range(num_sprints)],
        'date': dates,
        'velocity': velocities,
        'backlog': [backlog] * num_sprints
    })

    data = {"start_date":start_date.strftime('%d-%m-%Y'),
        "sprint_duration":sprint_duration,
        "df":df}

    return {
        "question": question_text,
        "question_half_1": q_half_1,
        "question_half_2": q_half_2,
        "options": {x:let for let,x in zip('abcdefg',options)},
        "answer": correct_answer,
        "data": data,
        "display_mode":"table"
    }

def question_forecasting_release_date_pessimistic(seed):
    random.seed(seed)

    # Step 1: Generate sprint duration and start date
    sprint_durations = [7, 14, 21, 28]
    sprint_duration = random.choice(sprint_durations)
    start_day = random.randint(1, 28)
    start_month = random.randint(1, 12)
    start_date = datetime.date(2025, start_month, start_day)

    # Step 2: Generate data for sprints
    num_sprints = random.randint(2, 8)
    backlog = 400
    velocities = [random.randint(14, 20) for _ in range(num_sprints)]
    dates = [start_date + timedelta(days=sprint_duration * i) for i in range(num_sprints)]

    cumulative_velocity = sum(velocities)
    remaining_backlog = backlog - cumulative_velocity
    min_velocity = min(velocities)
    sprints_needed = round(remaining_backlog / min_velocity)
    days_needed = round(sprints_needed * sprint_duration)
    last_sprint_date = dates[-1]
    release_date = last_sprint_date + timedelta(days=days_needed)

    # Step 3: Build question text
    table_rows = "\n".join(
        [f"sprint {i+1}\t{dates[i].strftime('%d-%m-%Y')}\t{velocities[i]}\t{backlog}" for i in range(num_sprints)]
    )
    question_text = f"""A project starts on {start_date.strftime('%d-%m-%Y')} with sprints of duration {sprint_duration} days.

    The table below shows the velocity per sprint and the fixed backlog of {backlog} points.

    \tdate\tsprint velocity\tbacklog
    {table_rows}

    Estimate the Pessimistic release date assuming the team continues with the MINIMUM velocity achieved so far.

    What is the Pessimistic release date?"""

    q_half_1 = f"""A project starts on **{start_date.strftime('%d-%m-%Y')}** with sprints of duration **{sprint_duration}** days.The table below shows the velocity per sprint and the fixed backlog of **{backlog}** points."""

    q_half_2 = f"""Estimate the Pessimistic release date assuming the team continues with the **MINIMUM** velocity achieved so far. What is the **Pessimistic** release date?"""


    # Step 4: Generate options
    correct_answer = release_date.strftime('%d-%m-%Y')
    distractors = set()
    while len(distractors) < 3:
        variation_days = random.choice([-28, -14, -10, -7, -2, 2,  7, 10, 14, 28])
        distractor_date = release_date + timedelta(days=variation_days)
        formatted = distractor_date.strftime('%d-%m-%Y')
        if formatted != correct_answer:
            distractors.add(formatted)
    options = list(distractors) + [correct_answer]
    random.seed(seed + 3)
    random.shuffle(options)

    # Step 5: Build DataFrame for question table
    df = pd.DataFrame({
        'sprint': [f'sprint {i+1}' for i in range(num_sprints)],
        'date': dates,
        'velocity': velocities,
        'backlog': [backlog] * num_sprints
    })

    data = {"start_date":start_date.strftime('%d-%m-%Y'),
        "sprint_duration":sprint_duration,
        "df":df}

    return {
        "question": question_text,
        "question_half_1": q_half_1,
        "question_half_2": q_half_2,
        "options": {x:let for let,x in zip('abcdefg',options)},
        "answer": correct_answer,
        "data": data,
        "display_mode":"table"
    }

def question_forecasting_release_date_backlog_increase(seed):
    random.seed(seed)

    # Step 1: Generate sprint duration and start date
    sprint_durations = [7, 14, 21, 28]
    sprint_duration = random.choice(sprint_durations)
    start_day = random.randint(1, 28)
    start_month = random.randint(1, 12)
    start_date = datetime.date(2025, start_month, start_day)

    # Step 2: Generate data for sprints
    num_sprints = random.randint(2, 8)
    backlog = 400
    velocities = [random.randint(14, 20) for _ in range(num_sprints)]
    dates = [start_date + timedelta(days=sprint_duration * i) for i in range(num_sprints)]

    backlog_increase = random.randint(30, 60)

    cumulative_velocity = sum(velocities)
    remaining_backlog = backlog + backlog_increase - cumulative_velocity
    avg_velocity = cumulative_velocity / num_sprints
    sprints_needed = round(remaining_backlog / avg_velocity)
    days_needed = round(sprints_needed * sprint_duration)
    last_sprint_date = dates[-1]
    release_date = last_sprint_date + timedelta(days=days_needed)

    # Step 3: Build question text
    table_rows = "\n".join(
        [f"sprint {i+1}\t{dates[i].strftime('%d-%m-%Y')}\t{velocities[i]}\t{backlog}" for i in range(num_sprints)]
    )
    question_text = f"""A project starts on {start_date.strftime('%d-%m-%Y')} with sprints of duration {sprint_duration} days.

    The table below shows the velocity per sprint and the fixed backlog of {backlog} points.

    \tdate\tsprint velocity\tbacklog
    {table_rows}

    Due to a sudden change in business priorities, the product owner added new {backlog_increase} story points to the backlog, for a total of {backlog + backlog_increase}.
    Please Estimate the NEW expected release date assuming the team continues with the same average velocity from the previous sprints.

    What is the NEW expected release date?"""

    q_half_1 = f"""A project starts on **{start_date.strftime('%d-%m-%Y')}** with sprints of duration **{sprint_duration}** days.The table below shows the velocity per sprint and the fixed backlog of **{backlog}** points."""

    q_half_2 = f"""
    Due to a sudden change in business priorities, the product owner added new **{backlog_increase}** story points to the backlog, for a total of **{backlog + backlog_increase}**.
    Please Estimate the **NEW expected release date** assuming the team continues with the **same average velocity** from the previous sprints. 
    What is the NEW expected release date?"""

    # Step 4: Generate options
    correct_answer = release_date.strftime('%d-%m-%Y')
    distractors = set()
    while len(distractors) < 3:
        variation_days = random.choice([-28, -14, -10, -7, -2, 2,  7, 10, 14, 28])
        distractor_date = release_date + timedelta(days=variation_days)
        formatted = distractor_date.strftime('%d-%m-%Y')
        if formatted != correct_answer:
            distractors.add(formatted)
    options = list(distractors) + [correct_answer]

    random.seed(seed + 1)
    random.shuffle(options)

    # Step 5: Build DataFrame for question table
    df = pd.DataFrame({
        'sprint': [f'sprint {i+1}' for i in range(num_sprints)],
        'date': dates,
        'velocity': velocities,
        'backlog': [backlog] * num_sprints
    })

    data = {"start_date":start_date.strftime('%d-%m-%Y'),
            "sprint_duration":sprint_duration,
            "backlog_increase":backlog_increase,
            "df":df}

    return {
        "question": question_text,
        "question_half_1": q_half_1,
        "question_half_2": q_half_2,
        "options": {x:let for let,x in zip('abcdefg',options)},
        "answer": correct_answer,
        "data": data,
        "display_mode":"table"   
    }

def question_forecasting_release_date_roi_new_team_member(seed):
    random.seed(seed)

    # Step 1: Generate sprint duration and start date
    sprint_durations = [7, 14, 21, 28]
    sprint_duration = random.choice(sprint_durations)
    start_day = random.randint(1, 28)
    start_month = random.randint(1, 12)
    start_date = datetime.date(2025, start_month, start_day)

    # Step 2: Generate data for sprints
    num_sprints = random.randint(2, 8)
    backlog = 400
    velocities = [random.randint(14, 20) for _ in range(num_sprints)]
    dates = [start_date + timedelta(days=sprint_duration * i) for i in range(num_sprints)]

    backlog_increase = random.randint(30, 60)

    velocity_increase = random.randint(10,25)
    daily_rate = random.randint(75,160)
    revenue_increase = random.choice([500,600,700,800,900,1000])

    cumulative_velocity = sum(velocities)
    remaining_backlog = backlog + backlog_increase - cumulative_velocity
    avg_velocity = cumulative_velocity / num_sprints
    new_velocity = avg_velocity* ( 100 + velocity_increase )/100
    sprints_needed = round(remaining_backlog / avg_velocity)
    sprints_needed_new = round(remaining_backlog / new_velocity)
    days_needed = round(sprints_needed * sprint_duration)
    days_needed_new = round(sprints_needed_new * sprint_duration)
    last_sprint_date = dates[-1]
    release_date = last_sprint_date + timedelta(days=days_needed)
    new_release_date = last_sprint_date + timedelta(days=days_needed_new)

    days_saved = (release_date - new_release_date).days

    extra_revenue = days_saved * revenue_increase
    days_developer = (new_release_date - last_sprint_date).days
    extra_cost = days_developer * daily_rate

    profit = extra_revenue - extra_cost

    # print(release_date, new_release_date, days_saved)
    # print(extra_revenue, extra_cost, profit)

    should_hire = (profit > 0)
    correct_answer = "Yes, hire the extra developer" if should_hire else "No, do NOT hire the extra developer"

    # Step 3: Build question text
    table_rows = "\n".join(
        [f"sprint {i+1}\t{dates[i].strftime('%d-%m-%Y')}\t{velocities[i]}\t{backlog}" for i in range(num_sprints)]
    )
    question_text = f"""A project starts on {start_date.strftime('%d-%m-%Y')} with sprints of duration {sprint_duration} days.

    The table below shows the velocity per sprint and the fixed backlog of {backlog} points.

    \tdate\tsprint velocity\tbacklog
    {table_rows}

    Due to a sudden change in business priorities, the product owner added new {backlog_increase} story points to the backlog, for a total of {backlog + backlog_increase}.
    In order to handle the extra workload the product owner is considering the hiring of a new developer. 
    Please consider the following information:

    - The product owner estimates that a new developer would increase the average team velocity by {velocity_increase} %.
    - The daily salary of the new developer is {daily_rate} € per day. 
    - Every day of reduction for the release date is equivalent to a potential increase in revenue of {revenue_increase} € per day.

    Please calculate the reduction in days that the additional new developer will produe and estimate if it is profitable to make such an investment?
    
    Hints:

    - Use the expected release date from Q4 as your benchmark
    - Calculate the new expected release date by multiplying the original velocity by {100 + velocity_increase} %
    - Substract the two expected dates, and calculate the days saved by the new developer and the increase in revenue
    - Calculate the extra cost of the new developer between the last day of the sprint and the new expected release date
    - Calculate the overall profit of this decision
    
    Do you think that the product owner should hire the extra developer
    """

    q_half_1 = f"""A project starts on **{start_date.strftime('%d-%m-%Y')}** with sprints of duration **{sprint_duration}** days.The table below shows the velocity per sprint and the fixed backlog of **{backlog}** points."""

    q_half_2 = f"""
    Due to a sudden change in business priorities, the product owner added new **{backlog_increase}** story points to the backlog, for a total of **{backlog + backlog_increase}**.
    In order to handle the extra workload the product owner is considering the hiring of a new developer. 
    Please consider the following information:

    - The product owner estimates that a new developer would increase the average team velocity by **{velocity_increase}** %.
    - The daily salary of the new developer is **{daily_rate}** € per day. 
    - Every day of reduction for the release date is equivalent to a potential increase in revenue of **{revenue_increase}** € per day.
    
    Please calculate the reduction in days that the additional new developer will produe and estimate if it is profitable to make such an investment?
    
    Hints:

    - Use the expected release date from Q4 as your benchmark
    - Calculate the new expected release date by multiplying the original velocity by {100 + velocity_increase} %
    - Substract the two expected dates, and calculate the days saved by the new developer and the increase in revenue
    - Calculate the extra cost of the new developer between the last day of the sprint and the new expected release date
    - Calculate the overall profit of this decision
    
    Do you think that the product owner should hire the extra developer?
    """

    # Step 4: Generate options
    options = ["Yes, hire the extra developer", "No, do NOT hire the extra developer"]
    random.seed(seed + 6)
    random.shuffle(options)

    # Step 5: Build DataFrame for question table
    df = pd.DataFrame({
        'sprint': [f'sprint {i+1}' for i in range(num_sprints)],
        'date': dates,
        'velocity': velocities,
        'backlog': [backlog] * num_sprints
    })

    data = {"start_date":start_date.strftime('%d-%m-%Y'),
            "sprint_duration":sprint_duration,
            "backlog_increase":backlog_increase,
            "velocity":avg_velocity,
            "velocity_increase":velocity_increase,
            "new_velocity":new_velocity,
            "daily_rate":daily_rate,
            "revenue_increase":revenue_increase,
            "extra_revenue":extra_revenue,
            "days_developer":days_developer,
            "extra_cost":extra_cost,
            "release_date":release_date.strftime('%d-%m-%Y'),
            "new_release_date":new_release_date.strftime('%d-%m-%Y'),
            "days_saved":days_saved,
            "profit":profit,
            "df":df}

    return {
        "question": question_text,
        "question_half_1": q_half_1,
        "question_half_2": q_half_2,
        "options": {x:let for let,x in zip('abcdefg',options)},
        "answer": correct_answer,
        "data": data,
        "display_mode":"table"
    }

def question_control_limits_ucl(seed):
    random.seed(seed)
    np.random.seed(seed)

    # Step 1: Generate velocity data
    num_sprints = random.randint(4, 10)
    base_velocity = random.randint(45, 55)
    velocities = list(np.random.normal(loc=base_velocity, scale=5, size=num_sprints).astype(int))
    df = pd.DataFrame({
        'sprint': [f'sprint {i+1}' for i in range(num_sprints)],
        'velocity': velocities
    })

    # Step 2: Select sigma level and generate new velocity to evaluate
    sigma_level = random.randint(2, 6)
    velocity_to_check = random.randint(base_velocity - 15, base_velocity + 15)

    # Step 3: Calculate mean, std deviation, std error
    mean_velocity = np.mean(velocities)
    std_dev = np.std(velocities, ddof=1)
    std_error = std_dev / np.sqrt(num_sprints)
    UCL = mean_velocity + sigma_level * std_error
    LCL = mean_velocity - sigma_level * std_error

    # Step 4: Create question text
    table_text = "\n".join([f"{row.sprint}\t{row.velocity}" for _, row in df.iterrows()])
    question_text = f"""A scrum master is monitoring the velocity of their team across {num_sprints} sprints.

    Here is the velocity data for past sprints:

    \tSprint\tVelocity
    {table_text}
    At a sigma level of {sigma_level}, above wich Upper Limit Control (UCL) threshold should the scrum master investigate?

    Please round your answer to 0 decimals. Use control limits to answer the question."""

    q_half_1 = f"""A scrum master is monitoring the velocity of their team across **{num_sprints}** sprints. Here is the velocity data for past sprints:"""

    q_half_2 = f"""At a sigma level of **{sigma_level}**, above wich **Upper Limit Control (UCL)** threshold should the scrum master investigate? Please round your answer to **0 decimals**."""

    # Step 5: Create wrong options
    options = np.random.randint(1 , round(2*(UCL),0), size=3).tolist()
    options = [x + random.choice([-3,-2,-1,1,2,3]) if x == int(round(UCL,0)) else x for x in  options]
    options = [round(UCL,0)] + options
    options = [str(int(x)) for x in options]
    random.seed(seed + 4)
    random.shuffle(options)

    data = {"sigma_level":sigma_level,
            "velocity_to_check":velocity_to_check,
            "df":df}

    return {
        "question": question_text,
        "question_half_1": q_half_1,
        "question_half_2": q_half_2,
        "options": {x:let for let,x in zip('abcdefg',options)},
        "answer": str(int(round(UCL,0))),
        "data": data,
        "display_mode":"table"
    }

def question_control_limits_lcl(seed):
    random.seed(seed)
    np.random.seed(seed)

    # Step 1: Generate velocity data
    num_sprints = random.randint(4, 10)
    base_velocity = random.randint(45, 55)
    velocities = list(np.random.normal(loc=base_velocity, scale=5, size=num_sprints).astype(int))
    df = pd.DataFrame({
        'sprint': [f'sprint {i+1}' for i in range(num_sprints)],
        'velocity': velocities
    })

    # Step 2: Select sigma level and generate new velocity to evaluate
    sigma_level = random.randint(2, 6)
    velocity_to_check = random.randint(base_velocity - 15, base_velocity + 15)

    # Step 3: Calculate mean, std deviation, std error
    mean_velocity = np.mean(velocities)
    std_dev = np.std(velocities, ddof=1)
    std_error = std_dev / np.sqrt(num_sprints)
    UCL = mean_velocity + sigma_level * std_error
    LCL = mean_velocity - sigma_level * std_error

    # Step 4: Create question text
    table_text = "\n".join([f"{row.sprint}\t{row.velocity}" for _, row in df.iterrows()])
    question_text = f"""A scrum master is monitoring the velocity of their team across {num_sprints} sprints.

    Here is the velocity data for past sprints:

    \tSprint\tVelocity
    {table_text}
    At a sigma level of {sigma_level}, below wich Lower Limit Control (LCL) threshold should the scrum master investigate?

    Please round your answer to 0 decimals. Use control limits to answer the question."""

    q_half_1 = f"""A scrum master is monitoring the velocity of their team across **{num_sprints}** sprints. Here is the velocity data for past sprints:"""

    q_half_2 = f"""At a sigma level of **{sigma_level}**, below wich **Lower Limit Control (LCL)** threshold should the scrum master investigate? Please round your answer to **0 decimals**."""

    # Step 5: Create wrong options
    options = np.random.randint(1 , round(2*(UCL),0), size=3).tolist()
    options = [x + random.choice([-3,-2,-1,1,2,3]) if x == int(round(LCL,0)) else x for x in  options]
    options = [round(LCL,0)] + options
    options = [str(int(x)) for x in options]
    random.seed(seed + 5)
    random.shuffle(options)

    data = {"sigma_level":sigma_level,
        "velocity_to_check":velocity_to_check,
        "df":df}

    return {
        "question": question_text,
        "question_half_1": q_half_1,
        "question_half_2": q_half_2,
        "options": {x:let for let,x in zip('abcdefg',options)},
        "answer": str(int(round(LCL,0))),
        "data": data,
        "display_mode":"table"
    }

def question_control_limits_investigation(seed):
    random.seed(seed)
    np.random.seed(seed)

    # Step 1: Generate velocity data
    num_sprints = random.randint(4, 10)
    base_velocity = random.randint(45, 55)
    velocities = list(np.random.normal(loc=base_velocity, scale=5, size=num_sprints).astype(int))
    df = pd.DataFrame({
        'sprint': [f'sprint {i+1}' for i in range(num_sprints)],
        'velocity': velocities
    })

    # Step 2: Select sigma level and generate new velocity to evaluate
    sigma_level = random.randint(2, 6)
    velocity_to_check = random.randint(base_velocity - 15, base_velocity + 15)

    # Step 3: Calculate mean, std deviation, std error
    mean_velocity = np.mean(velocities)
    std_dev = np.std(velocities, ddof=1)
    std_error = std_dev / np.sqrt(num_sprints)
    UCL = mean_velocity + sigma_level * std_error
    LCL = mean_velocity - sigma_level * std_error

    # Step 4: Determine if investigation is needed
    should_investigate = not (LCL <= velocity_to_check <= UCL)
    correct_answer = "Yes, investigate" if should_investigate else "No, no investigation needed"
    # correct_answer = (correct_answer,[int(round(LCL,0)),int(round(UCL,0))])

    # Step 5: Create question text
    table_text = "\n".join([f"{row.sprint}\t{row.velocity}" for _, row in df.iterrows()])
    question_text = f"""A scrum master is monitoring the velocity of their team across {num_sprints} sprints.

    Here is the velocity data for past sprints:

    \tSprint\tVelocity
    {table_text}

    Now, imagine that the last sprint's velocity is {velocity_to_check}.
    At a sigma level of {sigma_level}, should the scrum master investigate this anomaly?

    Use control limits to answer the question."""


    q_half_1 = f"""A scrum master is monitoring the velocity of their team across **{num_sprints}** sprints. Here is the velocity data for past sprints:"""

    q_half_2 = f"""Now, imagine that the last sprint's velocity is **{velocity_to_check}**. At a sigma level of **{sigma_level}**, should the scrum master investigate this anomaly? Use control limits to answer the question."""

    options = ["Yes, investigate", "No, no investigation needed"]
    random.seed(seed + 6)
    random.shuffle(options)

    data = {"sigma_level":sigma_level,
        "velocity_to_check":velocity_to_check,
        "df":df}

    return {
        "question": question_text,
        "question_half_1": q_half_1,
        "question_half_2": q_half_2,
        "options": {x:let for let,x in zip('abcdefg',options)},
        "answer": correct_answer,
        "data": data,
        "display_mode":"table"
    }

def question_littles_law_1(seed):
    random.seed(seed)

    # Random values for WIP and throughput
    wip = random.randint(10, 40)
    throughput = random.randint(2, 20)

    # Calculate the correct cycle time using Little's Law
    cycle_time = round(wip / throughput)

    # Generate distractors
    distractors = set()
    while len(distractors) < 3:
        variation = random.choice([-4,-3,-2, -1, 1, 2, 3,4])
        candidate = cycle_time + variation
        if candidate > 0 and candidate != cycle_time:
            distractors.add(candidate)
    options = list(distractors) + [cycle_time]
    random.seed(seed + 7)
    random.shuffle(options)

    # Build question text
    question_text = f"""Your Scrum team visualizes work using sticky notes on a whiteboard (Kanban Board). Over the past few weeks, you observed:

- There are **{wip}** sticky notes on the Work-In-Progress column of the board at any time (on average).
- The team completes about **{throughput}** user stories per week.

Use Little’s Law to calculate the average cycle time for a user story. Round your answer to 0 decimals.
"""

    return {
        "question": question_text,
        "options": {str(x):let for let,x in zip('abcdefg',options)},
        "answer": f"{cycle_time}",
        "data": (wip, throughput, cycle_time),
        "display_mode":"full_text"
    }

def question_littles_law_2(seed):
    random.seed(seed)

    # Random parameters
    wip_limit = random.randint(5, 40)  # work in progress
    cycle_time_days = random.randint(2, 14)
    working_days_per_week = random.randint(2, 7)

    # Calculate throughput using Little's Law
    throughput = round((wip_limit / cycle_time_days) * working_days_per_week)

    # Generate distractors
    distractors = set()
    while len(distractors) < 3:
        variation = random.choice([-4,-3, -2, -1, 1, 2, 3, 4])
        candidate = throughput + variation
        if candidate > 0 and candidate != throughput:
            distractors.add(candidate)
    options = list(distractors) + [throughput]
    random.seed(seed + 8)
    random.shuffle(options)

    # Build question text
    question_text = f"""Your team is experimenting with WIP limits on their Kanban board. Currently:
- The WIP limit is **{wip_limit}**.
- The average cycle time for a feature is **{cycle_time_days}** days.
- The team works **{working_days_per_week}** days per week.

Estimate the team's throughput per week. Please Round your answer to **0 decimals**."""

    return {
        "question": question_text,
        "options":{f"{x} features/week":let for let,x in zip('abcdefg',options)},
        "answer": f"{throughput} features/week",
        "data": (wip_limit, cycle_time_days, working_days_per_week, throughput),
        "display_mode":"full_text"
    }

def question_kanban_bottleneck(seed):
    random.seed(seed)

    # Generate dates (weekly)
    num_weeks = random.randint(6, 10)
    start_date = date(2025, 4, 1)
    dates = [start_date + timedelta(days=7*i) for i in range(num_weeks)]

    # Generate WIP data with increasing complexity across stages
    analysis = [random.randint(10 + i, 15 + i) for i in range(num_weeks)]
    design = [max(0, a - random.randint(-3, 3)) for a in analysis]
    development = [max(0, d - random.randint(-6, 6)) for d in design]
    qa = [max(0, dev - random.randint(5, 8)) for dev in development]

    # Fill in other columns
    backlog = [400 - sum(qa[:i]) for i in range(num_weeks)]
    completed = [sum(qa[:i]) for i in range(num_weeks)]

    # Construct the DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Backlog': backlog,
        'Analysis': analysis,
        'Design': design,
        'Development': development,
        'QA': qa,
        'Completed': completed
    })

    # Compute averages
    avg_analysis = sum(analysis) / num_weeks
    avg_design = sum(design) / num_weeks
    avg_development = sum(development) / num_weeks
    avg_qa = sum(qa) / num_weeks

    avg_wips = {
        'Analysis': avg_analysis,
        'Design': avg_design,
        'Development': avg_development,
        'QA': avg_qa
    }

    # print(avg_wips)

    # Find the bottleneck (the column *after* the one with max average WIP)
    max_stage = max(avg_wips, key=avg_wips.get)
    stages = ['Analysis', 'Design', 'Development', 'QA']
    try:
        bottleneck_index = stages.index(max_stage) + 1
        bottleneck = stages[bottleneck_index]
    except IndexError:
        bottleneck = "Completed"  # If QA is max, bottleneck is "Completed"

    # Create MCQ options
    options = ['Design', 'Development', 'QA', 'Completed']
    if bottleneck not in options:
        options[random.randint(0, 3)] = bottleneck

    random.seed(seed + 9)
    random.shuffle(options)

    # Build question text
    table_str = df.to_string(index=False)
    question_text = f"""Your team is visualizing their flow using a Kanban board. The table below shows weekly WIP levels across various stages.
    Each user story in progress needs to go through different phases sequentially, from Analysis to QA, before is considered completed.

    {table_str}

    Based on Little's Law and the idea that work piles up before a bottleneck, which of the following stages of the WIP is most likely to be the bottleneck in this process?"""

    q_half_1 = f"""Your team is visualizing their flow using a Kanban board. The table below shows weekly WIP levels across various stages.
    Each user story in progress needs to go through different phases sequentially, from Analysis to QA, before is considered completed."""

    q_half_2 = f"""Based on Little's Law and the idea that work piles up before a bottleneck, which of the following stages of the WIP is most likely to be the bottleneck in this process?"""

    data = {"bottleneck":bottleneck,
            "df":df}

    return {
        "question": question_text,
        "question_half_1": q_half_1,
        "question_half_2": q_half_2,
        "options": {x:let for let,x in zip('abcdefg',options)},
        "answer": bottleneck,
        "data": data,
        "display_mode":"table"
    }

def question_kanban_throughput_estimation(seed):
    random.seed(seed)
    np.random.seed(seed)

    # Generate dates (weekly)
    num_weeks = random.randint(6, 10)
    start_date = date(2025, 4, 1)
    dates = [start_date + timedelta(days=7 * i) for i in range(num_weeks)]

    # Generate WIP data
    analysis = [random.randint(10 + i, 15 + i) for i in range(num_weeks)]
    design = [max(0, a - random.randint(-3, 3)) for a in analysis]
    development = [max(0, d - random.randint(-6, 6)) for d in design]
    qa = [max(0, dev - random.randint(5, 8)) for dev in development]

    # Compute backlog and completed over time
    backlog = [400 - sum(qa[:i]) for i in range(num_weeks)]
    completed = [sum(qa[:i]) for i in range(num_weeks)]

    # Build DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Backlog': backlog,
        'Analysis': analysis,
        'Design': design,
        'Development': development,
        'QA': qa,
        'Completed': completed
    })

    # Calculate average throughput (average of weekly changes in 'Completed')
    weekly_deltas = [completed[i] - completed[i - 1] for i in range(1, len(completed))]
    avg_throughput = round(sum(weekly_deltas) / len(weekly_deltas),1)

    # Generate distractors
    distractors = set()
    while len(distractors) < 3:
        variation = max(1,random.choice([-5,-4,-3, -2, -1, 1, 2, 3, 4, 5]))
        candidate = avg_throughput + variation
        if candidate > 0 and candidate != avg_throughput:
            distractors.add(candidate)
    options = list(distractors) + [avg_throughput]
    random.seed(seed + 10)
    random.shuffle(options)

    # Build question
    table_str = df.to_string(index=False)
    question_text = f"""Your team is visualizing their flow using a Kanban board. The table below shows weekly WIP levels across various stages.
    Each user story in progress needs to go through different phases sequentially, from Analysis to QA, before it is considered completed.

    {table_str}

    Based on the information above, what is the team's average throughput (TH) per week? Please round your answer to 1 decimal value."""

    q_half_1 = f"""Your team is visualizing their flow using a Kanban board. The table below shows weekly WIP levels across various stages.
    Each user story in progress needs to go through different phases sequentially, from Analysis to QA, before is considered completed."""

    q_half_2 = f""" Based on the information above, what is the team's average throughput (TH) per week? Please round your answer to **1 decimal** value."""

    data = {"avg_throughput":avg_throughput,
        "df":df}

    return {
        "question": question_text,
        "question_half_1": q_half_1,
        "question_half_2": q_half_2,
        "options": {f"{x} stories/week":let for let,x in zip('abcdefg',options)},
        "answer": f"{avg_throughput} stories/week",
        "data": data,
        "display_mode":"table"
    }

def question_kanban_average_wip(seed):
    random.seed(seed)
    np.random.seed(seed)

    # Generate dates (weekly)
    num_weeks = random.randint(6, 10)
    start_date = date(2025, 4, 1)
    dates = [start_date + timedelta(days=7 * i) for i in range(num_weeks)]

    # Generate WIP values
    analysis = [random.randint(10 + i, 15 + i) for i in range(num_weeks)]
    design = [max(0, a - random.randint(-3, 3)) for a in analysis]
    development = [max(0, d - random.randint(-6, 6)) for d in design]
    qa = [max(0, dev - random.randint(5, 8)) for dev in development]

    # Calculate WIP per row and then average
    wip_per_week = [a + d + dev + q for a, d, dev, q in zip(analysis, design, development, qa)]
    avg_wip = round(sum(wip_per_week) / len(wip_per_week), 1)

    # Other columns
    backlog = [400 - sum(qa[:i]) for i in range(num_weeks)]
    completed = [sum(qa[:i]) for i in range(num_weeks)]

    # Build DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Backlog': backlog,
        'Analysis': analysis,
        'Design': design,
        'Development': development,
        'QA': qa,
        'Completed': completed
    })

    # Generate distractors
    distractors = set()
    while len(distractors) < 3:
        variation = random.choice([-10 ,-5, -3, -2, 2, 3, 5, 10])
        candidate = round(avg_wip + variation + random.choice([2,-2])*np.random.rand(), 1)
        if candidate > 0 and candidate != avg_wip:
            distractors.add(candidate)
    options = list(distractors) + [avg_wip]
    random.seed(seed + 11)
    random.shuffle(options)

    # Build question text
    table_str = df.to_string(index=False)
    question_text = f"""Your team is visualizing their flow using a Kanban board. The table below shows weekly WIP levels across various stages.
    Each user story in progress needs to go through different phases sequentially, from Analysis to QA, before it is considered completed.

    {table_str}

    What is the team's average Work In Progress (WIP) across the period shown? Please round your answer to 1 decimal value."""

    q_half_1 = f"""Your team is visualizing their flow using a Kanban board. The table below shows weekly WIP levels across various stages.
    Each user story in progress needs to go through different phases sequentially, from Analysis to QA, before is considered completed."""

    q_half_2 = f"""What is the team's average Work In Progress (WIP) across the period shown? Please round your answer to **1 decimal** value."""

    data = {"avg_wip":avg_wip,
        "df":df}

    return {
        "question": question_text,
        "question_half_1": q_half_1,
        "question_half_2": q_half_2,
        "options": {f"{x} items":let for let,x in zip('abcdefg',options)},
        "answer": f"{avg_wip} items",
        "data": data,
        "display_mode":"table"
    }

def question_kanban_cycle_time(seed):
    random.seed(seed)

    # Generate dates (weekly)
    num_weeks = random.randint(6, 10)
    start_date = date(2025, 4, 1)
    dates = [start_date + timedelta(days=7 * i) for i in range(num_weeks)]

    # Generate WIP values
    analysis = [random.randint(10 + i, 15 + i) for i in range(num_weeks)]
    design = [max(0, a - random.randint(-3, 3)) for a in analysis]
    development = [max(0, d - random.randint(-6, 6)) for d in design]
    qa = [max(0, dev - random.randint(5, 8)) for dev in development]

    # Weekly WIP sum
    wip_per_week = [a + d + dev + q for a, d, dev, q in zip(analysis, design, development, qa)]
    avg_wip = sum(wip_per_week) / len(wip_per_week)

    # Completed column and throughput
    completed = [sum(qa[:i]) for i in range(num_weeks)]
    weekly_deltas = [completed[i] - completed[i - 1] for i in range(1, len(completed))]
    avg_throughput = sum(weekly_deltas) / len(weekly_deltas)

    # Little's Law: CT = WIP / Throughput
    cycle_time = round(avg_wip / avg_throughput, 1)

    # Other columns
    backlog = [400 - c for c in completed]

    # Build DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Backlog': backlog,
        'Analysis': analysis,
        'Design': design,
        'Development': development,
        'QA': qa,
        'Completed': completed
    })

    # Generate distractors
    distractors = set()
    while len(distractors) < 3:
        variation = random.choice([-2, -1, -0.5, 0.5, 1, 2])
        candidate = round(cycle_time + variation, 1)
        if candidate > 0 and candidate != cycle_time:
            distractors.add(candidate)
    options = list(distractors) + [cycle_time]
    random.seed(seed + 12)
    random.shuffle(options)

    # Build question text
    table_str = df.to_string(index=False)
    question_text = f"""Your team is visualizing their flow using a Kanban board. The table below shows weekly WIP levels across various stages.
    Each user story in progress needs to go through different phases sequentially, from Analysis to QA, before it is considered completed.

    {table_str}

    Use Little's Law to calculate the team's average cycle time (CT) during the period shown. Please round your answer to 1 decimal value."""


    q_half_1 = f"""Your team is visualizing their flow using a Kanban board. The table below shows weekly WIP levels across various stages.
    Each user story in progress needs to go through different phases sequentially, from Analysis to QA, before is considered completed."""

    q_half_2 = f"""Use Little's Law to calculate the team's average cycle time (CT) during the period shown. Please round your answer to **1 decimal** value."""
    
    data = {"avg_wip":avg_wip,
            "avg_throughput":avg_throughput,
            "cycle_time":cycle_time,
            "df":df}

    return {
        "question": question_text,
        "question_half_1": q_half_1,
        "question_half_2": q_half_2,
        "options": {f"{x} days":let for let,x in zip('abcdefg',options)},
        "answer": f"{cycle_time} days",
        "data": data,
        "display_mode":"table"
    }

def question_kingman_utilization(seed):

    def tq(cv_a, cv_p, m, u, tp):
      t1 = ((cv_a**2) + (cv_p**2)) / 2
      t2 = (u**(np.sqrt(2 * (m + 1)) - 1)) / (m * (1 - u))
      tq = t1 * t2 * tp
      return tq

    random.seed(seed)
    np.random.seed(seed)

    # Step 1: Random inputs
    r_a = random.randint(25, 30)  # arrivals per week
    std_a = random.randint(60, 80)  # standard deviation of arrivals
    r_p = random.randint(31, 40)  # processing rate per week
    std_p = random.randint(8, 15)  # std dev of processing time
    m = 1  # number of servers

    # Step 2: Calculations
    u = r_a / r_p

    # Step 3: Generate distractors
    distractors = set()
    while len(distractors) < 3:
        candidate = round(np.random.rand(), 3)
        if candidate > 0 and candidate != u:
            distractors.add(candidate)
    options = list(distractors) + [round(u, 3)]
    random.seed(seed + 13)
    random.shuffle(options)

    # Step 4: Build question text
    question_text = f"""
    You are the Product Owner of an Agile team and due to a recent release, new user stories related to bugs arrive at about **{r_a}** per week with a standard deviation of **{std_a}**.
    A team member can debug approximately **{r_p}** stories per week with a standard deviation of **{std_p}**.
    For the time being, assume there is a single **(1) team member** processing these tasks.

    Please calculate the current utilization (u) of the process. Please round up your answer to **3 decimals**.
    """

    return {
        "question": question_text,
        "options": {f"{x:0.3f}":let for let,x in zip('abcdefg',options)},
        "answer": f"{u:.03f}",
        "data": {
            "r_a": r_a,
            "std_a": std_a,
            "r_p": r_p,
            "std_p": std_p,
            "u": round(u, 3),
            "m": m,
            "utilization": round(u, 3),
        },
        "display_mode":"full_text"
    }

def question_kingman_wait_time(seed):

    def tq(cv_a, cv_p, m, u, tp):
      t1 = ((cv_a**2) + (cv_p**2)) / 2
      t2 = (u**(np.sqrt(2 * (m + 1)) - 1)) / (m * (1 - u))
      tq = t1 * t2 * tp
      return tq

    random.seed(seed)

    # Step 1: Random inputs
    r_a = random.randint(25, 30)  # arrivals per week
    std_a = random.randint(60, 80)  # standard deviation of arrivals
    r_p = random.randint(31, 40)  # processing rate per week
    std_p = random.randint(8, 15)  # std dev of processing time
    m = 1  # number of servers

    # Step 2: Calculations
    u = r_a / r_p
    t_a = 1 / r_a
    t_p = 1 / r_p
    cv_a = std_a * t_a
    cv_p = std_p * t_p

    t_q = tq(cv_a, cv_p, m, u, t_p)
    t_q_rounded = round(t_q, 3)

    # Step 3: Generate distractors
    distractors = set()
    while len(distractors) < 3:
        variation = random.choice([-0.33,-0.255 ,-0.22, -0.155 ,-0.11,-0.055, 0.055 , 0.11,0.155, 0.22,0.255, 0.33])
        candidate = round(t_q + variation, 3)
        if candidate > 0 and candidate != t_q_rounded:
            distractors.add(candidate)
    options = list(distractors) + [t_q_rounded]
    random.seed(seed + 13)
    random.shuffle(options)

    # Step 4: Build question text
    question_text = f"""
    You are the Product Owner of an Agile team and due to a recent release, new user stories related to bugs arrive at about **{r_a}** per week with a standard deviation of **{std_a}**.
    A team member can debug approximately **{r_p}** stories per week with a standard deviation of **{std_p}**.
    For the time being, assume there is a **single (1) team member** processing these tasks.

    Please use the Kingman’s approximation (VUT formula) to estimate the average waiting time in queue **(in weeks)** for a user story to be processed.
    Please round up your answer to **3 decimals**.
    """

    return {
        "question": question_text,
        "options": {f"{x} weeks":let for let,x in zip('abcdefg',options)},
        "answer": f"{t_q_rounded} weeks",
        "data": {
            "r_a": r_a,
            "std_a": std_a,
            "r_p": r_p,
            "std_p": std_p,
            "u": round(u, 3),
            "m": m,
            "utilization": round(u, 3),
            "cv_a": round(cv_a, 3),
            "cv_p": round(cv_p, 3),
            "t_p": round(t_p, 3),
            "t_q": float(t_q_rounded)
        },
        "display_mode":"full_text"
    }

def question_kingman_inventory_in_line(seed):

    def tq(cv_a, cv_p, m, u, tp):
      t1 = ((cv_a**2) + (cv_p**2)) / 2
      t2 = (u**(np.sqrt(2 * (m + 1)) - 1)) / (m * (1 - u))
      tq = t1 * t2 * tp
      return tq

    random.seed(seed)

    # Step 1: Random inputs
    r_a = random.randint(25, 30)  # arrivals per week
    std_a = random.randint(60, 80)  # standard deviation of arrivals
    r_p = random.randint(31, 40)  # processing rate per week
    std_p = random.randint(8, 15)  # std dev of processing time
    m = 1  # number of servers

    # Step 2: Calculations
    u = r_a / r_p
    t_a = 1 / r_a
    t_p = 1 / r_p
    cv_a = std_a * t_a
    cv_p = std_p * t_p

    t_q = tq(cv_a, cv_p, m, u, t_p)
    t_q_rounded = round(t_q, 3)

    WIP_q = round(t_q * r_a,0)

    # print(WIP_q)

    # Step 3: Generate distractors
    distractors = set()
    while len(distractors) < 3:
        variation = random.choice([-3,-2,-1, 1, 2, 3])
        candidate = round(max(WIP_q + variation,0), 1)
        if candidate > 0 and candidate != WIP_q:
            distractors.add(candidate)
    options = list(distractors) + [WIP_q]
    random.seed(seed + 13)
    random.shuffle(options)

    # Step 4: Build question text
    question_text = f"""
    You are the Product Owner of an Agile team and due to a recent release, new user stories related to bugs arrive at about **{r_a}** per week with a standard deviation of **{std_a}**.
    A team member can debug approximately **{r_p}** stories per week with a standard deviation of **{std_p}**.
    For the time being, assume there is a **single (1) team member** processing these tasks.

    Please use the Kingman’s approximation (VUT formula) and Little's Law to estimate the average amount of user stories waiting in line (queue).
    Please round up your answer to **0 decimals**.
    """

    return {
        "question": question_text,
        "options": {f"{x:.0f} stories":let for let,x in zip('abcdefg',options)},
        "answer": f"{WIP_q:.0f} stories",
        "data": {
            "r_a": r_a,
            "std_a": std_a,
            "r_p": r_p,
            "std_p": std_p,
            "u": round(u, 3),
            "m": m,
            "utilization": round(u, 3),
            "cv_a": round(cv_a, 3),
            "cv_p": round(cv_p, 3),
            "t_p": round(t_p, 3),
            "t_q": float(t_q_rounded),
            "WIP_q": int(WIP_q)
        },
         "display_mode":"full_text"
    }

def question_kingman_total_time(seed):

    def tq(cv_a, cv_p, m, u, tp):
        t1 = ((cv_a**2) + (cv_p**2)) / 2
        t2 = (u**(np.sqrt(2 * (m + 1)) - 1)) / (m * (1 - u))
        tq = t1 * t2 * tp
        return tq

    random.seed(seed)

    # Step 1: Random inputs
    r_a = random.randint(25, 30)  # arrivals per week
    std_a = random.randint(60, 80)  # standard deviation of arrivals
    r_p = random.randint(31, 40)  # processing rate per week
    std_p = random.randint(8, 15)  # std dev of processing time
    m = 1  # number of servers

    # Step 2: Calculations
    u = r_a / r_p
    t_a = 1 / r_a
    t_p = 1 / r_p
    cv_a = std_a * t_a
    cv_p = std_p * t_p

    t_q = round(tq(cv_a, cv_p, m, u, t_p),3)
    t_total = round(t_q + t_p, 3)

    # Step 3: Generate distractors
    distractors = set()
    while len(distractors) < 3:
        variation = random.choice([-0.33,-0.255 ,-0.22, -0.155 ,-0.11,-0.055, 0.055 , 0.11,0.155, 0.22,0.255, 0.33])
        candidate = round(t_total + variation, 3)
        if candidate > 0 and candidate != t_total:
            distractors.add(candidate)
    options = list(distractors) + [t_total]
    random.shuffle(options)

    # Step 4: Build question text
    question_text = f"""
    You are the Product Owner of an Agile team and due to a recent release, new user stories related to bugs arrive at about **{r_a}** per week with a standard deviation of **{std_a}**.
    A team member can debug approximately **{r_p}** stories per week with a standard deviation of **{std_p}**.
    For the time being, assume there is a **single (1) team member** processing these tasks.

    Please use the Kingman’s approximation (VUT formula) to estimate the average total time (in weeks) a user story spends in the system (including both waiting and processing).
    Please round up your answer to **3 decimals**.
    """

    return {
        "question": question_text,
        "options": {f"{x} weeks":let for let,x in zip('abcdefg',options)},
        "answer": f"{t_total} weeks",
        "data": {
            "r_a": r_a,
            "std_a": std_a,
            "r_p": r_p,
            "std_p": std_p,
            "u": round(u, 3),
            "m": m,
            "utilization": round(u, 3),
            "cv_a": round(cv_a, 3),
            "cv_p": round(cv_p, 3),
            "t_p": round(t_p, 3),
            "t_q": round(t_q, 3),
            "t_total": t_total
        },
        "display_mode":"full_text"
    }

def question_kingman_inventory_total(seed):

    def tq(cv_a, cv_p, m, u, tp):
      t1 = ((cv_a**2) + (cv_p**2)) / 2
      t2 = (u**(np.sqrt(2 * (m + 1)) - 1)) / (m * (1 - u))
      tq = t1 * t2 * tp
      return tq

    random.seed(seed)

    # Step 1: Random inputs
    r_a = random.randint(25, 30)  # arrivals per week
    std_a = random.randint(60, 80)  # standard deviation of arrivals
    r_p = random.randint(31, 40)  # processing rate per week
    std_p = random.randint(8, 15)  # std dev of processing time
    m = 1  # number of servers

    # Step 2: Calculations
    u = r_a / r_p
    t_a = 1 / r_a
    t_p = 1 / r_p
    cv_a = std_a * t_a
    cv_p = std_p * t_p

    t_q = tq(cv_a, cv_p, m, u, t_p)
    t_q_rounded = round(t_q, 3)

    WIP_q = round(t_q * r_a,0)

    total_time = round(t_q + t_p, 3)
    total_WIP = round(total_time * r_a,0)

    # print(total_WIP)

    # Step 3: Generate distractors
    distractors = set()
    while len(distractors) < 3:
        variation = random.choice([-3,-2,-1, 1, 2, 3])
        candidate = round(max(total_WIP + variation,0), 0)
        if candidate > 0 and candidate != total_WIP:
            distractors.add(candidate)
    options = list(distractors) + [total_WIP]
    random.seed(seed + 14)
    random.shuffle(options)

    # Step 4: Build question text
    question_text = f"""
    You are the Product Owner of an Agile team and due to a recent release, new user stories related to bugs arrive at about **{r_a}** per week with a standard deviation of **{std_a}**.
    A team member can debug approximately **{r_p}** stories per week with a standard deviation of **{std_p}**.
    For the time being, assume there is a **single (1) team member** processing these tasks.

    Please use the Kingman’s approximation (VUT formula) and Little's Law to estimate the average amount of user stories in the system.
    Please round up your answer to **0 decimals**.
    """

    return {
        "question": question_text,
        "options": {f"{x:.0f} stories":let for let,x in zip('abcdefg',options)},
        "answer": f"{total_WIP:.0f} stories",
        "data": {
            "r_a": r_a,
            "std_a": std_a,
            "r_p": r_p,
            "std_p": std_p,
            "u": round(u, 3),
            "m": m,
            "utilization": round(u, 3),
            "cv_a": round(cv_a, 3),
            "cv_p": round(cv_p, 3),
            "t_p": round(t_p, 3),
            "t_q": float(t_q_rounded),
            "WIP_q": int(WIP_q),
            "total_WUP": int(total_WIP)
        },
         "display_mode":"full_text"
    }

def question_kingman_team_size(seed):

    def tq(cv_a, cv_p, m, u, tp):
        t1 = ((cv_a ** 2) + (cv_p ** 2)) / 2
        t2 = (u ** (np.sqrt(2 * (m + 1)) - 1)) / (m * (1 - u))
        return t1 * t2 * tp

    random.seed(seed)

    K = (7*8*60)

    # Step 1: Random inputs
    r_a = random.randint(25, 30)  # arrivals per week
    std_a = random.randint(60, 80)  # standard deviation of arrivals
    r_p = random.randint(31, 40)  # processing rate per week
    std_p = random.randint(8, 15)  # std dev of processing time

    # Step 2: Convert 120 minutes to weeks

    time_limit = 120

    # Step 3: Compute fixed quantities
    u = r_a / r_p
    t_p = 1 / r_p
    t_a = 1 / r_a
    cv_a = std_a * t_a
    cv_p = std_p * t_p

    # Step 4: Search for minimum m that satisfies T_t <= time_limit_weeks
    max_m = 20
    selected_m = None
    t_q_final = None
    for m in range(1, max_m + 1):
        u_m = r_a / (r_p * m)
        if u_m >= 1:  # system is unstable
            continue
        t_q = tq(cv_a, cv_p, m, u_m, t_p)
        t_total = t_q + t_p
        t_total = t_total*K

        if t_total <= time_limit:
            selected_m = m
            t_q_final = t_q*K
            u = u_m
            break

    # Step 5: Prepare options
    correct_answer = selected_m
    distractors = set()
    while len(distractors) < 3:
        variation = random.choice([-2, -1, 1, 2, 3, 4, 5])
        candidate = correct_answer + variation
        if candidate > 0 and candidate != correct_answer:
            distractors.add(candidate)
    options = list(distractors) + [correct_answer]
    options = sorted(set(options))
    random.shuffle(options)

    # Step 6: Build question text
    question_text = f"""
    You are the Product Owner of an Agile team and due to a recent release, new user stories related to bugs arrive at about **{r_a}** per week with a standard deviation of **{std_a}**.
    A team member can debug approximately **{r_p}** stories per week with a standard deviation of **{std_p}**.
    For the time being, assume there is a single team member processing these tasks. Based on recent market research, you discovered that customers expect bugs to be resolved in less than 120 minutes.

    With only one member in the development is not possible to meet this service level requirement so What should be the size of the development team to guarantee this service level?
    Use the Kingman’s approximation (VUT formula) with different **\"m\"** values to determine the minimum number of team members required. Please remember to adjust your utilization calculations \"u\" accordingly.
    Please assume:

    - 1 week = 7 days. The team is working every day of the week.
    - 1 working day = 8 hours. The team is working 8 hours a day.
    - Each new member has the same processing rate.

    How many team members are needed to ensure the required service level?
    Please round up your answer to **0 decimals** (number of team members cannot have decimal values).
    """

    return {
        "question": question_text,
        "options": {f"{x} team member":let for let,x in zip('abcdefg',options)},
        "answer": f"{correct_answer} team member",
        "data": {
            "r_a": r_a,
            "std_a": std_a,
            "r_p": r_p,
            "std_p": std_p,
            "cv_a": round(cv_a, 3),
            "cv_p": round(cv_p, 3),
            "u": round(u, 3),
            "t_p": round(t_p*K, 2),
            "t_q": round(t_q_final,2),
            "t_total": round(t_total, 2),
            "selected_m": selected_m
        },
        "display_mode":"full_text"
    }