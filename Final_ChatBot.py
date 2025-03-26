import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Read the CSV file
file = "C:\\Users\\Admin\\Documents\\AI_Project\\ChatBot_Dataset.csv"
df = pd.read_csv(file, encoding="Latin")
                                                                                                 
# Create a dictionary from the DataFrame for fast lookups (Query -> Response)
response_dict = pd.Series(df.Response.values, index=df.Query.str.lower()).to_dict()
                                                                     
# Function to get most similar query using Sentence Transformers
def get_most_similar_query(user_input):
    user_embedding = model.encode(user_input.lower(), convert_to_tensor=True)
    max_similarity = 0
    best_match = None

    for query in response_dict.keys():
        query_embedding = model.encode(query, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(user_embedding, query_embedding).item()        
        #print(f"Query: {query} -> Similarity: {similarity}")
                                                                                            
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = query
    return best_match, max_similarity

def start_chat():
    print("...Welcome to the chat...type (exit / Byee) to exit the chat")
    
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "bye", "quit"]:
            print("ChatBot : Goodbye...Have a great day :)")
            break
            
        # Check if user input matches any query
        matched_query, similarity = get_most_similar_query(user_input)
        #print(matched_query, similarity)
        
        if matched_query and similarity > 0.7:  # You can adjust the threshold here
            print("ChatBot : ", response_dict[matched_query])
        else:
            print("ChatBot : Sorry...I didn't get it")

# Main Logic

#start_chat()

