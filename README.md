# TuneIn-Take-Home-Assignment

Written for TuneIn's Take Home Assignment.
I will make this repo private once my process with TuneIn is completed.

## Notes

All the code you need is found in `performance.py`.

However, in order to run this script, you will need to create a `.env` file. This is because I learned the hard way that I can't push
webhook links onto github, or Slack will disable it. I wouldn't want that happening to your webhook!

Example `.env` file:
```
WEBHOOK_URL = "[YOUR WEBHOOK HERE]"
```

## How the averages are calculated

I asked for clarification about this, but was unable to get a response, so the calculations are done as follows:

`Average Day = (sum of all revenues for that day) / (number of revenues for that day)`

`Average Week = (sum of all revenues for that week) / (number of revenues for that week)`

I'm happy to resubmit the script if any of these assumed formulas are incorrect, but will make a submission 
as of April 14, 2023 10:30 AM PST as I feel that this isn't a super blocking issue.