import csv
import time

def newMovieRating(user_id,movie_id,ratings):
    fields=[user_id,movie_id,ratings,time.time()]
    with open(r'./csv/ratings.csv', 'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
           
def createNewUser(user_id):
    fields=[[user_id,1,4.25],[user_id,464,4.12],[user_id,1270,4.52],[user_id,3996,4.05],[user_id,8981,4.23]]
    for i in fields:
        newMovieRating(i[0],i[1],i[2])