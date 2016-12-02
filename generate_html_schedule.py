#!/usr/bin/env python3

import sys
import csv
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


hidden = '''<a href="#mycollapse{}" data-toggle="collapse">{}</a><div style="max-width:400px" id="mycollapse{}" class="collapse">
{}</div>'''
hidden_count = 0

def print_set(cur):
    global hidden_count

    if cur[0] is not None:
        event_name, _, colour = increments[cur[0]]
        event
        speakers = []
        info = []
        for name, title, abstract, homepage in cur[1]:
            if 'talk' in cur[0]:
                if len(homepage) > 0:
                    speakers.append('<a href="{}">{}</a>'.format(homepage, name))
                else:
                    speakers.append(name)
            if len(abstract) == 0:
                info.append(title)
            else:
                info.append(hidden.format(hidden_count, title, hidden_count, abstract))
                hidden_count += 1
        if len(cur[1]) > 1:
            event_name += "s"
        time = cur[2].strftime("%H:%M")
        print(row.format(colour, time, event_name, '\n'.join(speakers), '\n'.join(info)))

minute = datetime.timedelta(minutes=1)
ctime = datetime.datetime(2016,12,2,13,10,00)
cur = (None, [], ctime)
print(start)
with open('schedule.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for data_row in reader:
        key = data_row[1]
        if key not in increments:
            continue
        if key != cur[0]:
            print_set(cur)
            # Increment ctime to the next 15 min point
            while ctime.minute % 5 != 0:
                ctime += minute
            cur = (key, [], ctime)

        _, delta, colour = increments[key]
        event = data_row[0]
        title = data_row[5]
        abstract = data_row[6]
        homepage= data_row[7]
        cur[1].append((event, title, abstract, homepage))
        ctime += delta
print_set(cur)

print(end)
