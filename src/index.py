import os
import json
import logging
import autoscaling

# Environment variables
min_capacity = int(os.environ.get("min_capacity"))
max_capacity = int(os.environ.get("max_capacity"))
cluster_identifier = os.environ.get("cluster_identifier")

def handler(event, context):
  sns_message = event.get('Records')[0].get('Sns').get('Message')
  new_state_value = json.loads(sns_message).get('NewStateValue')

  if min_capacity > max_capacity:
    logging.critical("The 'min_capacity' cannot be greater than 'max_capacity'.")
    return None

  docdb = autoscaling.DocumentDB(cluster_identifier, min_capacity, max_capacity)

  if new_state_value == "ALARM":
    logging.warning("Adding replica...")
    docdb.add_replica()
  if new_state_value == "OK":
    logging.warning("Removing replica...")
    docdb.remove_replica()
