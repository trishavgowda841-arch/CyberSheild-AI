import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("dataset.csv", encoding=" ISO-8859-1", usecols =[0 , 1], engine ="python")

# Keep only required columns
data = data[['v1', 'v2']]

# Rename columns
data.columns = ['label', 'message']

# Convert labels
data['label'] = data['label'].map({
    'ham': 0,
    'spam': 1
})

X = data['message']
y = data['label']

vectorizer = TfidfVectorizer(stop_words='english')
X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"Model Accuracy: {accuracy * 100:.2f}%")

pickle.dump(model, open("phishing_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model saved successfully!")