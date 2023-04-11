import requests
import csv

def read_con_data(filename = "IO_API_Keys.txt"):

    '''
    Gets connection data from a file. Returns a list the AK and SK 
    ready to be used on HTTP methods
    '''

    with open(filename) as file:
        connection_details = [line.rstrip() for line in file]
        AK = connection_details[0]
        SK = connection_details[1]
    
    headers = {
    "accept": "application/json",
    "X-ApiKeys": "accessKey="+AK+";secretKey="+SK
    }

    return ['cloud.tenable.com', headers]

def dict_to_csv(dict_data, filename):

    headers = dict_data[0].keys()
    
    with open(filename+'.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(dict_data)

    return "CSV File Generated"

def get_io(resource = 'users'):

    '''
    Uses a HTTP GET method to retrive info from Tenable.io. If no
    resource specified, it will get the a json with current users
    '''

    data = read_con_data()
    host = data[0]
    headers = data[1]

    response = requests.get('https://'+host+'/'+resource, headers = headers)
    
    return response

def post_io(resource, payload):

    '''
    Uses a HTTP POST method to write info to Tenable.io.
    '''

    data = read_con_data()
    host = data[0]
    headers = data[1]
    headers["accept"] = "application/json"
    headers["content-type"] = "application/json"

    response = requests.post('https://'+host+'/'+resource, json=payload, headers = headers)
    
    return response

def put_io(resource, payload):

    '''
    Uses a HTTP PUT method to update info in Tenable.io.
    '''

    data = read_con_data()
    host = data[0]
    headers = data[1]
    headers["accept"] = "application/json"
    headers["content-type"] = "application/json"

    response = requests.put('https://'+host+'/'+resource, json=payload, headers = headers)
    
    return response

def show_scans():
    
    '''
    Connects to tenable.io using and creates a .csv report with all
    the scans created in T.io. Also Returns a list with all the scans id's
    '''

    response = get_io(resource='scans')
    scans = response.json()['scans']
    scans_id = []
    


    with open('tio_scans_report.csv', 'w') as file:
        file.write("Scan ID,Status,Name,Owner\n")
        #print("Scan ID\tStatus\tName\tOwner")
        for scan in scans:
            line = '{id},{status},{name},{owner}\n'.format(**scan)
            #print('{id}\t{status}\t{name}\t{owner} '.format(**scan))
            scans_id.append(scan['id'])
            file.write(line)

    return scans_id