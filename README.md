# docdb-autoscaling

An auto-scaling solution for Amazon DocumentDB.

This project is an [AWS Lambda](https://aws.amazon.com/lambda/) written in Python and deployed with [Terraform](https://www.terraform.io/) that easily implements auto-scaling functionality for [Amazon DocumentDB](https://aws.amazon.com/documentdb/).

## Why?

Amazon DocumentDB (with MongoDB compatibility) supports [up to 15 read replicas](https://docs.aws.amazon.com/documentdb/latest/developerguide/replication.html), but by default AWS does not provide an easy way to set up an auto-scaling policy for them.

## The Solution

Follow below how the system works:

![Architecture diagram](./assets/diagram.png)

Resources created by Terraform:

- **[CloudWatch](https://aws.amazon.com/cloudwatch/) alarm** ─ will watch a CloudWatch metric from the Document Database cluster (e.g. `CPUUtilization`).
- **[Simple Notification Service (SNS)](https://aws.amazon.com/sns/)** ─ will be triggered by CloudWatch when any metrics are matched.
- **[AWS Lambda](https://aws.amazon.com/lambda/)** ─ will be triggered by the SNS and will be responsible for adding or removing read replicas in the Document Database cluster.

## Terraform module

You can deploy the function with Terraform using the following syntax:

```terraform
module "docdb-autoscaling-prod" {
  source             = "github.com/theuves/docdb-autoscaling"
  cluster_identifier = "my-prod-cluster"
  name               = "docdb-autoscaling-prod"
  min_capacity       = 3
  max_capacity       = 6

  scaling_policy = [
    {
      metric_name = "CPUUtilization"
      target      = 80
      statistic   = "Average"
      cooldown    = 300
    }
  ]
}
```

## Deployment

To create the resources:

```bash
terraform init
terraform plan
terraform apply
```

To destroy:

```bash
terraform destroy
```

## Input variables

| Variable | Description | Type | Default value |
|:---|:---|:---|:---|
| `cluster_identifier` | DocumentDB cluster identifier. | `string` | n/a |
| `name` | Resources name. | `string` | `"docdb-autoscaling"` |
| `min_capacity` | The minimum capacity. | `number` | `0` |
| `max_capacity` | The maximum capacity. | `number` | `15` |
| `scaling_policy` | The auto-scaling policy. | [see here](/#hello) | [see here](/#hello) |

### `scaling_policy`

Type:

```terraform
list(object({
  metric_name = string
  target      = number
  statistic   = string
  cooldown    = number
}))
```

Default value:

```terraform
[
  {
    metric_name = "CPUUtilization"
    target      = 60
    statistic   = "Average"
    cooldown    = 120
  }
]
```

Options:

- `metric_name` ─ Amazon DocumentDB metric name ([see the list](https://docs.aws.amazon.com/documentdb/latest/developerguide/cloud_watch.html)).
- `target` ─ The value against which the specified statistic is compared.
- `statistic` ─ The statistic to apply to the alarm's associated metric (supported values: `SampleCount`, `Average`, `Sum`, `Minimum`, `Maximum`). 
- `cooldown` ─ The cooldown period between scaling actions.

## Output values

n/a

## License

MIT