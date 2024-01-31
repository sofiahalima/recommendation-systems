import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class Recommender:

    def __init__(self):
        super().__init__()

    # dataset https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset?resource=download
    books = pd.read_csv('/********/recommendation-systems/data/Books.csv')
    users = pd.read_csv('/********/recommendation-systems/data/users.csv')
    ratings = pd.read_csv('/*******/recommendation-systems/data/ratings.csv')
    # print(books.shape)
    # print(books.isnull().sum())
    # print(ratings.duplicated().sum())

    ratings_with_book_details = ratings.merge(books, on='ISBN')
    # print(ratings_with_book_details.head())
    ratings_with_book_details.drop(columns=['ISBN', 'Image-URL-M', 'Image-URL-L'], inplace=True)

    merge_all_df = ratings_with_book_details.merge(users.drop(columns=['Age', 'Location']), on='User-ID')
    #print(merge_all_df[merge_all_df['Book-Rating'] == 5])

    number_of_ratings_on_book = merge_all_df.groupby('Book-Title').count()['Book-Rating'].reset_index()
    number_of_ratings_on_book.rename(columns={'Book-Rating': 'number_of_ratings'}, inplace=True)
    #print(number_of_ratings_on_book.head())
    top_50_books = number_of_ratings_on_book[number_of_ratings_on_book['number_of_ratings']>=300].head(50).sort_values('number_of_ratings', ascending=False)
    #print(top_50_books)

    top_50_books_sorted = top_50_books.merge(books, on='Book-Title').drop_duplicates('Book-Title')[['Book-Title', 'Book-Author', 'Publisher','number_of_ratings', 'Image-URL-S']]
    #print(top_50_books_sorted.head())

    #Collaborative Filtering Based Recommender System
    #print(merge_all_df.head())
    user_rating_index = merge_all_df.groupby('User-ID').count()['Book-Rating']>100
    quality_user_rating = user_rating_index[user_rating_index].index

    merge_with_quality_users = merge_all_df[merge_all_df['User-ID'].isin(quality_user_rating)]

    final_df_with_high_ratings = merge_with_quality_users.groupby('Book-Title').count()['Book-Rating']>=50
    famous_books_df = final_df_with_high_ratings[final_df_with_high_ratings].index

    final_ratings_df = merge_with_quality_users[merge_with_quality_users['Book-Title'].isin(famous_books_df)]
    pt = final_ratings_df.pivot_table(index='Book-Title',columns='User-ID'
                              ,values='Book-Rating')

    pt.fillna(0,inplace=True)
    similarity_score = cosine_similarity(pt)



    def recommend(self, book_name):
        index = np.where(self.pt.index == book_name)[0][0]
        similar_books = sorted(list(enumerate(self.similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

        data = []

        for i in similar_books:
            item = []
            temp_df = self.books[self.books['Book-Title'] == self.pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-S'].values))

            data.append(item)
        return data