import paramiko

class BuckeTracker():

    bkt = ""
    client = ""

    def storeBucketLevel(self, config_command: str):
        bucket = config_command.removeprefix("config ").removeprefix("edit ")
        
        self.bkt = bucket
    
    def show_or_get(self, command):
        stdin, stdout, stderr = self.client.exec_command(f"{command} {self.bkt}")

        print(f"\n{stdout.read().decode()}", end="")

        stdin, stdout, stderr = self.client.exec_command(f"config {self.bkt}")

        return stdin, stdout, stderr

    def __init__(self, ssh_client: paramiko.SSHClient):

        self.client = ssh_client
        self.bkt = ""  