import os
import json
import autoscaling

# Environment variables
min_capacity = int(os.environ.get("min_capacity"))
max_capacity = int(os.environ.get("max_capacity"))
cluster_identifier = os.environ.get("cluster_identifier")

def handler(event, context):
  sns_message = event.get('Records')[0].get('Sns').get('Message')
  new_state_value = json.loads(sns_message).get('NewStateValue')

  if min_capacity > max_capacity:
    print("min_capacity cannot be greater than max_capacity")
    return

  docdb = autoscaling.DocumentDB(cluster_identifier, min_capacity, max_capacity)

  if new_state_value == "ALARM":
    docdb.add_replica()
    print("Adding replica...")
  if new_state_value == "OK":
    docdb.remove_replica()
    print("Removing replica...")
