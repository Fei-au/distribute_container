#!/bin/bash for python container
/usr/local/bin/supervisord -c /app/subscriber.conf

# For ec2 vm. No, we run this sh in container
# /usr/bin/supervisord -c /app/subscriber.conf
