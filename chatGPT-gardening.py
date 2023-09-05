# import library to make API calls
import requests

input_address_city = "San Anselmo"
input_address_state = "CA"
input_address_country = "US"
input_address_favorite_plant = "Kiwi"

# step one: call Zippopotamus API to retrieve zipcode for the city

service_url1 = "http://api.zippopotam.us/"+input_address_country+"/"+input_address_state+"/"+input_address_city
headers1 = {
  "Content-Type": "application/json",
}

response1 = requests.get(service_url1, headers=headers1)
response1 = response1.json()

zipcode = response1['places'][0]['post code']


# step two: look up USDA hardiness zode based on zipcode

service_url2 = "https://plant-hardiness-zone.p.rapidapi.com/zipcodes/"+zipcode
headers2 = {
	"X-RapidAPI-Key": "********************************",
	"X-RapidAPI-Host": "plant-hardiness-zone.p.rapidapi.com"
}

response2 = requests.get(service_url2, headers=headers2)
response2 = response2.json()

hardiness_zone = response2['hardiness_zone']


# step three: query chatGPT for suggestions for plants to plant based on what I know I already like

openai_api_key = "********************************"
service_url3 = "https://api.openai.com/v1/chat/completions"
prompt3 = "I like to eat "+input_address_favorite_plant+" and I like in USDA hardiness zone "+hardiness_zone+" , recommend 3 other plants that would grow well where I live and would produce similarly edible food. Return this information in JSON format with the following fields: name, flavor_description, planting_season, irrigtation_requirements, sun_exposure_requirements "

payload3 = {
    "model": "gpt-3.5-turbo",
    "temperature" : 1.0,
    "messages" : [
      {"role": "system", "content": prompt3}
      ] 
}

headers3 = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "+openai_api_key
}

response3 = requests.post(service_url3, json=payload3, headers=headers3)
response3 = response3.json()

# step four: print it out

print("Prompt: "+prompt3)
print("-----")
print("Response: "+response3['choices'][0]['message']['content'])