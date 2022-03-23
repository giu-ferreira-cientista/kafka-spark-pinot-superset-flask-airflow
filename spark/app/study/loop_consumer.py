from kafka import KafkaConsumer

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('NOTIFICATION',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'])
#while True:
    # Response format is {TopicPartiton('topic1', 1): [msg1, msg2]}
#msg_pack = consumer.poll(timeout_ms=500)
count = 1
#for message in consumer:
while count <= 10:        
    msg_pack = consumer.poll(timeout_ms=500)

    for tp, messages in msg_pack.items():
        for message in messages:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            print ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
                                                  message.offset, message.key,
                                                  message.value))
    count += 1

consumer.close()                                                