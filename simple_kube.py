#!/usr/bin/python
import os
import sys
import subprocess


class Common():

    def __init__(self):
        self.system_os = "linux"
    def DoError (self,Error) :
        sys.exit(Error)
    def execute_commands(self, execute_local_command):
        try:
            process = subprocess.Popen(execute_local_command, shell=True, stdout=subprocess.PIPE)
            out, err = process.communicate()
            print(out.decode())
        except Exception as e:
            print(str(e))

class InstallMicrok8s():

    def __init__(self):
        self.system_os = "linux"
        self.common_obj = Common()

    def execute_installation_command(self):
        try:
            if self.system_os == "mac":
                self.common_obj.execute_commands("brew install mulitpass")
                self.common_obj.execute_commands("multipass launch --name microk8s-vm --mem 4G --disk 40G")
                self.common_obj.execute_commands("multipass exec microk8s-vm -- sudo snap install microk8s --classic")
                self.common_obj.execute_commands("multipass exec microk8s-vm -- sudo iptables -P FORWARD ACCEPT")
                self.common_obj.execute_commands("multipass exec microk8s-vm -- /snap/bin/microk8s.status")
                self.common_obj.execute_commands("multipass exec microk8s-vm -- /snap/bin/microk8s.config > kubeconfig")
                self.common_obj.execute_commands("kubectl --kubeconfig=kubeconfig get all --all-namespaces")
                self.common_obj.execute_commands("multipass exec microk8s-vm -- /snap/bin/microk8s.enable dns dashboard registry")
            elif self.system_os == "linux":
                self.common_obj.execute_commands("snap install microk8s --classic")
                self.common_obj.execute_commands("export PATH=$PATH:/snap/bin")
                self.common_obj.execute_commands("microk8s.enable dns dashboard registry")
        except Exception as e:
            print(str(e))

    def status_microk8s(self):
        try:
            if self.system_os == "mac":
                self.common_obj.execute_commands("multipass exec microk8s-vm -- /snap/bin/microk8s.status")
            elif self.system_os == "linux":
                self.common_obj.execute_commands("microk8s.status")
        except Exception as e:
            print(str(e))

    def stop_microk8s(self):
        try:
            if self.system_os == "mac":
                self.common_obj.execute_commands("multipass exec microk8s-vm -- /snap/bin/microk8s.stop")
            elif self.system_os == "linux":
                self.common_obj.execute_commands("microk8s.stop")
        except Exception as e:
            print(str(e))

    def start_microk8s(self):
        try:
            if self.system_os == "mac":
                self.common_obj.execute_commands("multipass exec microk8s-vm -- /snap/bin/microk8s.start")
            elif self.system_os == "linux":
                self.common_obj.execute_commands("microk8s.start")
        except Exception as e:
            print(str(e))

    def get_pods_microk8s(self):
        try:
            if self.system_os == "mac":
                self.common_obj.execute_commands("multipass exec microk8s-vm -- /snap/bin/microk8s.kubectl get pods")
            elif self.system_os == "linux":
                self.common_obj.execute_commands("microk8s.kubectl get pods")
        except Exception as e:
            print(str(e))

    def get_deployment_microk8s(self):
        try:
            if self.system_os == "mac":
                self.common_obj.execute_commands("multipass exec microk8s-vm -- /snap/bin/microk8s.kubectl get deployment")
            elif self.system_os == "linux":
                self.common_obj.execute_commands("microk8s.kubectl get deployment")
        except Exception as e:
            print(str(e))

    def create_deployment_microk8s(self,yaml_file):
        try:
            if self.system_os == "mac":
                self.common_obj.execute_commands("multipass exec microk8s-vm -- /snap/bin/microk8s.kubectl create -f " + str(yaml_file))
            elif self.system_os == "linux":
                self.common_obj.execute_commands("microk8s.kubectl create -f " + str(yaml_file))
        except Exception as e:
            print(str(e))


class DockerImage():

    def __init__(self):
        self.system_os = "linux"
        self.common_obj = Common()

    def create_docker_image(self,path_of_docker_file):
        try:
            create_tag = str(path_of_docker_file.split("/")[-1:][0])
            if not create_tag:
                create_tag = str(path_of_docker_file.split("/")[-2:][0])
            self.common_obj.execute_commands("sudo docker build -t " + str(create_tag) + " " + str(path_of_docker_file))
        except Exception as e:
            print(str(e))

    def create_push_docker_image(self,path_of_docker_file):
        try:
            create_tag = str(path_of_docker_file.split("/")[-1:][0])
            if not create_tag:
                create_tag = str(path_of_docker_file.split("/")[-2:][0])
            self.common_obj.execute_commands("sudo docker build -t localhost:32000/" + str(create_tag) + " " + str(path_of_docker_file))
            self.common_obj.execute_commands("sudo docker push localhost:32000/" + str(create_tag))
        except Exception as e:
            print(str(e))

    def status_docker_image(self,docker_image_name):
        try:
            self.common_obj.execute_commands("sudo docker images " + str(docker_image_name))
        except Exception as e:
            print(str(e))

    def remove_docker_image(self,docker_image_name):
        try:
            self.common_obj.execute_commands("sudo docker rmi " + str(docker_image_name))
        except Exception as e:
            print(str(e))


    def list_docker_image(self):
        try:
            self.common_obj.execute_commands("sudo docker images")
        except Exception as e:
            print(str(e))


    def create_push_deployment(self,image_name):
        try:
            if self.system_os == "mac":
                self.common_obj.execute_commands("multipass exec microk8s-vm -- /snap/bin/microk8s.kubectl create -f " + str(yaml_file))
            elif self.system_os == "linux":
                self.common_obj.execute_commands("sudo docker build -t localhost:32000/" + str(image_name) + " . ")
                self.common_obj.execute_commands("sudo docker push localhost:32000/" + str(image_name))
                pod_name = self.common_obj.execute_commands("sudo microk8s.kubectl get pods | grep " + str(image_name) + " | awk '{print $1}'")
                self.common_obj.execute_commands("sudo microk8s.kubectl delete pods " + str(pod_name).strip())
        except Exception as e:
            print(str(e))


def main():
    common_obj = Common()
    try:
        if len(sys.argv) == 3:
            user_input = sys.argv[1] # --start --stop
            user_input_command = sys.argv[2] # kube
        else:
            print("Please execute as below ")
            print("Ex: ./simple_kube.py --status kube")
            print("                     --start kube")
            print("                     --stop kube")
            print("                     --install kube")
            print("                     --list-pods kube")
            print("                     --list-deployment kube")
            print("                     --create-deployment /tmp/test.yaml")
            print("                     --create-docker <Docker_file_path>")
            print("                     --create-push-docker <Docker_file_path>")
            print("                     --status-docker-image imagename")
            print("                     --remove-docker-image imagename")
            print("                     --docker-image list")
            print("                     --create-push-deploy imagename")
            sys.exit(1)
    except Exception as exc:
        print("Please execute as below ")
        print("Ex: ./simple_kube.py --status kube")
        sys.exit(1)

    try:
        if user_input_command and user_input_command == "kube":
            obj = InstallMicrok8s()
            # Below is for microk8s status, start, stop and installation
            if user_input == "--status":
                obj.status_microk8s()
            if user_input == "--start":
                obj.start_microk8s()
            if user_input == "--stop":
                obj.stop_microk8s()
            if user_input == "--install":
                obj.execute_installation_command()
            if user_input == "--list-pods":
                obj.get_pods_microk8s()
            if user_input == "--list-deployment":
                obj.get_deployment_microk8s()
            if user_input == "--create-deployment":
                obj.create_deployment_microk8s()
    except Exception as e:
        print(str(e))

    try:
        # Below is for create of docker images locally
        if "docker" in user_input or "deploy" in user_input:
            obj = DockerImage()
            if user_input == "--create-docker":
                # ex: sudo docker build -t mongodb_docker ./atlan/mongodb_docker
                obj.create_docker_image(user_input_command)
            if user_input == "--create-push-docker":
                # ex: sudo docker build -t mongodb_docker ./atlan/mongodb_docker
                obj.create_push_docker_image(user_input_command)
            if user_input == "--status-docker-image":
                obj.status_docker_image(user_input_command)
            if user_input == "--remove-docker-image":
                obj.remove_docker_image(user_input_command)
            if user_input == "--docker-image":
                if user_input_command == "list":
                    obj.list_docker_image()
            if user_input == "--create-push-deploy":
                if user_input_command:
                    obj.create_push_deployment(user_input_command)

    except Exception as e:
        common_obj.DoError(str(e))


if __name__ == "__main__":
    main()
