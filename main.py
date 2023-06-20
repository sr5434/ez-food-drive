import jwt.utils
import time
import math
import os
import json
import uuid
import requests

accessKey = os.environ["DOORDASH_KEY"]

token = jwt.encode(
    {
        "aud": "doordash",
        "iss": os.environ["DOORDASH_KEY"], #Doordash Developer ID
        "kid": os.environ["DD_KID"],#Doordash Developer Key ID
        "exp": str(math.floor(time.time() + 300)),
        "iat": str(math.floor(time.time())),
    },
    jwt.utils.base64url_decode(os.environ["DD_SS"]), #Doordash developer signing secret
    algorithm="HS256",
    headers={"dd-ver": "DD-JWT-V1"})
def deliver(business_address, 
            business_name, 
            business_phone, 
            business_instruct, 
            dropoff_addr, 
            dropoff_name, 
            dropoff_num, 
            dropoff_instruct, 
            num):
    """Simulate a DoorDash Delivery."""
    endpoint = "https://openapi.doordash.com/drive/v2/deliveries/"

    headers = {"Accept-Encoding": "application/json",
               "Authorization": "Bearer " + token,
               "Content-Type": "application/json"}

    request_body = { # Modify pickup and drop off addresses below
        "external_delivery_id": str(uuid.uuid4()),
        "pickup_address": business_address,
        "pickup_business_name": business_name,
        "pickup_phone_number": business_phone,
        "pickup_instructions": business_instruct,
        "dropoff_address": dropoff_addr,
        "dropoff_business_name": dropoff_name,
        "dropoff_phone_number": dropoff_num,
        "dropoff_instructions": dropoff_instruct,
        "order_value": num
    }

    create_delivery = requests.post(endpoint, headers=headers, json=request_body) # Create POST request
    return create_delivery.status_code
if __name__ == "__main__":
    if os.path.isfile("./data.json") != True:
        foodbank = {}
        pickup_locs = []
        foodbank["addr"] = input("Foodbank address: ")
        foodbank["name"] = input("Foodbank name: ")
        foodbank["phone"] = input("Foodbank phone number: ")
        foodbank["instruct"] = input("Foodbank instructions: ")
        while True:
            pickup_loc = {}
            pickup_loc["addr"] = input("Pickup address: ")
            pickup_loc["name"] = input("Pickup name: ")
            pickup_loc["phone"] = input("Pickup phone number: ")
            pickup_loc["instruct"] = input("Pickup instructions: ")
            pickup_loc["quant"] = input("Item quantity: ")
            pickup_locs.append(pickup_loc)
            if input("New user(y/n):") == "n":
                break
            else:
                continue
        data = {"foodbank": foodbank, "pickup_locs": pickup_locs}
        with open("data.json", "w") as outfile:
            json.dump(data, outfile)
    else:
        f = open('./data.json')

        # returns JSON object as 
        # a dictionary
        data = json.load(f)

        f.close()
        for i in data["pickup_locs"]:
            status = deliver(data["foodbank"]["addr"],
                data["foodbank"]["name"],
                data["foodbank"]["phone"], 
                data["foodbank"]["instruct"], 
                i["addr"], 
                i["name"], 
                i["phone"], 
                i["instruct"], 
                i["quant"])
            print("Status code: " + str(status))
        print("Done.")