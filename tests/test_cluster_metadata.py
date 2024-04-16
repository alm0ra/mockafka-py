from mockafka.admin_client import FakeAdminClientImpl, NewTopic
from mockafka.broker_metadata import BrokerMetadata
from mockafka.cluster_metadata import ClusterMetadata


def test_cluster_metadata():
    # topic does not exist
    metadata = ClusterMetadata(topic="test")
    assert metadata.cluster_id == "test"

    # topic exists
    FakeAdminClientImpl().create_topic(topic=NewTopic(topic="test1", num_partitions=1))
    ClusterMetadata(topic="test")


def test_broker_metadata():
    broker = BrokerMetadata()
    assert str(broker) == f"{broker.host}:{broker.port}/{broker.id}"
