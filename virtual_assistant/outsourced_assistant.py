import requests


def call_outsourced_API(input):
    print("Calling RPI API")
    # requests.post('http://raspberrypi.local:5000')
    # print("GET DONE")
    try:
        req = requests.post('http://raspberrypi.local:5000/',
                        json={'query': input})
        return req.json()['response']
    except:
        return "sorry the server is not responding"


def main():

    while True:
        query = input(">:")
        print("<:", call_outsourced_API(query))


if __name__ == "__main__":
    main()
