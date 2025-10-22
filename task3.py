import sys
from collections import defaultdict
from typing import List, Dict, Union

def parse_log_line(line: str) -> Union[Dict[str, str], None]:
    """
    Parses a single line of the log, separates it into date, time, lvl and message.
    """
    try:
        
        parts = line.split(maxsplit=3) # 4 pieces split date, time, lvl, msg
        if len(parts) < 4:
            return None #invalid log line
        date, time, level, message = parts[0], parts[1], parts[2], parts[3].strip()
        
        valid_levels = {'INFO', 'ERROR', 'DEBUG', 'WARNING'}
        if level not in valid_levels:
            return None #invalid log level

        return {
            'date': date,
            'time': time,
            'level': level,
            'message': message
        }
    except Exception as e:
        #other unexpected parsing errors
        print(f"String Parsing Error: '{line.strip()}' - {e}", file=sys.stderr) 
        return None

def load_logs(file_path: str) -> List[Dict[str, str]]:
    """
    Loads log files from the specified path and parses each line.
    """
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            logs = [
                log_entry
                for line in file 
                if (log_entry := parse_log_line(line)) is not None
            ]
        return logs
    except FileNotFoundError:
        print(f"[FileNotFoundError] '{file_path}' not found.", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        return []

def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    """
    Filters logs by certain lvl.
    """
    target_level = level.upper()
    return list(filter(lambda log: log['level'] == target_level, logs)) #filter by lvl

def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Counts the number of records for each logging lvl.
    """
    counts = defaultdict(int)
    for log in logs:
        counts[log['level']] += 1
    return dict(counts)

def display_log_counts(counts: Dict[str, int]):
    """
    Formats and displays log count statistics as a table.
    """
    print("\nРівень логування | Кількість")
    print("-----------------|----------")

    for level, count in sorted(counts.items(), key=lambda item: item[1], reverse=True): #sort by count desc
        print(f"{level:<16} | {count}")
    print("-" * 30)

def display_filtered_logs(filtered_logs: List[Dict[str, str]], level: str):
    """
    Displays details of filtered log entries.
    """
    if filtered_logs:
        print(f"\nДеталі логів для рівня '{level.upper()}':")
        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}") #displays log details
    else:
        print(f"\nДеталі логів для рівня '{level.upper()}': Не знайдено записів.") #no logs found
    print("-" * 30)

def main():
    """
    analyzes logs by file path, counts log lvls and optionally filters and displays logs of a certain lvl.
    """
    if len(sys.argv) < 2:
        print("Usage example>>> python3 task3.py task3_logfile.log [LVL - optional]", file=sys.stderr)
        #python3 task3.py task3_logfile.log info >>> Деталі логів для рівня 'INFO': ... (log details)
        #python3 task3.py task3_logfile.log test >>> Деталі логів для рівня 'TEST': Не знайдено записів.
        sys.exit(1)

    log_file_path = sys.argv[1]
    filter_level = sys.argv[2] if len(sys.argv) > 2 else None

    #load and parse logs
    all_logs = load_logs(log_file_path)
    if not all_logs and not filter_level: #exit if no logs and no filter
        sys.exit(0) 

    log_counts = count_logs_by_level(all_logs) #count logs by lvl
    display_log_counts(log_counts) #general log lvl counts

    if filter_level: #if filter lvl provided, filter and display logs
        filtered_logs = filter_logs_by_level(all_logs, filter_level)
        display_filtered_logs(filtered_logs, filter_level)

if __name__ == "__main__":
    main()