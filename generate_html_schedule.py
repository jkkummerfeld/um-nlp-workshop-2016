#!/usr/bin/env python3

import sys
import datetime

increments = {
    'Welcome': ('Welcome', datetime.timedelta(minutes=10), ''),
    'Photo': ('Group Photo', datetime.timedelta(minutes=4), ' class="warning"'),
    'Tea Break': ('Tea Break', datetime.timedelta(minutes=30), ' class="success"'),
    'Dinner': ('Dinner', datetime.timedelta(minutes=60), ' class="success"'),
    'PhD talk': ('PhD talk', datetime.timedelta(minutes=11, seconds=0), ''),
    'Faculty talk': ('Faculty talk', datetime.timedelta(minutes=11, seconds=0), ''),
    'Postdoc talk': ('Postdoctoral talk', datetime.timedelta(minutes=11, seconds=0), ''),
    'Ugrad talk': ('Undergraduate talk', datetime.timedelta(minutes=2, seconds=30), ''),
    'MS talk': ('Masters talk', datetime.timedelta(minutes=2, seconds=30), ''),
}

start = '''
<table class="table">
  <thead>
    <tr>
      <th>Start Time</th>
      <th>Event</th>
      <th>Speaker</th>
      <th>Title</th>
    </tr>
  </thead>
  <tbody>'''
end = '''  </tbody>
</table>
'''
row = '''    <tr{}>
      <td>{}</td>
      <td>{}</td>
      <td style="white-space:pre-wrap ; word-wrap:break-word;">{}</td>
      <td style="white-space:pre-wrap ; word-wrap:break-word;">{}</td>
    </tr>'''

def print_set(cur):
    if cur[0] is not None:
        name, _, colour = increments[cur[0]]
        event = '\n'.join(cur[1])
        if len(cur[1]) > 1:
            name += "s"
        time = cur[2].strftime("%H:%M")
        print(row.format(colour, time, name, event, ""))

minute = datetime.timedelta(minutes=1)
ctime = datetime.datetime(2016,12,2,13,10,00)
cur = (None, [], ctime)
print(start)
for line in open("schedule.txt"):
    done = False
    for key in increments:
        if line.strip().endswith(key) and not done:
            if key != cur[0]:
                print_set(cur)
                # Increment ctime to the next 15 min point
                while ctime.minute % 5 != 0:
                    ctime += minute
                cur = (key, [], ctime)

            _, delta, colour = increments[key]
            event = line.strip()[:-len(key)].strip()
            cur[1].append(event)

            done = True
            ctime += delta
    if not done:
        print("Missed: '{}'".format(line.strip()))
print_set(cur)

print(end)
