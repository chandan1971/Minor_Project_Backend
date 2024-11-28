from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json

import bz2
import pickle as cPickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@api_view(['GET'])
def predictor(request):
    return Response({'message': 'Hello, Everyone!'})


@api_view(['GET'])
def formInfo(request):
    policy=request.GET['policy']
    # print(policy)
    recommended_schemes=recommend(policy)
    list_of_schemes=""
    for x in recommended_schemes:
        list_of_schemes+=x+"+"
    list_of_schemes = list_of_schemes[:-1]
    print(list_of_schemes)
    return Response(json.dumps(list_of_schemes),content_type="application/json")
    # return render(request,'index.html',{"policy":"response aa gya"})

@api_view(['GET'])
def userInfo(request):
    user_tags=request.GET['user_tags']
    day=request.GET['day']
    city=request.GET['city']
    cuisine=request.GET['cuisine']
    # domicile_of_tripura=request.GET['domicile_of_tripura']
    print(user_tags)
    print(day)
    print(city)
    print(cuisine)
    recommended_restaurants=recommendation_on_inputs(user_tags,day,city,cuisine)
    print(recommended_restaurants)
    # return Response({'message': 'Hello, Everyone!'})
    list_of_schemes=""
    # for x in recommended_schemes[2]:
    #     list_of_schemes+=x+'+'
    for x in range(0,len(recommended_restaurants[0])):
        for y in range(0,3):
            list_of_schemes+=str(recommended_restaurants[y][x])+'+'
            # print(type(recommended_schemes[y][x]))
    list_of_schemes = list_of_schemes[:-1]
    
    return Response(json.dumps(list_of_schemes))
    return render(request,'recommend.html',{"schemes":recommendation_on_inputs(user_tags,day,city,cuisine)})
@api_view(['GET'])
def policyInfo(request):
    policy=request.GET['policy']
    get_description(policy)
    return Response({"message":"policy mil gya"})
    

def decompress_pickle(file):
    with bz2.BZ2File(file, 'rb') as f:
        data = cPickle.load(f)
    return data

df_new = decompress_pickle('Notebooks/df_new.pbz2')
similarity = decompress_pickle('Notebooks/similarity.pbz2')
food_data=decompress_pickle('Notebooks/food_data.pbz2')
food_dataframe = pd.DataFrame(df_new)
# tfidf_matrix=decompress_pickle('Notebooks/tfidf_matrix.pbz2')
vectorizer=TfidfVectorizer()
tfidf_matrix=vectorizer.fit_transform(food_data['tags'])


def recommendation_on_inputs(user_tags,day,city,cuisine):

    

    user_tags_str =city+' '+day+' '+user_tags+' '+cuisine
    
    print("User Tags String:", user_tags_str) 
    
    tfidf_user_tags = vectorizer.transform([user_tags_str])
    cosine_similarities = cosine_similarity(tfidf_user_tags, tfidf_matrix).flatten()
    
    # print("Cosine Similarities:", cosine_similarities)
    top_similar_indices = cosine_similarities.argsort()[::-1]
    recommendations_restaurants=[]
    recommendations_business_id=[]
    recommendations_business_city=[]
    for i, index in enumerate(top_similar_indices):
        if (food_data.iloc[index]['business_id']) not in recommendations_restaurants:
            print(food_data.iloc[index]['name'])
            recommendations_business_id.append(str(food_data.iloc[index]['business_id']))
            recommendations_business_city.append(food_data.iloc[index]['city'])
            recommendations_restaurants.append(food_data.iloc[index]['name'])
            if(len(recommendations_restaurants)==5):
                break
    return [recommendations_business_id,recommendations_business_city,recommendations_restaurants]
    
def get_description(policy):    
    pol_data=policy_data.loc[policy_data["scheme_name"]==policy].head(1)
    
    if pol_data.empty:
        print("khali")
    else:
        print(pol_data)
    
    

def recommend(policy):
    #scheme index is the location of that scheme in the similarity_df
    scheme_index=similarity.index.get_loc(policy)


    #top_5 is storing the top 10 schemes having a similar applicant as the entered scheme
    top_5=similarity.iloc[scheme_index].sort_values(ascending=False)[1:6]

    return top_5.to_dict()




    
