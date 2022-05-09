import requests


def call_outsourced_API(input_val):
    print("Calling RPI API")
    # requests.post('http://raspberrypi.local:5000')
    # print("GET DONE")
    req = requests.post('http://localhost:6000/',
                    json={'query': input_val})

    # return req.json()['response'], req.json()['html']
    return req.json()['html']


def main():

    while True:
        query = input(">:")
        print("<:", call_outsourced_API(query))


if __name__ == "__main__":
    main()
