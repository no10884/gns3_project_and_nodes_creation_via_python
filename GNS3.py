import requests
import json
import time

ip_adr = "192.168.59.129:80"
api_url = f"http://{ip_adr}/v2"
template_id = "1931978b-f91f-4928-8fee-ac31ca4d887c"

headers = {'Content-Type': 'application/x-www-form-urlencoded',}

project_name = "GNS3PY_test_" + str(time.time())

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

data_node1 = {
    "name": "Debian_custom1", 
    "x": 0,
	"y": 0
}
data_node1 = json.dumps(data_node1)

response_node1 = requests.post(
    f'{api_url}/projects/{project_id}/templates/{template_id}', 
    headers = headers, 
    data=data_node1
)
print("Node creation 1 status: " + str(response_node1.status_code))
node_id1 = response_node1.json()
node_id1 = node_id1["node_id"]
print ("ID node 1: " + node_id1 + "\n")

#=========================================================================

data_node2 = {
    "name": "Debian_custom2", 
    "x": 200,
	"y": 0
}
data_node2 = json.dumps(data_node2)

response_node2 = requests.post(
    f'{api_url}/projects/{project_id}/templates/{template_id}', 
    headers = headers, 
    data=data_node2
)
print("Node creation 2 status: " + str(response_node2.status_code))
node_id2 = response_node2.json()
node_id2 = node_id2["node_id"]
print ("ID node 2: " + node_id2 + "\n")

#=========================================================================

data_link = {
    "nodes": [
        {
            "adapter_number": 0, 
            "node_id": f"{node_id1}", 
            "port_number": 0
        }, 
        {
            "adapter_number": 0, 
            "node_id": f"{node_id2}", 
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

