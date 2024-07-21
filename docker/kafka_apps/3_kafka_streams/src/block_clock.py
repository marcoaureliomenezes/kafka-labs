import faust
import random
import os
import json

from utils.fake_generator import FakeGenerator


KAFKA_BROKERS = os.getenv('KAFKA_BROKERS')
KAFKA_TOPIC_1 = os.getenv('KAFKA_TOPIC_1')
KAFKA_TOPIC_2 = os.getenv('KAFKA_TOPIC_2')
APP_NAME = "Block_Clock_App"

print(f'KAFKA_BROKERS: {KAFKA_BROKERS}')
brokers = KAFKA_BROKERS.split(',')


app = faust.App(APP_NAME,broker=f'kafka://{brokers[0]}')

block_metadata_topic = app.topic(KAFKA_TOPIC_1, value_type=str, value_serializer='raw')
block_txs_hash_ids_topic = app.topic(KAFKA_TOPIC_2, value_type=str, value_serializer='raw')

@app.timer(interval=5)
async def block_clock():
  block_data = FakeGenerator().fake_block()
  print(f'Block: {block_data}')
  encoded_block_data = json.dumps(block_data).encode('utf-8')
  await block_metadata_topic.send(value=encoded_block_data)
  _ = [await block_txs_hash_ids_topic.send(value=tx) for tx in block_data['txs']]


@app.agent(block_txs_hash_ids_topic)
async def process_block_txs_hash_ids(stream):
  async for hash_ids in stream:
    print(f'Hash IDs: {hash_ids}')


