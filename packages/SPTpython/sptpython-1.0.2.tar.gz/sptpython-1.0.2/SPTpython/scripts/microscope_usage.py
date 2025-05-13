import os
import datetime
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates

def get_time_from_log_item(s):
    """Extracts the time from a log item string."""
    re_match = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d{3}'
    time_s = re.search(re_match, s)
    if time_s is None:
        return -1
    time_s = time_s.group(1)
    # print(time_s)
    return datetime.datetime.strptime(time_s, '%Y-%m-%d %H:%M:%S')

def plot_ranges(ranges, title):
    # Set up the plot
    fig, ax = plt.subplots(figsize=(12, 2))
    y_pos = 0.5

    # Plot each time block
    for start, end, is_active in ranges:
        color = 'green' if is_active else 'red'
        rect = mpatches.Rectangle((mdates.date2num(start), y_pos - 0.2),
                                mdates.date2num(end) - mdates.date2num(start),
                                0.4, color=color)
        ax.add_patch(rect)

    # Configure date axis formatting for months + days + time
    ax.set_xlim(mdates.date2num(ranges[0][0]), mdates.date2num(ranges[-1][1]))
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel('Time')
    ax.set_title(title)

    # Set major formatter to show month, day, and time
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))

    # Rotate date labels for readability
    fig.autofmt_xdate()

    plt.tight_layout()
    plt.show()
    
def calculate_usage(start_range, end_range):
    path = r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Personal Computers\Chris\Research\Programming Scripts\AutoSPT\logs'
    ranges = []

    total_time = datetime.timedelta(0)
    for file in os.listdir(path):
        try:
            match = re.match(r'(\d{8}_\d{6})', file)
            date = datetime.datetime.strptime(match.group(1), '%Y%m%d_%H%M%S')
            if start_range <= date <= end_range:
                with open(os.path.join(path, file), 'r') as f:
                    lines = f.readlines()
                    if lines == []:
                        continue
                    exp_start = get_time_from_log_item(lines[0])
                    idx = -1
                    while get_time_from_log_item(lines[idx])==-1:
                        idx -= 1
                    exp_end = get_time_from_log_item(lines[idx])
                    total_time += (exp_end - exp_start)
                    
                    if ranges == []:
                        ranges.append((start_range, exp_start, False))
                    else:
                        ranges.append((ranges[-1][1], exp_start,False))
                    ranges.append((exp_start, exp_end, True))
            
                    
        except Exception as e:
            print(f"Error parsing date from filename: {file}")
            print(e)
            
    ranges.append((exp_end, datetime.datetime.now(), False))
            
    total_used = total_time.total_seconds() / 3600
    total_possible = (end_range - start_range).total_seconds() / 3600
    print(f"Total time in hours: {total_used:.2f} hours")
    print(f"Total time range: {total_possible:.2f} hours")
    print(f"Usage: {total_used/total_possible:.2%}")

    plot_ranges(ranges, title = f'{start_range.strftime("%d/%m/%Y %H:%M")} - {end_range.strftime("%d/%m/%Y %H:%M")}: {total_used:.2f} h / {total_possible:.2f} h ({total_used/total_possible:.2%})')
    
def main():
    modes = ['2 weeks', 'YTD', 'all']
    mode = modes[0]
    
    # DDMMYYYY HHMM
    if mode == '2 weeks':
        end_range = datetime.datetime.now()
        start_range = end_range - datetime.timedelta(days=14)
    elif mode == 'YTD':
        start_range = '01012025 0000'
        end_range = datetime.datetime.now()
        start_range = datetime.datetime.strptime(start_range, '%d%m%Y %H%M')
    elif mode == 'all':
        # earliest time in logs
        start_range = '14052023 0000'
        end_range = datetime.datetime.now()
        start_range = datetime.datetime.strptime(start_range, '%d%m%Y %H%M')
    
    # end_range = datetime.datetime.strptime(end_range, '%d%m%Y %H%M')
    calculate_usage(start_range, end_range)

    
if __name__ == '__main__':
    main()