from google.cloud import pubsub_v1
from django.core.cache import cache
import threading

project_id = "glass-gasket-415918"
topic_id = "msgq"
subscription_id = "celeryworker"

def publish_messages():
    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    for n in range(1, 10):
        data_str = f"Message number {n}"
        # Data must be a bytestring
        data = data_str.encode("utf-8")
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data)
        print(future.result())

    print(f"Published messages to {topic_path}.")
    

def start_subscriber(subscriber_id: str, timeout: float = None):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message}.")
        '''
            {
                data: b'Message number 8'
                ordering_key: ''
                attributes: {}
            }
        '''
        print(f"subscriber {subscriber_id}, Data: {message.data.decode('utf-8')}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Subscriber {subscriber_id} listening on {subscription_path}..\n")

    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()

def receive_messages():
    # 创建两个subscriber线程
    subscriber1 = threading.Thread(target=start_subscriber, args=("subscriber1", 30.0))
    subscriber2 = threading.Thread(target=start_subscriber, args=("subscriber2", 30.0))

    # 启动线程
    subscriber1.start()
    subscriber2.start()

    # 等待线程结束
    subscriber1.join()
    subscriber2.join()