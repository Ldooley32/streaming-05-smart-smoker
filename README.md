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


# sources 
https://nwmissouri.instructure.com/courses/60464/discussion_topics/498771

- [RabbitMQ Tutorial - Work Queues](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)