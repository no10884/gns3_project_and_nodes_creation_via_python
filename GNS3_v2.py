import requests
import json
import time
headers = {'Content-Type': 'application/x-www-form-urlencoded',}
ip_adr = "192.168.59.129:80"
api_url = f"http://{ip_adr}/v2"

project_name = "GNS3PY_test_" + str(time.time())

your_node_name = "debian_custom"
your_docker_template_id = "1931978b-f91f-4928-8fee-ac31ca4d887c"

#=========================================================================

data_project = {"name": project_name}
data_project = json.dumps(data_project)

response_project = requests.post(
    f'{api_url}/projects', 
    headers=headers, 
    data=data_project)
print("\nProject creation status: " + str(response_project.status_code))
project_id = response_project.json()
project_id = project_id["project_id"]
print("Project's ID: " + str(project_id) + "\n")

#=========================================================================

def counter_func():
    a = 0
    def node_counter():
        nonlocal a 
        a+=1
        return a
    return node_counter()

def create_docker_node_from_template(name, docker_template_id, x, y):
    data = {
        "name": name + str(counter_func()),
        "x": x,
        "y": y
    }
    data = json.dumps(data)

    response_node = requests.post(
    f'{api_url}/projects/{project_id}/templates/{docker_template_id}', 
    headers = headers, 
    data=data
    )
    
    output = response_node.json()    
    return output["node_id"]

#=========================================================================

data_link = {
    "nodes": [
        {
            "adapter_number": 0, 
            "node_id": f"{create_docker_node_from_template(your_node_name, your_docker_template_id, 0, 0)}", 
            "port_number": 0
        }, 
        {
            "adapter_number": 0, 
            "node_id": f"{
                create_docker_node_from_template(your_node_name, your_docker_template_id, 200, 0)}", 
            "port_number": 0
        }
    ]
}
data_link = json.dumps(data_link)

response = requests.post(
    f'{api_url}/projects/{project_id}/links',
    headers=headers,
    data=data_link,
)

#=========================================================================

input("Press <Enter> to delete this project") # Pause before deleting project

response_project = requests.delete(f'{api_url}/projects/{project_id}')
print("Project deletion status: " + str(response_project.status_code) + "\n")

