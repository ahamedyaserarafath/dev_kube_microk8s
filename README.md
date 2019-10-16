# Kubernetes - Python - Microk8s
# Deploying the Kubernetes(Microk8s) in linux(ubuntu - 18.04) machine for the use of in house development. 
- [Introduction](#Introduction)
- [Pre-requisites](#pre-requisites)
- [Installation and commands](#Installation/commands)

# Introduction
we will deploy a microk8s in linux(ubuntu - 18.04)/MacOs(not tested)and will create the docker image and push it local registry and  deploy the same docker in microk8s kube.

# Pre-requisites
Before we get started using the script. 
* Ensure you have installed docker.
* Snap need to be installed.
* Python need to be installed.

# Installation/commands
1. Below command will install microk8s and enabled dns,dashboard and registry
```
python ./simple_kube.py --install kube
```

2. Varies command to stop,start and check the status of microk8s.
```
python ./simple_kube.py --start/stop/status kube
```

3. List the pods running in microk8s
```
python ./simple_kube.py --list-pods kube
```

4. List the deployment running in microk8s
```
python ./simple_kube.py --list-deployment kube
```

5. Below command will create the deployment in microk8s.
```
python ./simple_kube.py --create-deployment <yaml_path>
```

6. Below command will create the docker images and kept locally.
```
python ./simple_kube.py --create-docker <Docker_file_path>
```

7. Below command will create the docker images and push it to local registry which is enabled in microk8s.
```
python ./simplekube.py --create-push-docker <Docker_file_path>
```

8. show the status docker images.
```
python ./simple_kube.py --status-docker-image <imagename>
```

9. Remove the docker images.
```
python ./simple_kube.py --remove-docker-image <imagename>
```

10. List the docker images.
```
python ./simple_kube.py --docker-image list
```

11. It will create the docker images and push it to local registry and deploy the same in microk8s.
Note: The above command need to run where the dockerfile exisits.
```
python ./simple_kube.py --create-push-deploy <docker_image_name>
```
