import time
from snowflake import(generate_snowflake_id, decode_node_id,decode_sequence_id, decode_timestamp_ms)

epoch = 1288834974657

s = generate_snowflake_id(sequence_id=42, node_id=7, epoch_ms=epoch)


print("id:", s)
print("node_id:", decode_node_id(s))
print("sequence_id:", decode_sequence_id(s))
print("time:", decode_timestamp_ms(s, epoch))
print("now:", int(time.time() * 1000))