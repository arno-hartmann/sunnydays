resource "aws_vpc" "sunnydays-vpc" {
    cidr_block = "10.10.0.0/16"
    enable_dns_hostnames = true
    tags = {
        Name = "sunnydays-vpc"
    }
}

resource "aws_security_group" "sunnydays-webserver-sg" {
  name = "allow-website-access"
  description = "Open ports for http and ssh connection"
  vpc_id = aws_vpc.sunnydays-vpc.id

  ingress {
      description = "Allow HTTP access"
      from_port = 80
      to_port = 80
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }
    ingress {
      description = "Allow SSH access"
      from_port = 22
      to_port = 22
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
      from_port = 0
      to_port = 0
      protocol = "-1"
      cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_subnet" "sunnydays-private-subnet" {
  vpc_id = aws_vpc.sunnydays-vpc.id
  cidr_block = "10.10.1.0/24"
  availability_zone = "us-west-2b"

  tags = {
      Name = "sunnydays-private-subnet"
  }
}

resource "aws_subnet" "sunnydays-public-subnet" {
  vpc_id = aws_vpc.sunnydays-vpc.id
  cidr_block = "10.10.2.0/24"
  availability_zone = "us-west-2a"

  tags = {
      Name = "sunnydays-public-subnet"
  }
}

resource "aws_db_subnet_group" "sunnydays-subnets" {
  name = "sunnydays-subnets"
  subnet_ids = [aws_subnet.sunnydays-private-subnet.id, aws_subnet.sunnydays-public-subnet.id]
  tags = {
      Name = "sunnydays-subnets"
  }
}


resource "aws_internet_gateway" "sunnydays-gw" {
  vpc_id = aws_vpc.sunnydays-vpc.id
}


resource "aws_instance" "webserver" {
  ami = "ami-02b92c281a4d3dc79"
  instance_type = "t2.micro"
  availability_zone = "us-west-2a"
  key_name = aws_key_pair.ssh.key_name
  security_groups = [aws_security_group.sunnydays-webserver-sg.id]
  subnet_id = aws_subnet.sunnydays-public-subnet.id
  iam_instance_profile = var.instance_profile
  user_data = "${file("modules/tf-user-data.sh")}"
}

resource "aws_eip" "webserver" {
  instance = aws_instance.webserver.id
  vpc      = true
}

resource "aws_route_table" "sunnydays_route_table" {
  vpc_id = aws_vpc.sunnydays-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.sunnydays-gw.id
  }
}

resource "aws_route_table_association" "public_subnet" {
  subnet_id = aws_subnet.sunnydays-public-subnet.id
  route_table_id =aws_route_table.sunnydays_route_table.id  
}

variable "instance_profile" {
  type = string
}