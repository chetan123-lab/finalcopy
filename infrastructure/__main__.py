import pulumi
from vpc import create_vpc
from security_groups import create_security_groups
from iam import create_iam_roles
from alb import create_alb_wrapper
from ecs import create_ecs_resources_wrapper

vpc_resources = create_vpc()
security_groups = create_security_groups(vpc_resources["vpc"])
iam_roles = create_iam_roles()
alb_resources = create_alb_wrapper(vpc_resources, security_groups["alb_security_group"])
ecs_resources = create_ecs_resources_wrapper(
    iam_roles["ecs_task_execution_role"],
    iam_roles["ecs_task_role"],
    security_groups["fargate_security_group"],
    vpc_resources["private_subnet"],
    alb_resources["target_group"],
)

pulumi.export("vpc_id", vpc_resources["vpc"].id)
pulumi.export("public_subnet_a_id", vpc_resources["public_subnet_a"].id)
pulumi.export("public_subnet_b_id", vpc_resources["public_subnet_b"].id)
pulumi.export("alb_security_group_id", security_groups["alb_security_group"].id)
pulumi.export("fargate_security_group_id", security_groups["fargate_security_group"].id)
pulumi.export("ecs_task_role_arn", iam_roles["ecs_task_role"].arn)
pulumi.export("ecs_task_execution_role_arn", iam_roles["ecs_task_execution_role"].arn)
pulumi.export("alb_dns_name", alb_resources["alb"].dns_name)