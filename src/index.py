import os
import boto3
import uuid

client = boto3.client('docdb')

min_capacity = os.environ.get("min_capacity")
max_capacity = os.environ.get("max_capacity")

if min_capacity > max_capacity:
  print("min_capacity cannot be greater than max_capacity")
  exit()

class DocumentDB:
  def __init__(self, db_cluster_id):
    self.db_cluster_id = db_cluster_id

    # needed to know what is the 'primary instance'
    self.db_clusters = client.describe_db_clusters(DBClusterIdentifier=db_cluster_id)

    # needed to know the instance class
    self.db_instances = client.describe_db_instances(
      Filters=[{
        'Name': 'db-cluster-id',
        'Values': [ db_cluster_id ]
      }]
    )

  def is_modifying(self):
    db_instances = self.db_instances.get('DBInstances')
    for db_instance in db_instances:
      if db_instance.get('DBInstanceStatus') != 'available':
        return True

    return False

  def get_replicas_count(self):
    db_instances = self.db_instances.get('DBInstances')
    return len(db_instances[1:])
  
  def get_primary_instance_class(self):
    db_cluster_members = self.db_clusters.get('DBClusters')[0].get('DBClusterMembers')
    db_instances = self.db_instances.get('DBInstances')

    for cluster_member in db_cluster_members:
      is_cluster_writer = cluster_member.get('IsClusterWriter')
      if is_cluster_writer:
        for db_instance in db_instances:
          if cluster_member.get('DBInstanceIdentifier') == db_instance.get('DBInstanceIdentifier'):
            return db_instance.get('DBInstanceClass')
    
    # in theory this block never can be executed
    return 'db.r5.large'

  def add_replica(self):
    replicas_count = self.get_replicas_count()

    if replicas_count >= max_capacity:
      print("maximum capacity reached")
      return None

    if self.is_modifying():
      print("is modifying")
      return None

    return client.create_db_instance(
      DBClusterIdentifier=self.db_cluster_id,
      DBInstanceIdentifier="%s-%s" % (self.db_cluster_id, uuid.uuid4().hex[0:8]),
      DBInstanceClass=self.get_primary_instance_class(),
      Engine="docdb",
    )

  def remove_replica(self):
    replicas_count = self.get_replicas_count()
    
    if replicas_count <= min_capacity:
      print('minimum capacity reached')
      return None
    
    if self.is_modifying():
      print("is modifying")
      return None

    db_cluster_members = self.db_clusters.get('DBClusters')[0].get('DBClusterMembers')

    for cluster_member in db_cluster_members:
      # remove the first replica instance found
      if not cluster_member.get('IsClusterWriter'):
        return client.delete_db_instance(
          DBInstanceIdentifier=cluster_member.get('DBInstanceIdentifier')
        )
