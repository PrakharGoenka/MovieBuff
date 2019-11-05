import csv
import pickle
import time

def newMovieRating(user_id,movie_id,ratings):
    fields=[user_id,movie_id,ratings,time.time()]
    with open(r'./csv/ratings.csv', 'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    return None
           
def createNewUser(username, password):
    print('called')
    try:
        with open ('./csv/users', 'rb') as infile:
            users = pickle.load(infile)
    except EnvironmentError:
        print(EnvironmentError)

    if username in users:
        return False, 'username already taken'

    user_id = len(username) + len(password)

    users[username] = (user_id, password)

    try:
        with open ('./csv/users', 'wb') as outfile:
            pickle.dump(users, outfile)
    except EnvironmentError:
        print(EnvironmentError)

    fields=[[user_id,1,4.25],[user_id,464,4.12],[user_id,1270,4.52],[user_id,3996,4.05],[user_id,8981,4.23]]
    for i in fields:
        newMovieRating(i[0],i[1],i[2])

    return True, 'user successfuly registered'