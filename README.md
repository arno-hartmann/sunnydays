# sunnydays


## Setting up sunnydays:

To be able to access the Webserver-EC2, make a file called "ssh-key.tf" and enter your ssh-key-values:

```
resource "aws_key_pair" "ssh" {
  key_name      = "$KEYNAME"
  public_key    = "$PUBLIKKEY"
}

output "ssh"{
    value       = aws_key_pair.ssh
}
```

run:<br> 
```sh setup_sunnydays.sh```




