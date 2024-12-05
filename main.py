import csv
from collections import Counter

# Function to parse a single log line
def parse_log(log_line):
    parts = log_line.split()
    ip_address = parts[0]
    method, endpoint = parts[5][1:], parts[6]
    status_code = int(parts[8])
    return ip_address, method, endpoint, status_code

# Function to analyze log data
def analyze_logs(log_lines):
    ip_counter = Counter()
    endpoint_counter = Counter()
    suspicious_ips = set()

    for log_line in log_lines:
        ip_address, method, endpoint, status_code = parse_log(log_line)

        # Count requests by IP
        ip_counter[ip_address] += 1

        # Count requests by endpoint
        endpoint_counter[endpoint] += 1

        # Detect suspicious activity (e.g., repeated failed login attempts)
        if status_code == 401 and "/login" in endpoint:
            suspicious_ips.add(ip_address)

    # Get the most frequently accessed endpoint
    most_frequent_endpoint = endpoint_counter.most_common(1)[0] if endpoint_counter else ("None", 0)

    return ip_counter, most_frequent_endpoint, suspicious_ips

# Function to save results to a CSV file
def save_to_csv(ip_counts, most_frequent_endpoint, suspicious_ips, output_file="log_analysis.csv"):
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write IP request counts
        writer.writerow(["IP Address", "Request Count"])
        for ip, count in ip_counts.items():
            writer.writerow([ip, count])

        # Write the most accessed endpoint
        writer.writerow([])
        writer.writerow(["Most Frequently Accessed Endpoint", "Access Count"])
        writer.writerow([most_frequent_endpoint[0], most_frequent_endpoint[1]])

        # Write suspicious activity details
        writer.writerow([])
        writer.writerow(["Suspicious IP Addresses"])
        for ip in suspicious_ips:
            writer.writerow([ip])

# Main function to process logs and output results
def main():
    input_file = "sample.log"  # Log file name
    output_file = "log_analysis.csv"  # Output CSV file name

    try:
        # Read the log file
        with open(input_file, "r") as file:
            log_data = file.readlines()

        # Analyze the log data
        ip_counts, most_frequent_endpoint, suspicious_ips = analyze_logs(log_data)

        # Display the results in the terminal
        print(f"{'IP Address':<20} {'Request Count'}")
        for ip, count in ip_counts.most_common():
            print(f"{ip:<20} {count}")

        print(f"\nMost Frequently Accessed Endpoint:")
        print(f"{most_frequent_endpoint[0]} (Accessed {most_frequent_endpoint[1]} times)")

        if suspicious_ips:
            print("\nSuspicious Activity Detected:")
            for ip in suspicious_ips:
                print(f"- {ip}")
        else:
            print("\nNo suspicious activity detected.")

        # Save results to a CSV file
        save_to_csv(ip_counts, most_frequent_endpoint, suspicious_ips, output_file)
        print(f"\nResults saved to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found. Please ensure it exists in the same directory.")

if __name__ == "__main__":
    main()
