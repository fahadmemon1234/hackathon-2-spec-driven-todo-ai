from kafka import KafkaProducer, KafkaConsumer
import json
import time

def test_kafka_connectivity():
    try:
        # Connect to Kafka running on localhost:29092 (external port)
        producer = KafkaProducer(
            bootstrap_servers=['localhost:29092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(2, 8, 0)  # Match your Kafka version
        )

        consumer = KafkaConsumer(
            'task-events',
            bootstrap_servers=['localhost:29092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            group_id='test-group'
        )

        # Send a test message
        topic = 'task-events'
        message = {
            'event': 'test-connectivity',
            'timestamp': '2026-01-26T10:00:00Z',
            'data': {'test_id': 12345}
        }

        future = producer.send(topic, value=message)
        record_metadata = future.get(timeout=10)

        print(f'Message sent successfully!')
        print(f'Topic: {record_metadata.topic}')
        print(f'Partition: {record_metadata.partition}')
        print(f'Offset: {record_metadata.offset}')

        # Wait briefly to allow message to be consumed
        time.sleep(1)

        # Poll for the message
        msg_count = 0
        for msg in consumer:
            print(f'Received message: {msg.value}')
            msg_count += 1
            if msg_count >= 1:
                break

        producer.close()
        consumer.close()

        print('Connectivity test completed successfully!')

    except Exception as e:
        print(f'Error connecting to Kafka: {str(e)}')
        raise

if __name__ == '__main__':
    test_kafka_connectivity()