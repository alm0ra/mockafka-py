__all__ = ["FakeConsumer"]


class FakeConsumer(object):
    """
    A high-level Apache Kafka consumer

    .. py:function:: Consumer(config)

    Create a new Consumer instance using the provided configuration *dict* (including properties and callback functions). See :ref:`pythonclient_configuration` for more information.

    :param dict config: Configuration properties. At a minimum, ``group.id`` **must** be set and ``bootstrap.servers`` **should** be set.
    """

    def assign(self, partitions):
        pass

    def assignment(self, *args, **kwargs):
        return []

    def close(self, *args, **kwargs):
        return None

    def commit(self, message=None, *args, **kwargs):
        return None

    def committed(self, partitions, timeout=None):
        return []

    def consume(self, num_messages=1, *args,
                **kwargs):
        return []

    def consumer_group_metadata(self):
        pass

    def get_watermark_offsets(self, partition, timeout=None, *args,
                              **kwargs):

        return (0, 0)

    def incremental_assign(self, partitions):
        pass

    def incremental_unassign(self, partitions):
        pass

    def list_topics(self, topic=None, *args,
                    **kwargs):
        return ClusterMetadata

    def offsets_for_times(self, partitions, timeout=None):
        return []

    def pause(self, partitions):
        return None

    def poll(self, timeout=None):
        return None

    def position(self, partitions):
        return []

    def resume(self, partitions):
        return None

    def seek(self, partition):
        pass

    def store_offsets(self, message=None, *args,
                      **kwargs):
        return None

    def subscribe(self, topics, on_assign=None, *args,
                  **kwargs):
        pass

    def unassign(self, *args, **kwargs):
        pass

    def unsubscribe(self, *args, **kwargs):
        pass

    def __init__(self, *args, **kwargs):
        pass
