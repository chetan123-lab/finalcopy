# DevOps Exercise Solution

## Overview
This document contains the solution for the technical interview exercise: modernizing an application deployment using AWS, Pulumi, and GitHub Actions.

## Application
The application is a simple Python Flask web service with the following endpoints:
- `GET /`: Returns a success message
- `GET /health`: Returns JSON `{"status": "ok"}`

## Design Choices
1. Containerization
      Containerization provides a lightweight and portable way to deploy applications, ensuring consistency across environments.
      Technology: Docker
2. Orchestration
      Orchestration is necessary to manage the lifecycle of containers, ensuring scalability, reliability, and efficient resource utilization.
      Technology: Amazon ECS with Fargate
3. Task Definition
      Task definitions define the configuration for ECS tasks, specifying container settings, resource requirements, and networking options.
      Configuration: CPU, memory, network mode, and container definitions are specified in the task definition.
## Design Considerations
1. Scalability
    - The application is designed to scale horizontally, with ECS Fargate providing automatic scaling capabilities.
2. High Availability
    - The application is deployed across multiple availability zones, ensuring high availability and fault tolerance.
3. Security
    - The application uses IAM roles for task execution and task roles, ensuring secure access to AWS resources.

### Tools and Resources used
 1.Pulumi,Github Actions,Python

## Trade-offs and Considerations
1. Complexity vs. Simplicity
    - The use of ECS Fargate simplifies the management of containerized applications, but may introduce additional complexity in task definition and configuration.AS this is small application ECS is the best choice.
2. Cost and Performance
    - The choice of CPU and memory resources for ECS tasks balances cost and performance requirements, ensuring efficient resource utilization.

## Production Readiness and Future Improvements
1.I will improve logging system.
2.For scanning the code,I will use veracode scanner for network security check.
3.Strategy to deploy on multiple environments,more refined code we can add.
4.I tried to avoid as much as hardcoded value.In future I will continue it.
5.In github action,I will add destroy phase.Keeping it as manual value.
6.SSL certificates I will like to add.We can add through AWS certificate manager or     OpenSSL tool.
7.If application becomes complex we can consider EKS cluster as option.
8.We can add unit testing phase in CI/CD for example PyTest Phase.
  We can use mock values for creating resources.
9.I add pulumi dependency phase  python -m venv venv,source venv/bin/activate in CI/CD.
  All required dependencies to run pulumi code will get installed. 
10.For selecting already  present stack,I add the command as well as take consideration
of already present ECR repository in CI/CD.
11.Image scanning phase we can include in CI/CD.
12.Destory phase we can add more in structured way.I will Prefer it as manual option.

## Challenges:
1.Initially my ECS tasks were deprovisioning,reason I found out through cloudwatch logs.
But in case of production scenario,I will like to consider options like promethus and grafana.
2.Code modularization will be complex in future as application become complex.





