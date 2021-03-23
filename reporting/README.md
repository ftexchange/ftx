# FTX Reporting for farming futures funding.

Reporting module sends two types of messages:
1. Daily reports of the farming result including previous day results and current position on the spot and futures market.
2. Hourly notification if funding rate becomes negative.

Before starting you have to fill the data.py file with 
* gmail login/password from the email used for sending notifications;
* email where to send notification
* API keys from your account (please use read-only keys for safety reasons)
* markets you want to analyze

After filling the data.py file start the process by executing start_reporting.py 
