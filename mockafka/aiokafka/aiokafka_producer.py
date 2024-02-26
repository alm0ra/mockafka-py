class FakeAIOKafkaProducer:
    def __init__(self):
        pass

    async def start(self):
        pass

    async def flush(self):
        pass

    async def stop(self):
        pass

    async def send(self):
        pass

    async def send_and_wait(self):
        pass

    async def create_batch(self):
        pass

    async def send_batch(self):
        pass

    async def begin_transaction(self):
        pass

    async def commit_transaction(self):
        pass

    async def abort_transaction(self):
        pass

    def transaction(self):
        pass

    async def send_offsets_to_transaction(self, offsets, group_id):
        pass


