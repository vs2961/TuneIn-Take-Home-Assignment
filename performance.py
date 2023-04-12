import datetime
import requests

"""
Get the best performing day.
"""
def best_performing_day(times, revenue):
    seen_dates = {}
    for i, date in enumerate(times):
        day_str = f"{date.month}/{date.day}/{date.year}"
        seen_dates[day_str] = seen_dates.get(day_str, 0) + revenue[i]

    best_day = max(seen_dates, key=lambda day: seen_dates[day])
    return (best_day, seen_dates[best_day])

"""
Get the best performing week. Assume that the first day of the week is Sunday.
"""
def best_performing_week(times, revenue):
    seen_weeks = {}
    for i, date in enumerate(times):
        # Index weeks by the sunday of that week.
        sunday_of_week = date - datetime.timedelta(date.isoweekday() % 7)
        day_str = f"{sunday_of_week.month}/{sunday_of_week.day}/{sunday_of_week.year}"
        seen_weeks[day_str] = seen_weeks.get(day_str, 0) + revenue[i]

    best_week = max(seen_weeks, key=lambda day: seen_weeks[day])
    return (best_week, seen_weeks[best_week])
        

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
    			"text": "The best performing week on average was "
    		}
    	},
        {
    		"type": "section",
    		"block_id": "section4",
    		"text": {
    			"type": "mrkdwn",
    			"text": "Finally, here is the code that did the magic!\n"
    		},
            "accessory": {
    			"type": "file",
    			"image_url": "./performance.py",
    			"alt_text": "Haunted hotel image"
    		}
    	},
    ]
}

def populate_json(best_day, best_week):
    REQUEST_JSON["blocks"][1]["text"]["text"] += f"{best_day[0]} with an average revenue of {str(best_day[1])}."
    REQUEST_JSON["blocks"][2]["text"]["text"] += f"{best_week[0]} with an average revenue of {str(best_week[1])}."
    code = open("./performance.py").readlines()
    REQUEST_JSON["blocks"][3]["text"]["text"] += "```" + "".join(code) + "```"


CSV_TO_PARSE = "./Take Home Assignment_Ad Systems Automation Intern (1).csv"
WEBHOOK_URL = "https://hooks.slack.com/services/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"

if __name__ == '__main__':
    revenue_csv = open(CSV_TO_PARSE)
    times = []
    revenue = []
    headers = revenue_csv.readline()
    for line in revenue_csv:
        time, rev = line.strip().split(",")
        if time and rev:
            parsed_time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
            times.append(parsed_time)
            revenue.append(float(rev))
    best_day = best_performing_day(times, revenue)
    best_week = best_performing_week(times, revenue)
    populate_json(best_day, best_week)
    requests.post(WEBHOOK_URL, json=REQUEST_JSON)


