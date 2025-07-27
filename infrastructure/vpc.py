import pulumi
import pulumi_aws as aws

# Load configuration
config = pulumi.Config()

def create_vpc():
    # Create a new VPC
    vpc = aws.ec2.Vpc("my-vpc",
        cidr_block=config.require("vpc_cidr_block"),
        enable_dns_hostnames=True,
        enable_dns_support=True,
        tags={
            "Name": "my-vpc",
        },
    )

    # Create a public subnet
    public_subnet_a = aws.ec2.Subnet("public-subnet-a",
        cidr_block=config.require("public_subnet_a_cidr_block"),
        vpc_id=vpc.id,
        availability_zone=config.require("availability_zone_a"),
        map_public_ip_on_launch=True,
        tags={
            "Name": "public-subnet-a",
        },
    )

    # Create a public subnet
    public_subnet_b = aws.ec2.Subnet("public-subnet-b",
        cidr_block=config.require("public_subnet_b_cidr_block"),
        vpc_id=vpc.id,
        availability_zone=config.require("availability_zone_b"),
        map_public_ip_on_launch=True,
        tags={
            "Name": "public-subnet-b",
        },
    )

    # Create a private subnet
    private_subnet = aws.ec2.Subnet("private-subnet",
        cidr_block=config.require("private_subnet_cidr_block"),
        vpc_id=vpc.id,
        availability_zone=config.require("availability_zone_b"),
        tags={
            "Name": "private-subnet",
        },
    )

    # Create an Internet Gateway
    igw = aws.ec2.InternetGateway("igw",
        vpc_id=vpc.id,
        tags={
            "Name": "igw",
        },
    )

    # Create an Elastic IP address
    eip = aws.ec2.Eip("eip",
        domain="vpc",
    )

    # Create a NAT gateway
    nat_gateway = aws.ec2.NatGateway("nat-gateway",
        subnet_id=public_subnet_a.id,
        allocation_id=eip.id,
    )

    # Create a route table for the private subnet
    private_route_table = aws.ec2.RouteTable("private-route-table",
        vpc_id=vpc.id,
        routes=[
            aws.ec2.RouteTableRouteArgs(
                cidr_block="0.0.0.0/0",
                nat_gateway_id=nat_gateway.id,
            ),
        ],
    )

    # Associate the private subnet with the route table
    aws.ec2.RouteTableAssociation("private-route-table-association",
        subnet_id=private_subnet.id,
        route_table_id=private_route_table.id,
    )

    # Create a Route Table for the public subnet
    public_route_table = aws.ec2.RouteTable("public-route-table",
        vpc_id=vpc.id,
        routes=[
            aws.ec2.RouteTableRouteArgs(
                cidr_block="0.0.0.0/0",
                gateway_id=igw.id,
            ),
        ],
        tags={
            "Name": "public-route-table",
        },
    )

    # Associate the public subnet with the Route Table
    aws.ec2.RouteTableAssociation("public-route-table-association-a",
        subnet_id=public_subnet_a.id,
        route_table_id=public_route_table.id,
    )

    aws.ec2.RouteTableAssociation("public-route-table-association-b",
        subnet_id=public_subnet_b.id,
        route_table_id=public_route_table.id,
    )

    return {
        "vpc": vpc,
        "public_subnet_a": public_subnet_a,
        "public_subnet_b": public_subnet_b,
        "private_subnet": private_subnet,
    }
