import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

class MovieRecommender():

    def __init__(self):
        self.movies = pd.read_csv("./csv/movies.csv",encoding="Latin1")
        self.Ratings = pd.read_csv("./csv/ratings.csv")
        self.Tags = pd.read_csv("./csv/tags.csv",encoding="Latin1")
        self.sim_user_30_m = None

        self.Mean = self.Ratings.groupby(by="userId",as_index=False)['rating'].mean()
        self.Rating_avg = pd.merge(self.Ratings,self.Mean,on='userId')
        self.Rating_avg['adg_rating']=self.Rating_avg['rating_x']-self.Rating_avg['rating_y']

        self.check = pd.pivot_table(self.Rating_avg,values='rating_x',index='userId',columns='movieId')


        self.final = pd.pivot_table(self.Rating_avg,values='adg_rating',index='userId',columns='movieId')

        # Replacing NaN by Movie Average
        self.final_movie = self.final.fillna(self.final.mean(axis=0))

        # Replacing NaN by user Average
        self.final_user = self.final.apply(lambda row: row.fillna(row.mean()), axis=1)

        # user similarity on replacing NAN by user avg
        self.b = cosine_similarity(self.final_user)
        np.fill_diagonal(self.b, 0 )
        self.similarity_with_user = pd.DataFrame(self.b,index=self.final_user.index)
        self.similarity_with_user.columns=self.final_user.index


        # user similarity on replacing NAN by item(movie) avg
        self.cosine = cosine_similarity(self.final_movie)
        np.fill_diagonal(self.cosine, 0 )
        self.similarity_with_movie = pd.DataFrame(self.cosine,index=self.final_movie.index)
        self.similarity_with_movie.columns=self.final_user.index
        self.sim_user_30_u = None

    def find_n_neighbours(self,df,n):
        order = np.argsort(df.values, axis=1)[:, :n]
        df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
               .iloc[:n].index, 
              index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
        return df

    

    def get_user_similar_movies(self, user1, user2 ):
        common_movies = self.Rating_avg[self.Rating_avg.userId == user1].merge(
        self.Rating_avg[self.Rating_avg.userId == user2],
        on = "movieId",
        how = "inner" )
        return common_movies.merge( self.movies, on = 'movieId' )

    def User_item_score(self, user,item):
        a = self.sim_user_30_m[self.sim_user_30_m.index==user].values
        b = a.squeeze().tolist()
        c = self.final_movie.loc[:,item]
        d = c[c.index.isin(b)]
        f = d[d.notnull()]
        avg_user = self.Mean.loc[self.Mean['userId'] == user,'rating'].values[0]
        index = f.index.values.squeeze().tolist()
        corr = self.similarity_with_movie.loc[user,index]
        fin = pd.concat([f, corr], axis=1)
        fin.columns = ['adg_score','correlation']
        fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
        nume = fin['score'].sum()
        deno = fin['correlation'].sum()
        final_score = avg_user + (nume/deno)
        return final_score

    

    def prediction_movie(self, user):
        # top 30 neighbours for each user
        self.sim_user_30_m = self.find_n_neighbours(self.similarity_with_movie,30)
        a = self.get_user_similar_movies(370,86309)
        a = a.loc[ : , ['rating_x_x','rating_x_y','title']]

        score = self.User_item_score(320,7371)

        self.Rating_avg = self.Rating_avg.astype({"movieId": str})
        self.Movie_user = self.Rating_avg.groupby(by = 'userId')['movieId'].apply(lambda x:','.join(x))
        self.Movie_seen_by_user = self.check.columns[self.check[self.check.index==user].notna().any()].tolist()
        a = self.sim_user_30_m[self.sim_user_30_m.index==user].values
        b = a.squeeze().tolist()
        d = self.Movie_user[self.Movie_user.index.isin(b)]
        l = ','.join(d.values)
        Movie_seen_by_similar_users = l.split(',')
        Movies_under_consideration = list(set(Movie_seen_by_similar_users)-set(list(map(str, self.Movie_seen_by_user))))
        Movies_under_consideration = list(map(int, Movies_under_consideration))
        score = []
        for item in Movies_under_consideration:
            c = self.final_movie.loc[:,item]
            d = c[c.index.isin(b)]
            f = d[d.notnull()]
            avg_user = self.Mean.loc[self.Mean['userId'] == user,'rating'].values[0]
            index = f.index.values.squeeze().tolist()
            corr = self.similarity_with_movie.loc[user,index]
            fin = pd.concat([f, corr], axis=1)
            fin.columns = ['adg_score','correlation']
            fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
            nume = fin['score'].sum()
            deno = fin['correlation'].sum()
            final_score = avg_user + (nume/deno)
            score.append(final_score)
        data = pd.DataFrame({'movieId':Movies_under_consideration,'score':score})
        top_5_recommendation = data.sort_values(by='score',ascending=False).head(5)
        Movie_Name = top_5_recommendation.merge(self.movies, how='inner', on='movieId')
        Movie_Names = Movie_Name.title.values.tolist()
        return Movie_Names

