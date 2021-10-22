#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = './testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    # YOUR CODE HERE
    user1_pref = (int)(user2.gender in user1.preferences)
    user2_pref = (int)(user1.gender in user2.preferences)
    compat_year = (36 - (user2.grad_year - user1.grad_year)**2)/36.0 #Compares Users
    similarity = 0.0
    for i, j in zip(user1.responses, user2.responses):
        similarity += ((i - j)/max(max(i, j), 1)) ** 2


    similarity /= len(user1.responses)
    similarity = similarity * compat_year * user1_pref * user2_pref

    return similarity


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
