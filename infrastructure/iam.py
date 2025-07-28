import pulumi
import pulumi_aws as aws
import json

def create_iam_roles():
    # IAM Role for the ECS Task
    ecs_task_role = aws.iam.Role("ecs-task-role",
        assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ecs-tasks.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }),
    )

    # IAM Role for the ECS Task Execution
    ecs_task_execution_role = aws.iam.Role("ecs-task-execution-role",
        assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ecs-tasks.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }),
    )

 
    # Load configuration
    config=pulumi.Config()
    ecr_actions=config.require_object("ecr_actions")
    logs_actions=config.require_object("logs_actions")
    policy_resources=config.require("policy_resources")

    # the ECS task execution role
    ecs_task_execution_policy = aws.iam.Policy("ecs-task-execution-policy",
        policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Action": ecr_actions + logs_actions,
                    "Resource": policy_resources
                }
            ]
        }),
    )

    # ECS task execution role
    aws.iam.RolePolicyAttachment("ecs-task-execution-policy-attachment",
        role=ecs_task_execution_role.name,
        policy_arn=ecs_task_execution_policy.arn,
    )

    return {
        "ecs_task_role": ecs_task_role,
        "ecs_task_execution_role": ecs_task_execution_role,
    }