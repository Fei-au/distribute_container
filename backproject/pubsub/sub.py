import os
from google.cloud import pubsub_v1
from django.core.cache import cache
import threading
import json
import logging

logger = logging.getLogger('pubsub')



project_id = os.getenv('PROJECT_ID')
pubsub_subscription_id = os.getenv('PUBSUB_SUBSCRIPTION_ID')

def receive_messages(subscriber_id: str, timeout: float):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, pubsub_subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        # Pretend to process the message.
        '''
            {
                data: b'{"uid": uid, "content": content}'
                ordering_key: ''
                attributes: {}
            }
        '''
        data = message.data.decode('utf-8')
        key = f'{subscriber_id}'
        # l = cache.get(key)
        # if l is None:
        #     l = []
        # else:
        #     l = json.loads(l)
        # l.append(f"subscriber {subscriber_id}, Data: {data}")
        # cache.set(key, json.dumps(l), 60*60*24)  # 1 day1 (in seconds l)
        # logger.info("Received message successfully")
        save_messages(key, data)
        logger.info("Received message successfully")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    logger.info(f"Subscriber {subscriber_id} listening on {subscription_path}..\n")

    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
            
def save_messages(key: str, data: str, ):
        l = cache.get(key)
        if l is None:
            l = []
        else:
            l = json.loads(l)
        l.append(f"{key}, Data: {data}")
        cache.set(key, json.dumps(l), 60*60*24)  # 1 day1 (in seconds l)

# def receive_messages():
#     # 创建两个subscriber线程
#     subscriber1 = threading.Thread(target=start_subscriber, args=("subscriber1", 30.0))
#     subscriber2 = threading.Thread(target=start_subscriber, args=("subscriber2", 30.0))

#     # 启动线程
#     subscriber1.start()
#     subscriber2.start()

#     # 等待线程结束
#     subscriber1.join()
#     subscriber2.join()