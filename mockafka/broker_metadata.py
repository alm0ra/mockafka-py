from __future__ import annotations


class BrokerMetadata(object):
    """
    Provides information about a Kafka broker.

    This class is typically not user instantiated.
    """

    def __init__(self):
        self.id = 1
        """Broker id"""
        self.host = "fakebroker"
        """Broker hostname"""
        self.port = 9091
        """Broker port"""

    def __repr__(self):
        return "BrokerMetadata({}, {}:{})".format(self.id, self.host, self.port)

    def __str__(self):
        return "{}:{}/{}".format(self.host, self.port, self.id)
