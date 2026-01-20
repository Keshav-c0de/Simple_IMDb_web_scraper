from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import html

container = []
master_genre_list = []
movie_genres = []
result = []
found = None

def check_description(container):
    movie_description=input("Type The Movie Name to See The Description ")
    for movies in container:
        if movie_description.lower() == movies["Title"].lower():
            print(movies["Description"])
            found = True 
            break
    
    if not found:
        print("Invaild Input")

url = "https://www.imdb.com/chart/top/?ref_=hm_nv_menu"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}

response = requests.get(url,headers=headers)
if response.status_code == 200:
    print("Success!")
else: 
    print(f"Something went wrong ERROR:{response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")
content=soup.prettify()

with open("inspect.html","w",encoding="utf-8") as f:
    f.write(content)

data =soup.find("script",{"type": "application/ld+json"})
string_data = data.string
json_data=json.loads(string_data)
for i in range(250):
    name=json_data["itemListElement"][i]["item"]["name"]
    clean_name = html.unescape(name)
    genre=json_data["itemListElement"][i]["item"]["genre"]
    image=json_data["itemListElement"][i]["item"]["image"]
    rating=json_data["itemListElement"][i]["item"]["aggregateRating"]["ratingValue"]
    description=json_data["itemListElement"][i]["item"]["description"]
    
    row ={
        "Title": clean_name,
        "Rating": rating,
        "Image": image,
        "Genre": genre,
        "Description": description,
    }
    container.append(row)
    raw_genres = genre.split(",")
    master_genre_list.extend([g.strip() for g in raw_genres])
    

unique_genres = sorted(list(set(master_genre_list)))
 
for _ in unique_genres:
    print(_)
chosen_genre=input("Choice The Prefered Genre From Following: ")

for movies in container:
    if chosen_genre.lower() in movies["Genre"].lower():
        result.append(movies)

print("Recommended Movies Are: ")

for movie in result:
    print(f"- {movie['Title']} ({movie['Rating']})")
    #print(f"  Poster: {movie['Image']}")

if input("type d to see check_description ")=="d":
    check_description(container)



