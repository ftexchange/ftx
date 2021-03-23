**FTX Reporting for farming futures funding.**

Reporting module sends two types of messages:
1. Daily reports of the farming result including previous day resul and current position on spot and futures market.
2. Hourly notification if funding rate become negative.

Before starting you have to fill the data.py file with 
* gmail login/password from the email used for sending notifications;
* email where to send notification
* API keys from you account (please use read-only keys for the safety reasons)
* markets you want to analize

After filling the data.py file start the process by executing start_reporting.py 
