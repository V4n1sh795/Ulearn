import socket
import pandas as pd
import sys
import json

def method(inp):
    request_data = json.loads(inp)
    operation = request_data.get("operation")
    name = request_data.get("name")
    df = pd.read_csv('test/organizations.csv')
    org_str = df[df['Name'].str.contains(name, na=False)]
    
    match operation:

        case "get_website":  
            return f"{org_str['Website'].to_list()[0]}"
        
        case "get_country":
            return f"{org_str['Country'].to_list()[0]}"
        
        case "get_number_of_employees":
            return f"{org_str['Number of employees'].to_list()[0]}"
        
        case "get_description":
            return f"{org_str['Description'].to_list()[0]}"


def start_server():
    host = "127.0.0.32"
    port = 12345
    # serv conf
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    client, _ = server.accept()
    while True:
        inp = client.recv(1024).decode()
        if not inp:
            break
        print(inp)
        result = {"result": method(inp)}
        print(result)
        response_json = json.dumps(result)

        client.sendall(response_json.encode())

    server.close()
if __name__ == '__main__':
    try:
        if sys.argv[1] == 'test':
            start_server()
    except IndexError:
        pass
