import pulumi
import pulumi_aws as aws

# Load configuration
config = pulumi.Config()

alb_port = config.require_int("alb_port")
target_group_port = config.require_int("target_group_port")

def create_alb_wrapper(vpc, alb_security_group):
    return create_alb(vpc, alb_security_group, alb_port, target_group_port)

def create_alb(vpc, alb_security_group, alb_port, target_group_port):
    # Application Load Balancer
    alb = aws.lb.LoadBalancer("alb",
        subnets=[vpc["public_subnet_a"].id, vpc["public_subnet_b"].id],
        security_groups=[alb_security_group.id],
        tags={
            "Name": "alb",
        },
    )

    # Target Group
    target_group = aws.lb.TargetGroup("target-group",
        port=target_group_port,
        protocol="HTTP",
        target_type="ip",
        vpc_id=vpc["vpc"].id,
        tags={
            "Name": "target-group",
        },
    )

    # Listener
    listener = aws.lb.Listener("listener",
        load_balancer_arn=alb.arn,
        port=alb_port,
        protocol="HTTP",
        default_actions=[
            aws.lb.ListenerDefaultActionArgs(
                target_group_arn=target_group.arn,
                type="forward",
            ),
        ],
    )

    return {
        "alb": alb,
        "target_group": target_group,
        "listener": listener,
    }