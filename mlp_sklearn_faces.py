import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score
import tensorflow as tf 
import os 
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sns



data = []  # List to store image data
labels = []  # List to store labels

# Define a function to extract the person label from the file name
def extract_person_label(file_name):
    return int(file_name.split('.')[0].replace('subject', '')) - 1  # Subtract 1 to make labels start from 0

# Load data and labels
dataset_dir = os.path.join(os.path.dirname(__file__), 'data/')

for file_name in os.listdir(dataset_dir):
    img = plt.imread(os.path.join(dataset_dir, file_name))
    # print(img.shape)
    data.append(img.flatten())  # Flatten image into a 1D array
    labels.append(extract_person_label(file_name))

data = np.array(data)
labels = np.array(labels)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

#model selection
from sklearn.neural_network import MLPClassifier
#create a classifier
mlp = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=250, activation='relu', solver='adam', random_state=42)

print('start training')
#train the model
mlp.fit(X_train, y_train)
#training model score
print("Training Data Accuracy:", mlp.score(X_train, y_train))

#test data score
y_pred = mlp.predict(X_test)
print("Test Data Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

#display the confusion matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)
#plot the confusion matrix
sns.heatmap(cm, annot=True)
plt.show()
