import pandas as pd
import time

class User:
    def __init__(self):
        self.dataset = pd.read_csv('csv/ratings.csv')
    
    def newMovieRating(self,user_id,movie_id,ratings):
        columns = ['userId','movieId','rating','timestamp']
        rows = []
        rows.append([user_id,movie_id,ratings,time.time()])
        df = pd.DataFrame(rows, columns=columns)
        result = self.dataset.append(df)
        return result
        
    
    def createNewUser(self,user_id):
        self.dataset = self.newMovieRating(user_id,1,4.25)
        self.dataset = self.newMovieRating(user_id,464,4.12)
        self.dataset = self.newMovieRating(user_id,1270,4.52)
        self.dataset = self.newMovieRating(user_id,3996,4.05)
        self.dataset = self.newMovieRating(user_id,8981,4.23)
        return self.dataset