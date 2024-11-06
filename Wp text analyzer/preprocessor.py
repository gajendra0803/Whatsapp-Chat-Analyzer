import re
import pandas as pd
import datetime

def preprocess(data):
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APM]{2}\s-\s)(.*)"

    matches = re.findall(pattern, data)
    messages = [match[1] for match in matches]
    pattern1 = r"(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APM]{2}\s-\s)"
    dates = re.findall(pattern1, data)

    df = pd.DataFrame({'User_messages': messages, 'message_date': dates})
    # Converting message date_type
    df['message_date'] = df['message_date'].str.rstrip(' -')
    df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %H:%M %p")

    users = []
    messages = []
    for message in df['User_messages']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['User_messages'], inplace=True)

    df['Year'] = df['message_date'].dt.year
    df['Month'] = df['message_date'].dt.month_name()
    df['day_name'] = df['message_date'].dt.day_name()
    df['month_num'] = df['message_date'].dt.month
    df['day'] = df['message_date'].dt.day
    df['date'] = df['message_date'].dt.date
    df['Hour'] = df['message_date'].dt.hour
    df['Minute'] = df['message_date'].dt.minute

    period = []
    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 11:
            period.append(str(hour) + "-" + str('12'))
        elif hour == 12:
            period.append(str(12) + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df