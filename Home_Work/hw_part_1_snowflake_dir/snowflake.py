import time

from constants import (EPOCH_MS_DEFAULT, NODE_ID_DEFAULT, NODE_ID_MAX, NODE_ID_SHIFT, SEQUENCE_ID_MAX, TIMESTAMP_MS_MAX, TIMESTAMP_SHIFT)
def read_current_millis(epoch_ms:int) -> int:
    now_ms = int(time.time() * 1000)
    return now_ms - epoch_ms

def decode_timestamp_ms(snowflake_id: int,epoch_ms: int = EPOCH_MS_DEFAULT) -> int:
    timestamp = snowflake_id >> TIMESTAMP_SHIFT
    timestamp = timestamp & TIMESTAMP_MS_MAX
    return timestamp + epoch_ms

def decode_node_id(snowflake_id: int) -> int:
    node_id = snowflake_id >> NODE_ID_SHIFT
    node_id = node_id & NODE_ID_MAX
    return node_id



def decode_sequence_id(snowflake_id: int) -> int:
    return snowflake_id & SEQUENCE_ID_MAX

def generate_snowflake_id(sequence_id: int, node_id: int =NODE_ID_DEFAULT, epoch_ms: int =EPOCH_MS_DEFAULT) -> int | None:
    if node_id < 0 or node_id > NODE_ID_MAX:
        print("node_id must be in [0, ", NODE_ID_MAX, "], got", node_id)
        return None

    if sequence_id < 0 or sequence_id > SEQUENCE_ID_MAX:
        print("sequence_id must be in [0,", SEQUENCE_ID_MAX, "], got ", sequence_id)
        return None
    timestamp = read_current_millis(epoch_ms)

    if timestamp > TIMESTAMP_MS_MAX:
        print("timestamp overflows:", timestamp, "> ", TIMESTAMP_MS_MAX)
        return None

    timestamp_part = timestamp << TIMESTAMP_SHIFT
    node_part = node_id << NODE_ID_SHIFT
    result = timestamp_part | node_part | sequence_id


    return result