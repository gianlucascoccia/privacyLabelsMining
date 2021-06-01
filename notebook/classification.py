# %% Imports

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import cross_validate
from sklearn.model_selection import RepeatedKFold
from sklearn.pipeline import FeatureUnion, Pipeline

# %% Parameters

IN_FILE = '../data/processed/apps_top1000_all.csv'

TRAIN_SIZE = 0.95
N_SPLITS = 10
N_REPEATS = 3

scoring = {'f1': 'f1_macro',
           'precision': 'precision_macro',
           'recall': 'recall_macro'}

# %% Load data

apps = pd.read_csv(IN_FILE, delimiter=';')

# drop uneccessary columns
apps = apps.drop(['Unnamed: 0', 'id', 'appId', 'name', 'top_chart_position_free', 'category', 'publisher', 'top_chart_position_grossing', 'title', 'url', 'description', 'icon', 'genres', 'genreIds', 'primaryGenreId', 'contentRating', 'languages', 'size', 'requiredOsVersion', 'released', 'updated', 'version', 'developerId', 'developer', 'developerUrl', 'developerWebsite', 'score', 'reviews', 'price', 'free', 'currency', 'Unnamed: 0.1'], axis=1) #primaryGenre

# %% init classifiers

svm_clf = LinearSVC() 
maxent_clf = LogisticRegression()
forest_clf = RandomForestClassifier()

# %% perform classification

for classif in [('svm', svm_clf), 
                ('max_ent', maxent_clf), 
                ('random_forest', forest_clf)]:

                # %% Split dataset in train/test
                train_set, test_set = train_test_split(apps, train_size=TRAIN_SIZE)

                p = Pipeline([
                    ('class', classif[1])
                ])

                p.fit(train_set.drop('primaryGenre', axis=1), train_set["primaryGenre"])

                scores = cross_validate(p, 
                             train_set.drop('primaryGenre', axis=1), 
                             train_set["primaryGenre"], 
                             scoring=scoring, 
                             cv=RepeatedKFold(n_splits=N_SPLITS, n_repeats=N_REPEATS))

        
                print("{:^15}{:^9}{:^9}{:^9}{:^9}".format('Class','F1','Prec','Rec','TestAcc'))
                print("{:^15}".format(classif[0]), end='')
                for metric in scores.keys():
                    if 'test_' in metric:
                     # f1, precision, recall
                        print("{:^9}".format(np.mean(scores[metric]).round(5)), end='')
    
                test_score = p.score(test_set.drop('primaryGenre', axis=1), test_set["primaryGenre"])
                #print("Accuracy on test portion of data: {}".format(test_score))    
                print('{:^9}'.format(test_score.round(5)))   

                print("Fit times: {}".format(scores['fit_time']))

# %%
