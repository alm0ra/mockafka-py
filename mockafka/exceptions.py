try:
    from confluent_kafka import (  # type: ignore[import-untyped]
        KafkaError,
        KafkaException,
    )
except ImportError:
    # Arguably not an exception, but essentially fits here.
    class KafkaError:  # type: ignore[no-redef]
        pass

    class KafkaException(Exception):  # type: ignore[no-redef]
        pass
