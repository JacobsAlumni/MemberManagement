#!/usr/bin/env python

import json
import datetime
from typing import List
import copy
import csv


with open('subscriptions.json') as f:
    subs: List = json.load(f)


    by_user = {}

    for sub in subs:

        user_id = sub['fields']['member']

        if  user_id not in by_user:
            by_user[user_id] = []

        by_user[user_id].append(sub)


    events = []

    for user_id, user_subs in by_user.items():
        for sub in user_subs:
            events.append({
                'action': '+',
                'tier': sub['fields']['tier'],
                'time': sub['fields']['start'][:10]# cut off the time from the datetime string
            })

            if sub['fields']['end']:
                events.append({
                    'action': '-',
                    'tier': sub['fields']['tier'],
                    'time': sub['fields']['end'][:10] # cut off the time from the datetime string
                })


    events = sorted(events, key=lambda x: x['time'])

    begin = {
        'st': 0,
        'co': 0,
        'pa': 0
    }
        
    snapshots = {
        events[0]['time']: begin
    }

    today = datetime.datetime.now().strftime('%F')


    current_date = events[0]['time']

    for event in events:
        if event['time'] > today:
            break
        
        if event['time'] != current_date:
            prev_date = current_date
            current_date = event['time']
            snapshots[current_date] = copy.deepcopy(snapshots[prev_date]) # Copy counts from previous snapshot

        if event['action'] == '-':
            snapshots[current_date][event['tier']] -= 1
        elif event['action'] == '+':
            snapshots[current_date][event['tier']] += 1



with open('snapshots.csv', 'w') as f:
    w = csv.writer(f)

    w.writerow(('Date', 'Starter', 'Contributor', 'Patron'))

    for t, snapshot in snapshots.items():
        w.writerow((t, snapshot['st'], snapshot['co'], snapshot['pa']))