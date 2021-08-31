# Scale-out and scale-in alarm
resource "aws_cloudwatch_metric_alarm" "main" {
  count = length(var.scaling_policy)

  alarm_name          = "${var.name}-${count.index}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  namespace           = "AWS/DocDB"
  metric_name         = var.scaling_policy[count.index].metric_name
  statistic           = var.scaling_policy[count.index].statistic
  period              = tostring(var.scaling_policy[count.index].cooldown)
  threshold           = tostring(var.scaling_policy[count.index].target)

  # Actions
  actions_enabled = "true"
  alarm_actions   = [aws_sns_topic.main.arn]
  ok_actions      = [aws_sns_topic.main.arn]

  dimensions = {
    DBClusterIdentifier = var.cluster_identifier
  }
}