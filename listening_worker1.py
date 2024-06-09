'''This program listens for work messages continuously.
    Start multiple versions to add more workers.

    Author: Denise Case
    Date: January 15, 2023

    Modified by: Laura Dooley
    Date: June 1, 2024
'''

import csv
import pika
import sys
import time
from pathlib import Path
from collections import deque


# Define the path to the CSV file
output_csv_path = Path("smoker-temps.csv")

# Ensure the CSV file exists 
if not output_csv_path.exists():
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Smoker Temp"])

# Define deques to keep track of temperatures for alerts
smoker_temps = deque(maxlen=5)  # Smoker Alert! -  2.5 minutes of data (5 * 30 seconds)
food_temps = { "food_a_queue": deque(maxlen=5), "food_b_queue": deque(maxlen=5) } # Food Stall Alert! - for 10 minute of data (20 * 30)

# Define a callback function to be called when a message is received


def callback(ch, method, properties, body):
    """Define behavior on getting a message."""
    queue_name = method.routing_key
    original_message = body.decode()

    
    print(f" [x] Received from {queue_name}: {original_message}")

    # Add temperature to appropriate deque
    try:
        # Assuming the message format is "Smoker Temp = <temperature_value>"
        temp_str = original_message.split("=")[1].strip()
        temp = float(temp_str)

        if queue_name == "smoker_queue":
            smoker_temps.append(temp)
            check_smoker_alert()
        elif queue_name in food_temps:
            food_temps[queue_name].append(temp)
            check_food_alert(queue_name)
    except ValueError:
        print(f"Received invalid temperature value: {original_message}")


    # When done with task, tell the user
    print(" [x] Done.")
    # Acknowledge the message was received and processed (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def check_smoker_alert():
    """Check for smoker alert."""
    if len(smoker_temps) == smoker_temps.maxlen:
        if smoker_temps[0] - smoker_temps[-1] > 15:
            print("Smoker alert!!! Check Smoker")

def check_food_alert(queue_name):
    """Check for food stall alert."""
    temps = food_temps[queue_name]
    if len(temps) == temps.maxlen:
        if abs(temps[0] - temps[-1]) < 1:
            print(f"Food stall alert in {queue_name}!!! Check Food")

# Define a main function to run the program
def main(hn: str = "localhost", queues: list = None):
    """Continuously listen for task messages on named queues."""
    if queues is None:
        queues = []

    # When a statement can go wrong, use a try-except block
    try:
        # Try this code, if it works, keep going
        # Create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # Except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # Use the connection to create a communication channel
        channel = connection.channel()

        for queue in queues:
            # Use the channel to declare a durable queue
            # A durable queue will survive a RabbitMQ server restart
            # and help ensure messages are processed in order
            # Messages will not be deleted until the consumer acknowledges
            channel.queue_declare(queue=queue, durable=True)

            # The QoS level controls the number of messages
            # that can be in-flight (unacknowledged by the consumer)
            # at any given time.
            # Set the prefetch count to one to limit the number of messages
            # being consumed and processed concurrently.
            # This helps prevent a worker from becoming overwhelmed
            # and improve the overall system performance.
            # Prefetch_count = per consumer limit of unacknowledged messages      
            channel.basic_qos(prefetch_count=1)

            # Configure the channel to listen on a specific queue,
            # use the callback function named callback,
            # and do not auto-acknowledge the message (let the callback handle it)
            channel.basic_consume(queue=queue, on_message_callback=callback)

        # Print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

        # Start consuming messages via the communication channel
        channel.start_consuming()

    # Except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # Call the main function with the information needed
    main("localhost", ["smoker_queue", "food_a_queue", "food_b_queue"])
