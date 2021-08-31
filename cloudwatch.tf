locals {
  comparison_operators = {
    "scale-out" = "GreaterThanThreshold"
    "scale-in"  = "LessThanThreshold"
  }
}

# Scale-out and scale-in alarm
resource "aws_cloudwatch_metric_alarm" "main" {
  count = length(var.scaling_policy)

  alarm_name          = "${var.name}-${count.index}-${var.scaling_policy[count.index].action}"
  comparison_operator = local.comparison_operators[var.scaling_policy[count.index].action]
  evaluation_periods  = "1"
  namespace           = "AWS/DocDB"
  metric_name         = var.scaling_policy[count.index].metric_name
  statistic           = var.scaling_policy[count.index].statistic
  period              = tostring(var.scaling_policy[count.index].cooldown)
  threshold           = tostring(var.scaling_policy[count.index].target)

  dimensions = {
    DBClusterIdentifier = var.cluster_identifier
  }
}