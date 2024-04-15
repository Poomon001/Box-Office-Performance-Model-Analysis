import requests
import pandas as pd
import random
import time

api_key = "XXX"
MOVIES_PER_PAGE = 20
MAX_PAGE_VAL = 500


# Sorting by revenue.desc guarantees that the movie will have revenue data
params = {
    "api_key": "XXX",
    "sort_by": "revenue.desc",
    "language": "en-US",
    "include_adult": False,
    "include_video": False,
    # "page": 1,  # Page number of the results, there are 20 results per page
    # "primary_release_date.gte": "2000-01-01",  # Start date for movie release
    # "primary_release_date.lte": "2022-12-31",  # End date for movie release
    # "vote_count.gte": 1000,  # Minimum number of votes to filter movies
}

def get_movie_data(movie_id):
  # Fetch additional details including revenue
  movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
  details_response = requests.get(movie_details_url)
  movie_details = details_response.json()




  # genres = [genre['name'] for genre in movie_details["genres"]]
  # production_companies = [production['name'] for production in movie_details["production_companies"]]
  # spoken_languages = [language["english_name"] for language in movie_details["spoken_languages"]]

  # Fetch additional details including cast and crew
  movie_credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
  credits_response = requests.get(movie_credits_url)
  credits_data = credits_response.json()

  # Extract cast names
  # cast = [actor["name"] for actor in credits_data.get("cast", [])]
  movie_details["cast"] = credits_data["cast"]
  movie_details["crew"] = credits_data["crew"]

  # Extract crew names
  # crew = [member["name"] for member in credits_data.get("crew", [])]


  # Create a dictionary with movie attributes

  return movie_details

# Set the size of the dataset
dataset_size = 5000
num_iterations = dataset_size // MOVIES_PER_PAGE

movies_data = []
for i in range(0,num_iterations):
  # pick a random page number between 1 and 500, 500 being the max value that the page parameter will accept.
  random_page_id = random.randint(1,MAX_PAGE_VAL)
  params['page'] = random_page_id

  # Send request using /discover endpoint with above page parameter to get a semi-random list of movies.
  url = "https://api.themoviedb.org/3/discover/movie"
  response = requests.get(url, params=params)
  data = response.json()

  # List of 20 movies returned from the request
  list_of_movies = data['results']

  # Iterate through these 20 movies, extract relevant data and append them to our list
  for movie in list_of_movies:
    movie_id = movie["id"]
    movie_data = get_movie_data(movie_id)
    movies_data.append(movie_data)

  # Sleep for 1s due to API usage limits
  time.sleep(1)


df = pd.DataFrame(movies_data)
df.head()
df.shape
df.info()

# This is the code to save the dataframe as a csv file so that we don't need to run the data collection script multiple times
df.to_csv("TMDB_dataset.csv")