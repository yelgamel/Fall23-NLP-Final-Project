# Group 5 - NLP Final Project

### 1.	Project Title: Entertainment Recommendation Web Application

### 2.	Team Names: Group 5 - Carl Cruzan, Maciel Lopez, and Yasmin Elgamel

### 3.	Project Description


#### •	Objectives: ---- (Completed by Yasmin Elgamel)
State as clearly as possible what you want to do. What problem do you solve etc?

- The team will create a web application using Flask that will allow the user to enter a title of a movie, TV series, or video game that they like, and receive recommendation based on their interest.
- If the user enters a title that is not in the database, the web application will display a message asking the user to enter the correct title.
- If the database has close matches to the user’s input, the web application will suggest a title with a closer match to the user’s input, and display recommendation.
- We will use NLP features to lower characters, remove special characters and whitespaces, tokenize, and remove stop words. Then, cosine similarity will be added in order to find similar titles that will match the user’s interest and preference.


#### •	Usefulness: ---- (Completed by Yasmin Elgamel)
State as clearly as possible why your chosen application is useful.
Make sure to answer the following questions: Are there any similar or equivalent applications out here? 
If so, what are they and how is yours different? Which user group/stakeholders is your application targeting?

- This application will be useful for companies like Netflix, Amazon, Disney, and all television studios, and video game companies. It will help businesses understand the user’s interest and tailor their products based on their customers’ needs. This will help them increase profit and productivity.
- This application can also be helpful in theatres, so customers can find out if the new movie or TV series will match their preference before buying a ticket.
- In addition, this application will be helpful and save lots of time for the user. They can easily and quickly find the entertainment of their choice. It will also save money for the users.
- Netflix and video game companies use recommendation systems; however, they use the user’s history to recommend movies. Our Entertainment Recommendation System is different, because it directly asks the users for their preferred titles. Personally, I believe that using the user’s history is not always effective. For example, most of the time I would start watching a movie and after twenty minutes I decide that I don’t like it. Then, Netflix fills the front page of my account with movies similar to the one I disliked. It is always effective to ask the person directly about what they like to achieve the most accurate recommendation results.
- Our application is targeting anyone who enjoys video games, and likes watching movies and TV series. It also targets all businesses that create and/or sell movies, TV series, and video games.



#### •	Data: ---- (Completed by Carl Cruzan)

1. Describe dataset origin (who collected, when, and for what purpose): https://www.kaggle.com/datasets/ramjasmaurya/top-250s-in-imdb/data?select=imdb+%281000+tv+series%29+-+%28june+2022%29.csv

We are using a dataset from Kaggle encompassing the 1000 top-rated movies, 1000 top-rated TV series and 250 top-rated video games.  The dataset was pulled from IMDb as of June 2022 by Ram Jas.  The purpose of the dataset is for general use by those who have an interest in the topic and/or those interested in creating a project with the data.   

2. The data is in three .csv files (one each for movies, TV series, and video games).

3. The three files are desribed below:  **NOTE THAT THE TEXT FIELD FOR NLP IS IN BOLD** (and the number of blank fields, if any, are in parentheses)

Movies File:  1000 records x 16 columns:  Ranking of movie, Movie name, Year, Certificate(5), Runtime, Genre, Rating, Metascore(163), **DETAIL ABOUT MOVIE**, Director, Actor 1, Actor 2,	Actor 3, Actor 4,	votes, Gross $(18)

TV Series File:  1000 records x 13 columns:  Ranking of series, Series name, Year, Certificate(170), Runtime(25), Genre,	Rating(450), **DETAILS ABOUT SERIES(8)**, Actor 1(2),	Actor 2(2), Actor 3(6),	Actor 4(7), Votes

Video Game File:  250 records x 13 columns:  Ranking of video game, Video game name,	Year,	Genre(1), Rating(1), **DETAILS ABOUT GAME**, Director(3), Actor 1(20),	Actor 2(24), Actor 3(31),	Actor 4(72), Votes, Certificate(40)

Other than the blank fields, the data looks generally in good shape.  Formatting in the "year" columns seems to be inconsistent and often contains text other than just the year.  Words/names with non-English punctuation generally have issues that may need to be addressed (e.g. PokÃ©mon and ShÃ´tarÃ´ Morikubo).  

For some of the blank fields, we may fill using other information:  for example, TV Series Rating could be filled by looking at shows with similar rankings.  Others may have the whole record excluded (the 8 TV Series without any description).  Still other blanks may be ignored, such as video games without an actor.

      
#### •	Functionalities: ---- (Completed by Maciel Lopez)

Describe tentatively what tasks your application will perform. There are two types of functions you would need to offer:
- NLP Functions: specific to your NLP tasks
- User Interaction: For example, allowing users to select/filter/search 

This application will provide two groups of functions through a REST API: NLP tasks and user interactions. 

1. Users can perform NLP tasks such as text normalization, lemmatization, and stop word removal. The user can also get content-based recommendations from a chosen category, such as movies, or a mixture categories by providing the title of a movie, tv show, or video game. Recommendations can be filtered by the number of recommendations desired or by applicable fields such as genre, year, ranking, rating, runtime, or number of votes. The user will be able to choose the similarity metric used to recommend content.
2. User interactions include retrieving information about the dataset. These can be categories, such as movie, television show, or video game, or details about a specific item like the runtime of a movie or the genre.

On failure, users should receive appropriate errors. 

Below is an example API described with the OpenAPI specification. Potential API endpoints are '/recommendations' and '/data'. '/recommendations' will accept GET requests. Users query this endpoint, directly or through a website, to receive recommendations. '/data' can be accessed through GET requests to provide information about known content in the dataset.

```
openapi: 3.0.3
info:
  title: Entertainment Recommendation Engine
  description: |-
    Example description.
  version: 1.0.0
servers:
  - url: localhost
tags:
  - name: nlp
    description: NLP functions
  - name: user
    description: User interactions
paths:
  /recommendations:
    get:
      tags:
        - nlp
      summary: Get a recommendation
      description: Get recommendation
      responses:
        default:
          description: Successful operation
  /data/movies:
    get:
      tags:
        - user
      summary: Get a list of movies
      description: Get movies
      responses:
        default:
          description: successful operation
  /data/tv-shows:
    get:
      tags:
        - user
      summary: Get a list of television shows
      description: Get television shows
      responses:
        default:
          description: successful operation
  /data/video-games:
    get:
      tags:
        - user
      summary: Get a list of video games
      description: Get video games
      responses:
        default:
          description: successful operation
```


#### •	Communication and Sharing: ---- (Completed by Yasmin Elgamel)

- Communication method: Group 5 is communicating via Teams, Canvas, and Piazza.
- Github repository link for the project: https://github.com/yelgamel/Fall23-NLP-Final-Project
- Upload dataset: Data has been uploaded to Github by Carl Cruzan


### 4. Personal Contribution Statement: ---- (Each team member will complete this part separately)
- This part will be completed by each team member as part of the proposal and submit it on Canvas.

--------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------


# Group 5 - Team Notes:
### This section is to include all the notes, updates, and edits made on Github and the project. So, whenever you make changes please make a record of it here. Thanks, Yasmin Elgamel

----------------------------------------------------------------

### 10/12/2023: Note from Yasmin Elgamel:
- Group 5 members met on Teams @ 7PM MT / 9PM EST
- I Created the Github repository, and added Maciel and Carl as collaborators
- I Created and sent invites for the next Teams meeting on 10/19/2023 @ 5PM MT / 7PM EST
- Link to the next meeting, 10/19/2023 @ 5PM MT / 7PM EST: https://teams.microsoft.com/l/meetup-join/19%3ameeting_YjgwNGM1MjQtYTdjNi00NDhjLWI1NTItMDdkNTEwZTY2Njgz%40thread.v2/0?context=%7b%22Tid%22%3a%221113be34-aed1-4d00-ab4b-cdd02510be91%22%2c%22Oid%22%3a%220796ac8e-9df5-429e-aeb0-df31f53b6f97%22%7d 

### 10/13/2023: Note from Yasmin Elgamel:
- Today I created 2 folders on Github: Final Project folder and Testing Phase folder.
- In the Testing Phase folder, I created the following as a reference for the Final Project: SentimentAnalyzerWebApp.py, index.html, and result.html
- The app clean, tokenize, lemmatize, and find the polarity of the text entered by the user.
- To try the Flask app in the Testing Phase folder:
    1- From the Testing Phase folder, download index.html and result.html and put them in a folder called "templates". 
    2- Download TestingSentimentAnalyzerWebApp.py. 
    3- Make sure the "templates" folder, and .py file saved in the same area. 
    4- Run the .py file.

### 10/16/2023: Note from Yasmin Elgamel:
- I completed the following topics in this proposal: "Project Title", "Team Names"; and under "Project Description", I completed "Objectives", "Usefulness", and "Communication and Sharing" portions.



