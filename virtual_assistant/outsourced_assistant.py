import requests


def call_outsourced_API(input):
    print("Calling RPI API")
    req = requests.post('http://raspberrypi.local:5000', json={'query': input})

    return req.json()['response']


def main():

    while True:
        print("<:", call_outsourced_API(input(">:")))


if __name__ == "__main__":
    main()
