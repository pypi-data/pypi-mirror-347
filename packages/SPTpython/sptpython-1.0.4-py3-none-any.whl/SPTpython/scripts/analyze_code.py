import os
# Whitelist of folders to include in the line count
whitelist = ["analysis", "C_code", "pySPT", "4th_year_review"]
ignore = ["kinetic_monte_carlo.c"]

results = {}
def count_lines_in_py_files(directory):
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        # Filter directories to only include those in the whitelist
        dirs[:] = [d for d in dirs if d in whitelist]
        for file in files:
            if file.endswith(".py") or file.endswith(".c") or file.endswith(".h"):
                file_path = os.path.join(root, file)
                if file in ignore:
                    print(f"Skipping {file_path} as it is in the ignore list.")
                    continue
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        line_count = sum(1 for _ in f)
                        results[file] = line_count
                        total_lines += line_count
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")
    
    # Find the longest key for padding
    max_key_length = max(len(key) for key in results.keys())
    print("\nDetailed line counts:")
    for file_path, line_count in results.items():
        print(f"{file_path.ljust(max_key_length)} : {line_count}")
    
    message = f"Total lines of code in whitelisted directories: {total_lines}"
    print()
    print('-'*len(message))
    print(message)

def count_log_files(directory):
    log_counts = {"processing": 0, "simulation": 0}
    log_folder = os.path.join(directory, "logs")
    
    if not os.path.exists(log_folder):
        print(f"Logs folder not found at {log_folder}")
        return log_counts

    for subfolder in log_counts.keys():
        subfolder_path = os.path.join(log_folder, subfolder)
        if not os.path.exists(subfolder_path):
            print(f"Subfolder '{subfolder}' not found in logs folder.")
            continue
        
        try:
            log_counts[subfolder] = sum(1 for file in os.listdir(subfolder_path) if file.endswith(".log"))
        except Exception as e:
            print(f"Could not count .log files in {subfolder_path}: {e}")
    
    print("\nLog file counts:")
    for subfolder, count in log_counts.items():
        print(f"{subfolder.capitalize()} : {count}")
    
def main():
    # Move one directory up
    current_directory = os.path.dirname(os.path.dirname(__file__))
    count_lines_in_py_files(current_directory)
    count_log_files(current_directory)

if __name__ == "__main__":
    main()