# -*- coding: utf-8 -*-
"""dmg-A2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aQEGcmPwxo6RY629skgzth3DsR6FmhpK
"""

from google.colab import drive
drive.mount('/content/drive/')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/dmg_A2/

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori,association_rules
import joblib
# from Apriori import apriori

movie_df = pd.read_csv("movies.csv",header=None)
rating_df = pd.read_csv("ratings.csv",header=None)
links_df = pd.read_csv("links.csv",header = None)
tags_df = pd.read_csv("tags.csv",header=None)
movie_df=movie_df.drop(0)
movie_df

rating_df.isnull().sum()

tags_df.isnull().sum()

links_df.isnull().sum()

movie_df.isnull().sum()

rating_df

tags_df

links_df

movie_df.describe()

rating_df.describe()

tags_df.describe()

links_df.describe()

movie_matrix=movie_df.to_numpy()
movie_matrix
movies=[]
for i in range (len(movie_matrix)):
  string=movie_matrix[i][2]
  lt=string.split('|')
  for m in lt:
    movies.append(m)
movies=set(movies)
movies=sorted(movies)
print(movies)

data=np.random.randint(1,size=(9743,20))
df_add=pd.DataFrame(data=data,columns=movies)
new_movie_df=pd.concat([movie_df,df_add],axis=1)
new_movie_df=new_movie_df.drop(0)
new_movie_df=new_movie_df.drop(2,axis=1)
new_movie_df

for i in range (9742):
  string=movie_matrix[i][2]
  lt=string.split('|')
  # print(lt)
  for m in lt:
    new_movie_df.at[i+1,m]=1

new_movie_df

new_movie_df.rename({0: 'Movie_Id', 1: 'Title'}, axis=1)

count_genere = new_movie_df.iloc[:,2:].sum(axis=0,skipna=True)
genre_count_lst = count_genere[:].tolist()
print(count_genere)
# genre_count_lst

frequency_tag_df = tags_df.iloc[:,1:].groupby(2).count()
frequency_tag_df

"""# **Common Genres**"""

plt.barh(movies,count_genere,color='hotpink')
plt.ylabel('Generes')
plt.xlabel('Count')

no_of_ratings = rating_df.iloc[1:,2].value_counts()
ratings_lst = no_of_ratings[:].tolist()
ratings=[4.0,3.0,5.0,3.5,4.5,2.0,2.5,1.0,1.5,0.5]

"""# **How much rating most people give?**"""

plt.bar(ratings,ratings_lst,color='lightgreen')
plt.ylabel('Count')
plt.xlabel('Ratings')

"""# **Top five Most rated movies**"""

top_five=rating_df.groupby(1).size().sort_values(ascending=False)[:5]
top_five

top_five_movies=[]
top_five_movie_count=list(top_five)
for i in top_five.keys():
  movie_title=new_movie_df[new_movie_df[0]==i]
  top_five_movies.append(movie_title.values[0][1])

plt.barh(top_five_movies,top_five_movie_count,color='orange')
plt.ylabel('movie')
plt.xlabel('rating count')

"""# **QUES 2**🕺"""

merged_df = pd.merge(rating_df, new_movie_df[[0, 1]], left_on=1, right_on=0)

merged_df['0_x']

merged_df.drop(['1_x','0_y',3],axis=1,inplace=True)

print(merged_df)
merged_df = merged_df.rename({1: 'Movie_Id', '0_x': 'User_Id','1_y':'Title',2:'Rating'}, axis=1)

merged_df

merged_df = merged_df.drop_duplicates(['User_Id','Title'])

merged_df

merged_df_pivot = merged_df.pivot(index='User_Id', columns='Title', values='Rating').fillna(0)
merged_df_pivot = merged_df_pivot.astype('float64')

merged_df_pivot

for j in merged_df_pivot.columns:
  
  merged_df_pivot.loc[merged_df_pivot[j] >= 1, j] = 1
  merged_df_pivot.loc[merged_df_pivot[j] < 1, j] = 0

merged_df_pivot = merged_df_pivot.astype('int64')
merged_df_pivot

"""# **Train Model**⛽

"""

f_set = apriori(merged_df_pivot, min_support=0.1, use_colnames=True)
f_set

ass_rule = association_rules(f_set, min_threshold=1, metric="lift")

# Save  as a picklefile
joblib.dump(ass_rule, 'model.pkl')
ass_rule

movies_sorted_recommendation=ass_rule.sort_values(by=['lift'],ascending=False)

movies_sorted_recommendation

"""# **Top Recommended Movies**🎥

"""

test_df = pd.read_csv("test.csv",header=None)
test_df=test_df.drop(0)
temp_lisss = (test_df.values)
final_liss = []
not_final_temp = []
for i in range(len(temp_lisss)):
  
  not_final_temp.append(temp_lisss[i][0].split("\n"))
  # final_liss.append(not_final_temp)

not_final_temp

def model_predict(temp_lisss):
  df_choice = movies_sorted_recommendation[movies_sorted_recommendation['antecedents'].apply(lambda x:len(x)==len(temp_lisss) and next(iter(x)) in temp_lisss)]
  top_list=df_choice.iloc[:,1].values
  
  top_recommendation=[]
  recommendation_count=4
  for i in top_list:
    for j in i:
      if recommendation_count>0 and j not in top_recommendation :
        top_recommendation.append(j)
        recommendation_count-=1

  # print(top_recommendation)
  for i in top_five.keys():
    
    if(len(top_recommendation)<4):
      movie_title=new_movie_df[new_movie_df[0]==i]
      # print(movie_title.values[0][1])
      top_recommendation.append(movie_title.values[0][1])
  return top_recommendation

final_ans = []

for i in not_final_temp:
    final_ans.append(model_predict(i))

# df_choice
print(final_ans)
test_df['recommendation']=final_ans
test_df.rename(columns = {0:'movies'}, inplace = True)
pd.DataFrame(test_df).to_csv('recommendation_list.csv',index=None)

index=1
for i in final_ans:
  print( str(index) +". "+str(i))
  index=index+1