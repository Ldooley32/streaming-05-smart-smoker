## streaming-05-smart-smoker

# Overview
Implementing analytics for a "smart smoker" (as in slow cooked food). Design a system and implement a producer.

# Step 1 - Creat a work space 
    1. create a new repo "streaming-05-smart-smoker"
    2. add README.MD file, and .gitignore file
    3. Clone to machine
    4. add smoker-temps.csv file
    5. create a producer file "emitter_of_tasks.py"

# Step 2 -  Design and execute a producer
    a. the produce will have 3 queues 
        1. Smoker Temp 
        2. Food A Temp
        3. Food B Temp
    b. bass the coding off of Project 4
    c. Will terminate on own
    d. Ensure the main function only executes when the script is run directly
    e. Run emitter_of_tasks.py (say y to monitor RabbitMQ queues)

# Step 3 - Design and excute 3 types of consumers
    a. design a consumer to listen to one type of 3 queues.
    b. make a terminate command 
        '''try:
        # Use the connection to create a communication channel
        channel = connection.channel()

        # Use the channel to declare a durable queue
        # A durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # Messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=qn, durable=True)

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
        channel.basic_consume(queue=qn, on_message_callback=callback)

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
        connection.close()'''

    c. Ensure the main function only executes when the script is run directly
    d. Launch workers 

# sources 
https://nwmissouri.instructure.com/courses/60464/discussion_topics/498771

- [RabbitMQ Tutorial - Work Queues](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)