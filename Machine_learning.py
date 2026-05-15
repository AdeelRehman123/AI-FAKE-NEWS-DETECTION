# Sehla Razzak (24K-0575)

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class FakeNewsClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
        self.model = LogisticRegression(C=1.0, max_iter=1000)
        self.is_trained = False
    
    def create_training_data(self):
        """Create comprehensive training dataset"""
        
        # FAKE NEWS patterns (Label: 1)
        fake_news = [
            "Aliens found on Mars NASA confirms",
            "Secret cure for cancer discovered by scientists",
            "Government hiding truth about economy",
            "Miracle weight loss pill approved by FDA",
            "World will end tomorrow scientists warn",
            "PM resigns secretly last night",
            "Earthquake predicted next week",
            "Vaccines causing new dangerous disease",
            "Secret meeting of world leaders exposed",
            "Breaking shocking news everyone must know",
            "You won't believe what happened",
            "This one weird trick cures everything",
            "Celebrity dies shocking news",
            "Bank collapses people lose all money",
            "Emergency declared fake news spreading"
        ]
        
        # REAL NEWS patterns (Label: 0)
        real_news = [
            "Government announces new economic policy",
            "Pakistan wins cricket match against India",
            "PM addresses nation tonight at 8pm",
            "Stock market reaches all time high",
            "New budget approved by cabinet",
            "President signs new education bill",
            "Healthcare facilities expanded in rural areas",
            "Trade agreement signed with China",
            "New university campus inaugurated",
            "Farmers loan scheme announced by government",
            "COVID19 cases decrease in country",
            "Election commission announces schedule",
            "Supreme Court issues important verdict",
            "Foreign minister visits friendly nation",
            "Economic growth rate increases"
        ]
        
        headlines = fake_news + real_news
        labels = [1] * len(fake_news) + [0] * len(real_news)
        
        return headlines, labels
    
    def train_model(self):
        """Train the Logistic Regression model"""
        
        print("\n🤖 Training Machine Learning Model (Logistic Regression)...")
        
        # Create training data
        headlines, labels = self.create_training_data()
        
        # Convert text to numerical features
        X = self.vectorizer.fit_transform(headlines)
        y = np.array(labels)
        
        # Split for validation
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Calculate accuracy
        train_accuracy = self.model.score(X_train, y_train) * 100
        test_accuracy = self.model.score(X_test, y_test) * 100
        
        print(f"   ✅ Training Accuracy: {train_accuracy:.1f}%")
        print(f"   ✅ Test Accuracy: {test_accuracy:.1f}%")
        
        self.is_trained = True
        
        return self.model
    
    def predict(self, headline):
        """Predict if a headline is REAL or FAKE"""
        
        if not self.is_trained:
            self.train_model()
        
        # Convert headline to features
        headline_vector = self.vectorizer.transform([headline])
        
        # Get prediction
        prediction = self.model.predict(headline_vector)[0]
        probability = self.model.predict_proba(headline_vector)[0]
        
        # prediction: 0 = REAL, 1 = FAKE
        if prediction == 0:
            return {
                'prediction': 'REAL',
                'confidence': round(probability[0] * 100, 2),
                'label': 0
            }
        else:
            return {
                'prediction': 'FAKE',
                'confidence': round(probability[1] * 100, 2),
                'label': 1
            }

# Create global instance
ml_model = FakeNewsClassifier()

def get_ml_prediction(headline):
    """Simple function for Member 1 to call"""
    return ml_model.predict(headline)

if __name__ == "__main__":
    # Test the model
    ml_model.train_model()
    
    test_headlines = [
        "Government announces new economic policy",  # Should be REAL
        "Aliens found on Mars",                      # Should be FAKE
        "Pakistan wins cricket match",               # Should be REAL
        "Secret cure for cancer discovered"          # Should be FAKE
    ]
    
    print("\n" + "="*50)
    print("TESTING ML MODEL")
    print("="*50)
    
    for headline in test_headlines:
        result = get_ml_prediction(headline)
        print(f"\n📰 {headline}")
        print(f"   🤖 ML Prediction: {result['prediction']} ({result['confidence']:.1f}%)")