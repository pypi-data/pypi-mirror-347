import os
import datetime

path = r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Personal Computers\Chris\Research\Programming Scripts\AutoSPT\logs'

# DDMMYYYY HHMM
start = '01032025 0000'
end = '01012025 0000'
start = datetime.datetime.strptime(start, '%d%m%Y %H%M')
end = datetime.datetime.strptime(end, '%d%m%Y %H%M')