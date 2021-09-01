import boto3
import uuid
import logging

client = boto3.client('docdb')

class DocumentDB:
  """
  Add or remove read replicas on an Amazon DocumentDB cluster.

  Attributes
  ----------
  db_cluster_id : str
    DocumentDB cluster identifier.
  min_capacity : int
    The minimum capacity (default is 0).
  max_capacity : int
    The maximum capacity (default is 15).

  Methods
  -------
  is_modifying()
    Check if some instance in the cluster is not "available".
  get_replicas_count()
    Get how many replicas there are in the cluster.
  get_primary_instance_class()
    Get the class of the primary instance (writer).
  add_replica()
    Add one read replica.
  remove_replica()
    Remove one read replica.
  """
  def __init__(self, db_cluster_id, min_capacity=0, max_capacity=15):
    """
    Parameters
    ----------
    db_cluster_id : str
      DocumentDB cluster identifier.
    min_capacity : int
      The minimum capacity (default is 0).
    max_capacity : int
      The maximum capacity (default is 15).
    """
    self.db_cluster_id = db_cluster_id
    self.min_capacity = min_capacity
    self.max_capacity = max_capacity

    # Needed to know what is the 'primary instance'
    self.db_clusters = client.describe_db_clusters(DBClusterIdentifier=db_cluster_id)

    # Needed to know the instance class
    self.db_instances = client.describe_db_instances(
      Filters=[{
        'Name': 'db-cluster-id',
        'Values': [ db_cluster_id ]
      }]
    )

  def is_modifying(self):
    """
    Check if some instance in the cluster is not "available".

    Returns
    -------
    bool
      Returns False if the status all instance is "available" else returns True.
    """
    db_instances = self.db_instances.get('DBInstances')
    for db_instance in db_instances:
      if db_instance.get('DBInstanceStatus') != 'available':
        return True

    return False

  def get_replicas_count(self):
    """
    Get how many replicas there are in the cluster.

    Returns
    -------
    int
      Replicas count.
    """
    db_instances = self.db_instances.get('DBInstances')
    return len(db_instances[1:])
  
  def get_primary_instance_class(self):
    """
    Get the class of the primary instance (writer).
    
    Returns
    -------
    str
      Class of the primary instance, if not found will returns "db.r5.large".
    """
    db_cluster_members = self.db_clusters.get('DBClusters')[0].get('DBClusterMembers')
    db_instances = self.db_instances.get('DBInstances')

    for cluster_member in db_cluster_members:
      is_cluster_writer = cluster_member.get('IsClusterWriter')
      if is_cluster_writer:
        for db_instance in db_instances:
          if cluster_member.get('DBInstanceIdentifier') == db_instance.get('DBInstanceIdentifier'):
            return db_instance.get('DBInstanceClass')
    
    # In theory this block never can be executed
    return 'db.r5.large'

  def add_replica(self, ignore_status=False):
    """
    Add one read replica.

    Parameters
    ----------
    ignore_status : bool
      Ignore the cluster status.
    """
    replicas_count = self.get_replicas_count()

    if replicas_count >= self.max_capacity:
      logging.error("Maximum capacity reached.")
      return None

    if not ignore_status and self.is_modifying():
      logging.error("Is modifying.")
      return None

    return client.create_db_instance(
      DBClusterIdentifier=self.db_cluster_id,
      DBInstanceIdentifier="%s-%s" % (self.db_cluster_id, uuid.uuid4().hex[0:8]),
      DBInstanceClass=self.get_primary_instance_class(),
      Engine="docdb",
    )

  def remove_replica(self, ignore_status=False):
    """
    Remove one read replica.

    Parameters
    ----------
    ignore_status : bool
      Ignore the cluster status.
    """
    replicas_count = self.get_replicas_count()
    
    if replicas_count <= self.min_capacity:
      logging.error('Minimum capacity reached.')
      return None
    
    if not ignore_status and self.is_modifying():
      logging.error("Is modifying.")
      return None

    db_cluster_members = self.db_clusters.get('DBClusters')[0].get('DBClusterMembers')

    for cluster_member in db_cluster_members:
      # Remove the first replica instance found
      if not cluster_member.get('IsClusterWriter'):
        return client.delete_db_instance(
          DBInstanceIdentifier=cluster_member.get('DBInstanceIdentifier')
        )