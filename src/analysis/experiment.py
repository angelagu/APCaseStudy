import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import datetime

data_direc = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data')
ignore_columns = ['Date']

def prepare_data(df):
	df = df.dropna()
	active_columns = df.columns.values.tolist()
	for c in ignore_columns:
		active_columns.remove(c)
	df = df[active_columns]
	return df

def generate_training_and_test_data(df, train_percentage):
	# Using daily percentage returns as the class labels;
	# 1 if return is positive, 0 if negative
	le = preprocessing.LabelEncoder()
	
	pos_indices = df['Daily Returns'] >= 0
	neg_indices = df['Daily Returns'] < 0
	df.loc[pos_indices, 'Labels'] = 1
	df.loc[neg_indices, 'Labels'] = 0
	df.Labels = le.fit(df.Labels).transform(df.Labels)

	features = df.columns[1:-1]
	X = df[features]    
	y = df.Labels    
	
	test_index = int(len(df) * train_percentage)

	X_train = X[:test_index]
	y_train = y[:test_index]             

	X_test = X[test_index:]   
	y_test = y[test_index:]

	return X_train, y_train, X_test, y_test  

def random_forest(x_train, y_train, x_test, y_test): 
	clf = RandomForestClassifier(n_estimators=10, n_jobs=-1)
	clf.fit(x_train, y_train)
	accuracy = clf.score(x_test, y_test)
	return accuracy

def knn(x_train, y_train, x_test, y_test): 
    clf = KNeighborsClassifier()
    clf.fit(x_train, y_train)
    accuracy = clf.score(x_test, y_test)
    return accuracy

def svm(x_train, y_train, x_test, y_test): 
	clf = SVC()
	clf.fit(x_train, y_train)
	accuracy = clf.score(x_test, y_test)
	return accuracy

def logistic_regression(x_train, y_train, x_test, y_test): 
	clf = LogisticRegression()
	clf.fit(x_train, y_train)
	accuracy = clf.score(x_test, y_test)
	return accuracy

def pca(df, filename, n_components=2):
	pca = PCA(n_components=n_components)
	X = pca.fit_transform(df)
	kmean = KMeans(n_clusters=4)
	Y = kmean.fit_predict(X)
	plt.figure()
	plt.scatter(X[:,0], X[:,1], c=Y)
	plt.title('%s PCA with Kmeans Clustering (K = 4)' %filename)
	plt.savefig('%s_%s.png' %(filename.lower(), 'pca'))

soybean_df = pd.read_csv('%s/%s.csv' %(data_direc, 'soybean_merged'))
soybean_oil_df = pd.read_csv('%s/%s.csv' %(data_direc, 'soybean_oil_merged'))

soybean_df = prepare_data(soybean_df)
soybean_oil_df = prepare_data(soybean_oil_df)

pca(soybean_df, 'Soybean')
pca(soybean_oil_df, 'Soybean_Oil')

print 'Soybean Results'
x_train, y_train, x_test, y_test = generate_training_and_test_data(soybean_df, 0.8)
print 'Random forest: ', random_forest(x_train, y_train, x_test, y_test)
print 'KNN: ', knn(x_train, y_train, x_test, y_test)
print 'SVM: ', svm(x_train, y_train, x_test, y_test)
print 'Logistic Regression: ', logistic_regression(x_train, y_train, x_test, y_test)
print 'Soybean Oil Results'
x_train, y_train, x_test, y_test = generate_training_and_test_data(soybean_oil_df, 0.8)
print 'Random forest: ', random_forest(x_train, y_train, x_test, y_test)
print 'KNN: ', knn(x_train, y_train, x_test, y_test)
print 'SVM: ', svm(x_train, y_train, x_test, y_test)
print 'Logistic Regression: ', logistic_regression(x_train, y_train, x_test, y_test)
