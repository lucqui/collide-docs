import requests
import random
import json

# Yelp API key
api_key = "uhFKLhSDKoDAteMLDKoEqiOZL2qfU3mQhsD-piD46rS_ibItjhyfiYiXQLVBqD_rA43IolnXY-GFQYZOgJBm61hJSHVeDFGOVX_E43A_d3MPGjatZPkSaafw7EvhY3Yx"

headers = {
    'Authorization': 'Bearer %s' % api_key,
}

food_type = input("What type of food you would like?: ")

def generate_random_location():
    latitude = 41.6488 + (42.0383 - 41.6488) * random.random()
    longitude = -87.9256 - (87.9256 - 87.5236) * random.random()
    return latitude, longitude

user1_location = generate_random_location()
user2_location = generate_random_location()

midpoint_latitude = (user1_location[0] + user2_location[0]) / 2
midpoint_longitude = (user1_location[1] + user2_location[1]) / 2

url = f"https://api.yelp.com/v3/businesses/search?term={food_type}&latitude={midpoint_latitude}&longitude={midpoint_longitude}&radius=3219&limit=50"

response = requests.get(url, headers=headers)

try:
    businesses = response.json()["businesses"]

except KeyError:
    print("An error occurred or no businesses were found.")

else:
    json_data = response.json()

    # Write API data to businesses.json
    with open('businesses.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
            
    # Print geographical midpoint between both users
    print(f"The midpoint between both users is {midpoint_latitude}, {midpoint_longitude}")

    # Choosing three random businesses from the selection of 50 businesses
    random_businesses = random.sample(businesses, 3)

    # Prompt user 1 to rank the 3 restaurants
    print("User 1: Please rank the following restaurants from 1-3 (1 being the highest)")
    for i, business in enumerate(random_businesses):
        print(f"{i + 1}. {business['name']}")

    user1_rankings = {}
    for i, business in enumerate(random_businesses):
        ranking = int(input(f"Rank for {business['name']}: "))
        user1_rankings[business['name']] = ranking

    # Prompt user 2 to rank the 3 restaurants
    print("User 2: Please rank the following restaurants from 1-3 (1 being the highest)")
    for i, business in enumerate(random_businesses):
        print(f"{i + 1}. {business['name']}")

    user2_rankings = {}
    for i, business in enumerate(random_businesses):
        ranking = int(input(f"Rank for {business['name']}: "))
        user1_rankings[business['name']] = ranking
    
    # Combine user1 and user2 rankings
    combined_rankings = {}
    for name in set(user1_rankings.keys()).union(user2_rankings.keys()):
        try:
            combined_rankings[name] = (user1_rankings[name] + user2_rankings[name]) / 2
        except KeyError:
            if name in user1_rankings:
                combined_rankings[name] = user1_rankings[name]
        else:
            combined_rankings[name] = user2_rankings[name]

    # Print the collective top-ranked business
    top_ranked = max(combined_rankings, key=combined_rankings.get)
    print(f"Yummy choice! Seems like {top_ranked} might be your best bet based off both of your choices.")
