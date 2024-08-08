import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def plot_cron_schedule(cron_expression: str):
    """
    Generates and displays a timeline chart for the given crontab expression,
    adjusting the x-axis scale based on the schedule (daily, weekly, monthly).
    
    Args:
    cron_expression (str): The crontab expression, e.g., "0 0,4,8,12,16,20 * * *".
    """
    # Function to parse crontab expression and generate execution times
    def generate_execution_times(cron_expression):
        parts = cron_expression.split()
        minute = int(parts[0])
        hours = [int(h) for h in parts[1].split(',')]
        days_of_month = parts[2]
        months = parts[3]
        days_of_week = parts[4]

        times = []

        if days_of_month == '*' and days_of_week == '*':
            # Schedule is daily
            current_time = datetime.now().replace(hour=0, minute=minute, second=0, microsecond=0)
            for hour in hours:
                times.append(current_time.replace(hour=hour))
        elif days_of_week != '*' and days_of_month == '*':
            # Schedule is weekly
            current_time = datetime.now().replace(hour=0, minute=minute, second=0, microsecond=0)
            week_start = current_time - timedelta(days=current_time.weekday())
            for day in days_of_week.split(','):
                for hour in hours:
                    execution_time = week_start + timedelta(days=int(day) - 1)
                    times.append(execution_time.replace(hour=hour))
        elif days_of_month != '*' and days_of_week == '*':
            # Schedule is monthly
            current_time = datetime.now().replace(hour=0, minute=minute, second=0, microsecond=0)
            for day in days_of_month.split(','):
                for hour in hours:
                    times.append(current_time.replace(day=int(day), hour=hour))

        return times

    # Generate execution times based on input
    execution_times = generate_execution_times(cron_expression)

    if execution_times:
        st.write("The cron job is scheduled to run at the following times:")

        # Determine the appropriate x-axis range
        time_labels = [time.strftime("%Y-%m-%d %H:%M") for time in execution_times]
        fig, ax = plt.subplots(figsize=(10, 2))

        ax.scatter(execution_times, [1] * len(execution_times), color='blue')
        ax.set_yticks([])
        ax.set_xticks(execution_times)
        ax.set_xticklabels(time_labels, rotation=45, ha='right')
        
        if len(set([t.date() for t in execution_times])) > 1:
            # Adjust x-axis for weekly or monthly scale
            ax.set_xlim([execution_times[0] - timedelta(days=1), execution_times[-1] + timedelta(days=1)])
        else:
            # Adjust x-axis for daily scale
            ax.set_xlim([execution_times[0] - timedelta(hours=1), execution_times[-1] + timedelta(hours=1)])

        st.pyplot(fig)
    else:
        st.write("Please enter a valid crontab expression.")

# Example usage within a Streamlit app
st.title("Cron Job Schedule Visualization")

# Input for crontab expression
cron_expression = st.text_input("Enter your crontab expression:", "")

# Check if the user has entered a value
if cron_expression.strip() == "":
    st.write("Please enter a crontab definition.")
else:
    # Plot the cron schedule
    plot_cron_schedule(cron_expression)