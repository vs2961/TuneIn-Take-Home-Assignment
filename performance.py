import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def best_performing_day(times: list[datetime.datetime], revenue: list[float]):
    '''Get the best performing day.'''
    seen_dates = {}
    for i, date in enumerate(times):
        # Index dates by the form mm/dd/yyyy
        day_str = f"{date.month}/{date.day}/{date.year}"

        # Save the total revenue earned, as well as the number of different revenue for that day
        seen_dates[day_str] = seen_dates.get(day_str, [0, 0])
        seen_dates[day_str][0] += revenue[i]
        seen_dates[day_str][1] += 1

    # Get the best day by total revenue
    best_day = max(seen_dates, key=lambda day: seen_dates[day][0] / seen_dates[day][1])
    return (best_day, seen_dates[best_day][0] / seen_dates[best_day][1])


def best_performing_week(times: list[datetime.datetime], revenue: list[float]):
    '''Get the best performing week. Assume that the first day of the week is Sunday.'''
    seen_weeks = {}
    for i, date in enumerate(times):
        # Index weeks by the sunday of that week, of form mm/dd/yyyy.
        sunday_of_week = date - datetime.timedelta(date.isoweekday() % 7)
        day_str = f"{sunday_of_week.month}/{sunday_of_week.day}/{sunday_of_week.year}"

        # Save the total revenue earned
        seen_weeks[day_str] = seen_weeks.get(day_str, [0, 0])
        seen_weeks[day_str][0] += revenue[i]
        seen_weeks[day_str][1] += 1

    # Get the best week by total revenue
    best_week = max(seen_weeks, key=lambda day: seen_weeks[day][0] / seen_weeks[day][1])
    return (best_week, seen_weeks[best_week][0] / seen_weeks[best_week][1])
        

REQUEST_JSON = {
    "blocks": [
    	{
    		"type": "section",
    		"text": {
    			"type": "mrkdwn",
    			"text": "Hi, my name is Victor Siu, and this is my submission for the take home assignment!"
    		}
    	},
    	{
    		"type": "section",
    		"block_id": "section2",
    		"text": {
    			"type": "mrkdwn",
    			"text": "According to your csv, the best performing day on average was "
    		}
    	},
    	{
    		"type": "section",
    		"block_id": "section3",
    		"text": {
    			"type": "mrkdwn",
    			"text": "The best performing week on average was the week of "
    		}
    	},
        {
    		"type": "section",
    		"block_id": "section4",
    		"text": {
    			"type": "mrkdwn",
    			"text": "Finally, here is the code that did the magic!\n"
    		}
    	},
    ]
}

def populate_json(best_day, best_week):
    '''Populate the slack message with the desired outputs'''
    REQUEST_JSON["blocks"][1]["text"]["text"] += f"*{best_day[0]}* with an average revenue of *{str(best_day[1])}*."
    REQUEST_JSON["blocks"][2]["text"]["text"] += f"*{best_week[0]}* with an average revenue of *{str(best_week[1])}*."
    code = open("./performance.py").readlines()
    REQUEST_JSON["blocks"][3]["text"]["text"] += "https://github.com/vs2961/TuneIn-Take-Home-Assignment"


CSV_TO_PARSE = "./Take Home Assignment_Ad Systems Automation Intern (1).csv"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if __name__ == '__main__':
    revenue_csv = open(CSV_TO_PARSE)
    times = []
    revenue = []
    headers = revenue_csv.readline()
    # Parse the CSV for the data and put into lists.
    for line in revenue_csv:
        time, rev = line.strip().split(",")
        if time and rev:
            parsed_time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
            times.append(parsed_time)
            revenue.append(float(rev))
    
    best_day = best_performing_day(times, revenue)
    best_week = best_performing_week(times, revenue)
    populate_json(best_day, best_week)
    
    # Send the slack message
    x = requests.post(WEBHOOK_URL, json=REQUEST_JSON)
    print(x.text)


