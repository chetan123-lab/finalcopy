import pulumi
import json
import pulumi_aws as aws

config = pulumi.Config()

cpu=config.require("cpu")
memory=config.require("memory")
desired_count=config.require_int("desired_count")
container_port=config.require_int("container_port")
container_image=config.require("container_image")

def create_ecs_resources_wrapper(ecs_task_execution_role, ecs_task_role, fargate_security_group, private_subnet, target_group):
    return create_ecs_resources(ecs_task_execution_role, ecs_task_role, fargate_security_group, private_subnet, target_group, cpu, memory, desired_count, container_port, container_image)

def create_ecs_resources(ecs_task_execution_role, ecs_task_role, fargate_security_group, private_subnet, target_group, cpu, memory, desired_count, container_port, container_image):
    # Create an ECS Cluster
    ecs_cluster = aws.ecs.Cluster("ecs-cluster",
        name="my-ecs-cluster",
    )

    # Create an ECS Task Definition
    task_definition = aws.ecs.TaskDefinition("task-definition",
        family="my-task-definition",
        cpu=cpu,
        memory=memory,
        network_mode="awsvpc",
        requires_compatibilities=["FARGATE"],
        execution_role_arn=ecs_task_execution_role.arn,
        task_role_arn=ecs_task_role.arn,
        container_definitions=pulumi.Output.all().apply(lambda args: json.dumps([
            {
                "name": "kyruushealth",
                "image": container_image,
                "portMappings": [
                    {
                        "containerPort": container_port,
                        "hostPort": container_port,
                        "protocol": "tcp",
                    },
                ],
            },
        ])),
    )

    # Create an ECS Service
    ecs_service = aws.ecs.Service("ecs-service",
        name="my-ecs-service",
        cluster=ecs_cluster.arn,
        task_definition=task_definition.arn,
        launch_type="FARGATE",
        network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
            security_groups=[fargate_security_group.id],
            subnets=[private_subnet.id],
            assign_public_ip=False,
        ),
        load_balancers=[
            aws.ecs.ServiceLoadBalancerArgs(
                target_group_arn=target_group.arn,
                container_name="kyruushealth",
                container_port=container_port,
            ),
        ],
        desired_count=desired_count,
    )

    return {
        "ecs_cluster": ecs_cluster,
        "task_definition": task_definition,
        "ecs_service": ecs_service,
    }

