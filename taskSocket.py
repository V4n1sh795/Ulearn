import socket
import pandas as pd
import sys

path = 'test/organizations.csv'

def test(org_name):
    global path
    df = pd.read_csv(path)
    org_str = df[df['Name'].str.contains(org_name, na=False)]
    return f"Сайт: {org_str['Website'].to_list()[0]}. Страна: {org_str['Country'].to_list()[0]}"
    # print(f"Сайт: {org_str['Website'].to_list()[0]}. Страна: {org_str['Country'].to_list()[0]}")

def start_server():
    host = "127.0.0.32"
    port = 12345
    # serv conf
    server = socket.socket()
    server.bind((host, port))
    server.listen(5)
    client, _ = server.accept()
    
    while True:
        inp = client.recv(1024).decode()
        if inp == 'exit':
            print("server dead")
            server.close()
            break
        else:
            data = test(inp)
            print(data)
            client.send(data.encode())
if __name__ == '__main__':
    try:
        if sys.argv[1] == 'test':
            start_server()
    except IndexError:
        pass