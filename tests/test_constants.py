import confluent_kafka  # type: ignore[import-untyped]

from mockafka import constants


def test_constants() -> None:
    print(vars(constants))

    actual = {
        name: value
        for name, value in vars(constants).items()
        if name.isupper()
    }

    expected = {
        name: getattr(confluent_kafka, name)
        for name in actual.keys()
    }

    assert actual == expected
