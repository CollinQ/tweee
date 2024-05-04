import pandas as pd
import ast
from scipy.spatial import distance
from test_embedding import embedding

def load_embeddings_from_excel(file_path):
    df = pd.read_excel(file_path)
    df['Embeddings'] = df['Embeddings'].apply(ast.literal_eval)
    return df

def cosine_similarity(vec1, vec2):
    return 1 - distance.cosine(vec1, vec2)

def find_most_similar_embedding(target_embedding, embeddings_df):
    highest_similarity = -1
    most_similar_index = None

    for index, row in embeddings_df.iterrows():
        similarity = cosine_similarity(target_embedding, row['Embeddings'])
        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar_index = index

    return most_similar_index, highest_similarity

def main():
    file_path = 'tweets.xlsx'
    embeddings_df = load_embeddings_from_excel(file_path)
    target_embedding = embedding
    index, similarity = find_most_similar_embedding(target_embedding, embeddings_df)
    print(f"The most similar embedding is at index {index} with a similarity of {similarity:.4f}")

if __name__ == "__main__":
    main()
