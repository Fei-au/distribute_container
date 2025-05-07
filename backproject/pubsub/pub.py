from google.cloud import pubsub_v1
from django.core.cache import cache
import json
import time
import os
import logging

logger = logging.getLogger('pubsub')

project_id = os.getenv('PROJECT_ID')
topic_id = os.getenv('TOPIC_ID')

def publish_messages(publisher_id: str, uid, content):
    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    data_dict = {
        "uid": uid,
        "content": content
    }
    data_str = json.dumps(data_dict)
    # Data must be a bytestring
    data = data_str.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    pub_res_id = future.result()
    l = cache.get(publisher_id)
    if l is None:
        l = []
    else:
        l = json.loads(l)
    l.append(f"Published {pub_res_id}:  {data_str} on {topic_path} at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    cache.set(publisher_id, json.dumps(l), 60*60*2)  # 2 hours (in seconds)
    logger.info(f"Published message successfully: {uid}")
