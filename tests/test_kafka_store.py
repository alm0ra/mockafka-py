from unittest import TestCase

from parameterized import parameterized

from mockafka.kafka_store import KafkaStore, KafkaException, Message


class TestKafkaStore(TestCase):
    TEST_TOPIC = 'test_topic'
    DEFAULT_PARTITION = 16
    DEFAULT_MESSAGE = Message(
        headers=None,
        key='test_key',
        value='{"test_value": "ok"}',
        topic=TEST_TOPIC,
        offset=None,
        error=None,
        latency=None,
        leader_epoch=None,
        partition=0,
        timestamp=None,
    )

    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)

    def _create_topic_partition(self):
        self.kafka.create_partition(topic=self.TEST_TOPIC, partitions=self.DEFAULT_PARTITION)

    def test_is_topic_exist(self):
        # check topic not exist
        self.assertFalse(self.kafka.is_topic_exist(topic=self.TEST_TOPIC))

        self.kafka.create_topic(topic=self.TEST_TOPIC)

        # check topic exist
        self.assertTrue(self.kafka.is_topic_exist(self.TEST_TOPIC))

    def test_is_partition_exist_on_topic(self):
        # create topic and partition
        self._create_topic_partition()

        # test partition exist
        self.assertTrue(self.kafka.is_partition_exist_on_topic(topic=self.TEST_TOPIC, partition_num=11))
        self.assertTrue(self.kafka.is_partition_exist_on_topic(topic=self.TEST_TOPIC, partition_num=0))
        self.assertTrue(self.kafka.is_partition_exist_on_topic(topic=self.TEST_TOPIC, partition_num=15))

        # test partition not exist
        self.assertFalse(self.kafka.is_partition_exist_on_topic(topic=self.TEST_TOPIC, partition_num=16))

    def test_get_number_of_partition(self):
        self._create_topic_partition()

        self.assertEqual(self.kafka.get_number_of_partition(topic=self.TEST_TOPIC), self.DEFAULT_PARTITION)

    def test_create_topic(self):
        self.kafka.create_topic(topic=self.TEST_TOPIC)

        self.assertTrue(self.kafka.is_topic_exist(self.TEST_TOPIC))

    def test_create_topic_that_exist(self):
        self.kafka.create_topic(topic=self.TEST_TOPIC)

        # test exception when topic exist
        with self.assertRaises(KafkaException):
            self.kafka.create_topic(topic=self.TEST_TOPIC)

    def test_remove_topic(self):
        # test partition not exist
        self.kafka.remove_topic(topic=self.TEST_TOPIC)

        # create topic
        self._create_topic_partition()
        self.kafka.remove_topic(topic=self.TEST_TOPIC)

        self.assertFalse(self.kafka.is_topic_exist(topic=self.TEST_TOPIC))

    def test_produce(self):
        self._create_topic_partition()

        self.assertEqual(
            self.kafka.get_messages_in_partition(topic=self.TEST_TOPIC, partition=0), []
        )

        # test produce on partition 0
        self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=0)

        self.assertEqual(
            self.kafka.get_messages_in_partition(topic=self.TEST_TOPIC, partition=0), [self.DEFAULT_MESSAGE]
        )

        # test produce on partition 1
        self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=1)
        self.assertEqual(
            self.kafka.get_messages_in_partition(topic=self.TEST_TOPIC, partition=1), [self.DEFAULT_MESSAGE]
        )

    def test_get_message(self):
        self._create_topic_partition()

        self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=1)
        self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=1)
        self.assertEqual(
            self.kafka.get_message(topic=self.TEST_TOPIC, partition=1, offset=0), self.DEFAULT_MESSAGE
        )
        self.assertEqual(
            self.kafka.get_message(topic=self.TEST_TOPIC, partition=1, offset=1), self.DEFAULT_MESSAGE
        )

    @parameterized.expand(range(10, 20))
    def test_get_messages_in_partition(self, count):
        self._create_topic_partition()
        for i in range(count):
            self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=1)

        self.assertEqual(len(self.kafka.get_messages_in_partition(topic=self.TEST_TOPIC, partition=1)), count)

    def test_topic_list(self):
        # test empty topic
        self.assertEqual(self.kafka.topic_list(), [])

        topics_to_add = [self.TEST_TOPIC, self.TEST_TOPIC + '01', self.TEST_TOPIC + '02']
        for topic in topics_to_add:
            self.kafka.create_topic(topic=topic)

        self.assertEqual(self.kafka.topic_list(), topics_to_add)

    def test_partition_list(self):
        self._create_topic_partition()

        self.assertEqual(self.kafka.partition_list(topic=self.TEST_TOPIC), list(range(0, self.DEFAULT_PARTITION)))

        self.kafka.create_partition(topic=self.TEST_TOPIC, partitions=self.DEFAULT_PARTITION + 16)
        self.assertEqual(self.kafka.partition_list(topic=self.TEST_TOPIC), list(range(0, self.DEFAULT_PARTITION + 16)))

    def test_number_of_message_in_topic(self):
        self._create_topic_partition()
        for i in range(10):
            self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=1)
            self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=0)
            self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=10)

        self.assertEqual(
            self.kafka.number_of_message_in_topic(topic=self.TEST_TOPIC), 30
        )

    def test_clear_topic_messages(self):
        self._create_topic_partition()
        for i in range(10):
            self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=1)

        # before clearing
        self.assertEqual(
            self.kafka.number_of_message_in_topic(topic=self.TEST_TOPIC), 10
        )

        self.kafka.clear_topic_messages(topic=self.TEST_TOPIC)

        # after clearing
        self.assertEqual(
            self.kafka.number_of_message_in_topic(topic=self.TEST_TOPIC), 0
        )

    def test_clear_partition_messages(self):
        self._create_topic_partition()
        for i in range(10):
            self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=1)
            self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=0)

        # before clearing
        self.assertEqual(
            self.kafka.number_of_message_in_topic(topic=self.TEST_TOPIC), 20
        )

        self.kafka.clear_partition_messages(topic=self.TEST_TOPIC, partition=0)

        # after clearing
        self.assertEqual(
            self.kafka.number_of_message_in_topic(topic=self.TEST_TOPIC), 10
        )

    def test_fresh(self):
        self._create_topic_partition()

        for i in range(self.DEFAULT_PARTITION):
            self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=i)

        # before clearing
        self.assertEqual(
            self.kafka.number_of_message_in_topic(topic=self.TEST_TOPIC), 16
        )

        self.kafka.fresh()

        # after clearing
        self.assertFalse(self.kafka.is_topic_exist(topic=self.TEST_TOPIC))

    def test_set_first_offset(self):
        self._create_topic_partition()

        self.assertEqual(
            self.kafka.get_partition_next_offset(topic=self.TEST_TOPIC, partition=0), 0
        )

        for i in range(self.DEFAULT_PARTITION):
            self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=0)

        self.assertEqual(
            self.kafka.get_partition_next_offset(topic=self.TEST_TOPIC, partition=0), 16
        )

        self.kafka.set_first_offset(topic=self.TEST_TOPIC, partition=0, value=1)
        self.assertEqual(
            self.kafka.get_partition_first_offset(topic=self.TEST_TOPIC, partition=0), 1
        )

        self.kafka.set_first_offset(topic=self.TEST_TOPIC, partition=0, value=10)
        self.assertEqual(
            self.kafka.get_partition_first_offset(topic=self.TEST_TOPIC, partition=0), 10
        )

        self.kafka.set_first_offset(topic=self.TEST_TOPIC, partition=0, value=100)
        self.assertEqual(
            self.kafka.get_partition_first_offset(topic=self.TEST_TOPIC, partition=0), 10
        )

        self.kafka.set_first_offset(topic=self.TEST_TOPIC, partition=0, value=8)
        self.assertEqual(
            self.kafka.get_partition_next_offset(topic=self.TEST_TOPIC, partition=0), 16
        )

    def test_reset_offset(self):
        self._create_topic_partition()

        for i in range(16):
            self.kafka.produce(message=self.DEFAULT_MESSAGE, topic=self.TEST_TOPIC, partition=0)

        self.kafka.set_first_offset(topic=self.TEST_TOPIC, partition=0, value=10)
        self.assertEqual(
            self.kafka.get_partition_first_offset(topic=self.TEST_TOPIC, partition=0), 10
        )

        # reset offset to latest
        self.kafka.reset_offset(topic=self.TEST_TOPIC, strategy='latest')
        self.assertEqual(
            self.kafka.get_partition_first_offset(topic=self.TEST_TOPIC, partition=0), 16
        )

        # reset offset to earliest
        self.kafka.reset_offset(topic=self.TEST_TOPIC, strategy='earliest')
        self.assertEqual(
            self.kafka.get_partition_first_offset(topic=self.TEST_TOPIC, partition=0), 0
        )
