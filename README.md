# Group 5 - NLP Final Project

### 1.	Project Title: Movie Recommendation Web Application

### 2.	Team Names: Group 5 - Carl Cruzan, Maciel Lopez, and Yasmin Elgamel

### 3.	Project Description


#### •	Objectives: ---- (Completed by Yasmin Elgamel)
State as clearly as possible what you want to do. What problem do you solve etc?

- The team will create a web application using Flask that will allow the user to enter a title of a movie that they like, and receive a recommendation for ten movies that are similar to their interest.
- If the user enters a title that is not in the database, the web application will display a message asking the user to enter the correct movie title.
- If the database has close matches to the user’s input, the web application will suggest a title with a closer match to the user’s input, and display recommendation for ten movies.
- We will use NLP features to lower characters, remove special characters and whitespaces, tokenize, and remove stop words. Then, cosine similarity will be added in order to find similar movies that will match the user’s interest and preference.


#### •	Usefulness: ---- (Completed by Yasmin Elgamel)
State as clearly as possible why your chosen application is useful.
Make sure to answer the following questions: Are there any similar or equivalent applications out here? 
If so, what are they and how is yours different? Which user group/stakeholders is your application targeting?

- This application will be useful for companies like Netflix, Amazon, Disney, and all television studios. It will help businesses understand the user’s interest and tailor their products based on their customers’ needs. This will help them increase profit and productivity.
- This application can also be helpful in theatres, so customers can find out if the new movie will match their preference before buying a ticket.
- In addition, from the user’s side, this application will be helpful and save lots of time for the user. They can easily and quickly find movies similar to what they like. It will also save them money, because users will buy movies they know they will enjoy.
- Netflix uses movie recommendation system; however, they use the user’s watch history to recommend movies. Our movie recommendation system is different, because it allows the customer to enter a title of a movie they like. Personally, I believe that using the watch history is not always effective, because most of the time I would start watching a movie and after twenty minutes I decide that I don’t like it. Then, Netflix fills the front page of my account with movies similar to the one I disliked. It is always effective to ask the person directly about what they like to achieve the most accurate movie recommendation system.
- Our application is targeting anyone who enjoys watching movies, and all businesses that create and/or sell movies.



#### •	Data: ---- (Completed by Carl Cruzan)

1- Describe dataset origin (who collected, when, and for what purpose): https://www.kaggle.com/datasets/ramjasmaurya/top-250s-in-imdb/data?select=imdb+%281000+tv+series%29+-+%28june+2022%29.csv

We are using a dataset from Kaggle encompassing the 1000 top-rated movies, 1000 top-rated TV series and 250 top-rated video games.  The dataset was pulled from IMDb as of June 2022.  The purpose of the dataset is for general use by those who have an interest in the topic and/or those interested in creating a project with the data.   

2- What is data format: csv, json?  The data is in three .csv files (one each for movies, TV series, and video games).

3- Provide initial data description:  **NOTE THAT THE TEXT FIELD FOR NLP IS IN BOLD**  
Movies File:  1000 records x 16 columns:  Ranking of movie, Movie name, Year, Certificate, Runtime, Genre, Rating, **DETAIL ABOUT MOVIE**, Director, Actor 1, Actor 2,	Actor 3, Actor 4,	votes, metascore,	Gross $
TV Series File:  1000 records x 13 columns:  Ranking of series, Series name, Year, Certificate,	Runtime, Genre,	Rating, **DETAILS ABOUT SERIES**, Actor 1,	Actor 2, Actor 3,	Actor 4, Votes
Video Game File:  250 records x 12 columns:  Video game name,	Year,	Genre, Rating, **DETAILS ABOUT GAME**, Director, Actor 1,	Actor 2, Actor 3,	Actor 4, Votes, Certificate
![image](https://github.com/yelgamel/Fall23-NLP-Final-Project/assets/147782148/829e8925-dbd3-4e3c-825e-1c9b88124267)

![image](https://github.com/yelgamel/Fall23-NLP-Final-Project/assets/147782148/7b865e99-d3c3-45e6-8de4-0a642ec671b6)

![image](https://github.com/yelgamel/Fall23-NLP-Final-Project/assets/147782148/c572e012-4059-4395-9109-a9d644b6c850)

- Besides a text field, what other information do you have
  (for example, review data -> location, stars, users; twitter data -> user, likes;...)
- Do you have labeled data?
- #records, #fields (columns if available), #NA values
- What type of cleaning does it require?
      
#### •	Functionalities: ---- (Completed by Maciel Lopez)

Describe tentatively what tasks your application will perform. There are two types of functions you would need to offer:
- NLP Functions: specific to your NLP tasks
- User Interaction: For example, allowing users to select/filter/search 
      
      
#### •	Communication and Sharing: ---- (Completed by Yasmin Elgamel)

- Communication method: Group 5 is communicating via Teams, Canvas, and Piazza.
- Github repository link for the project: https://github.com/yelgamel/Fall23-NLP-Final-Project
- Upload dataset: (Waiting for Carl and Maciel to provide the dataset)


### 4. Personal Contribution Statement: ---- (Each team member will complete this part separately)
- This part will be completed by each team member as part of the proposal and submitted on Canvas.

--------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------


# Group 5 - Team Notes:
### This section is to include all the notes, updates, and edits made on Github and the project. So, whenever you make changes please make a record of it here. Thanks, Yasmin Elgamel

----------------------------------------------------------------

### 10/12/2023: Note from Yasmin Elgamel:
- Group 5 members met on Teams @ 7PM MT / 9PM EST
- I Created the Github repository
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





















