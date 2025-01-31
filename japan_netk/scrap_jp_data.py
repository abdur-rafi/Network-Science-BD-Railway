import requests
import threading
from queue import Queue

# Configuration
base_url = "https://doko-train.jp/json/line/en/{}.json"
start_id = 0
end_id = 100
max_retries = 5
num_threads = 12
output_dir = "output"  # Directory to save the scraped files

# Create a queue to manage tasks
task_queue = Queue()

# Function to scrape a URL
def scrape_data(queue):
    while not queue.empty():
        line_id = queue.get()
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(base_url.format(line_id), timeout=10)
                response.raise_for_status()
                # Save the data to a file
                with open(f"{output_dir}/{line_id}.json", "w", encoding="utf-8") as file:
                    file.write(response.text)
                print(f"Successfully scraped: {line_id}")
                break
            except requests.RequestException as e:
                retries += 1
                print(f"Retry {retries}/{max_retries} for {line_id} due to error: {e}")
        else:
            print(f"Failed to scrape: {line_id} after {max_retries} retries")
        queue.task_done()

# Main function
def main():
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Populate the task queue
    for line_id in range(start_id, end_id + 1):
        task_queue.put(line_id)

    # Create and start threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=scrape_data, args=(task_queue,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    task_queue.join()
    for thread in threads:
        thread.join()

    print("Scraping completed!")

if __name__ == "__main__":
    main()
