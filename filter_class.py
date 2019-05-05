# Cài đặt các thư viện hỗ trợ
import matplotlib.pyplot as plt
import re
import nltk
import seaborn as sns
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC

class FilterEmail():
    def __init__(self):
        self.emails = pd.read_csv('emails.csv', header=0)

    def initialize_emails_and_data(self):
        output_text = ""
        # Đọc emails và các công đoạn tiền xử lý
        output_text += "{}".format(self.emails)
        self.emails .head()
        self.emails .columns = ['text', 'spam']

        output_text += "{}".format(self.emails.columns)
        output_text += "{}".format(self.emails.groupby('spam').count())

        # Biểu diễn dữ liệu
        label = self.emails .spam.value_counts()
        plt.figure(figsize=(12, 6))
        sns.barplot(label.index, label.values, alpha=0.9)
        plt.xticks(rotation='vertical')
        plt.xlabel('Spam', fontsize=12)
        plt.ylabel('Counts', fontsize=12)
        self.emails['length'] = self.emails['text'].map(lambda text: len(text))
        output_text += "{}".format(self.emails.groupby(['spam']).length.describe())
        return output_text

    def process_data(self):
        return self.cleaning_data()

    def cleaning_data(self):
        # Dùng thư viện nltk để làm sach dữ liêu

        #tách từ
        output_text = ""
        tokens = nltk.tokenize.word_tokenize
        self.emails['tokens'] = self.emails['text'].map(lambda text: nltk.tokenize.word_tokenize(text))
        output_text += "{}\n".format(self.emails['tokens'][1])

        # in ra các stopword và loai bỏ các stopword
        stopword = set(nltk.corpus.stopwords.words('english'))
        output_text += "{}\n".format(stopword)

        self.emails['filter_text'] = self.emails['tokens'].map(lambda tokens: [w for w in tokens if not w in stopword])

        # loại bỏ từ subject, xóa các ký tự đặc biệt
        self.emails['filter_text'] = self.emails['filter_text'].map(lambda text: text[2:])
        self.emails['filter_text'] = self.emails['filter_text'].map(lambda text: ' '.join(text))
        self.emails['filter_text'] = self.emails['filter_text'].map(lambda text: re.sub('[^A-Za-z0-9]+', ' ', text))

        # in ra emails
        output_text += "{}\n".format(self.emails['tokens'][1])
        output_text += "{}\n".format(self.emails['filter_text'][1])

        # dùng lemmatizer để làm gọn câu
        lemmatizer = nltk.WordNetLemmatizer()
        self.emails ['filter_text'] = self.emails ['filter_text'].map(lambda text: lemmatizer.lemmatize(text))
        output_text += "{}\n".format(self.emails ['filter_text'][1])
        output_text += "{}\n".format(self.convert_word_to_vector())

        return output_text

    def convert_word_to_vector(self):
        # Chuyển hóa văn bản thành vector
        output_text = ""
        self.count_vectorizer = CountVectorizer()
        x_counts = self.count_vectorizer.fit_transform(self.emails['filter_text'].values)
        y_counts = self.emails .iloc[:, 1].values

        output_text += "{}\n".format(x_counts.shape)
        output_text += "{}\n".format(y_counts.shape)
        tfidf_vectorier = TfidfTransformer()
        tfidf = tfidf_vectorier.fit_transform(x_counts)
        tf = self.emails .iloc[:, 1].values

        #Chia bộ dữ liệu thành train và test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x_counts, y_counts, test_size=0.20, random_state=42)
        output_text += "{}\n".format(self.X_train.shape)
        output_text += "{}\n".format(self.X_test.shape)
        output_text += "{}\n".format(self.y_train.shape)
        output_text += "{}\n".format(self.y_test.shape)

        return output_text


    def filter_emails(self):
        output_text = ""
        # Đưa dữ liệu bộ train vào model NBC
        classifier = MultinomialNB(alpha=1.0)
        classifier.fit(self.X_train, self.y_train)
        output_text += "{}\n".format(classifier.fit(self.X_train, self.y_train))

        # Dự đoán trên bộ X_test
        y_pred = classifier.predict(self.X_test)
        output_text += "{}\n".format(y_pred)

        # thử mô hình svm
        svc = LinearSVC()
        svc.fit(self.X_train, self.y_train)
        output_text += "{}\n".format(svc.fit(self.X_train, self.y_train))

        y_pred2 = svc.predict(self.X_test)
        output_text += "{}\n".format(y_pred2)

        # Thêm confusion matrix
        confu = confusion_matrix(self.y_test, y_pred)
        output_text += "{}\n".format(confu)

        # Kiểm tra độ chính xác trên tập dữ liệu
        accuracy_score(self.y_test, y_pred)
        output_text += "{}\n".format(accuracy_score(self.y_test, y_pred))
        accuracy_score(self.y_test, y_pred, normalize=False)
        output_text += "{}\n".format(accuracy_score(self.y_test, y_pred, normalize=False))

        # Thêm tập xác nhận validation
        validation = cross_val_score(estimator=classifier, X=self.X_train, y=self.y_train, cv=10)
        output_text += "{}\n".format(validation)

        val2 = validation.mean()
        output_text += "{}\n".format(val2)

        val3 = validation.std()
        output_text += "{}\n".format(val3)

        # classification_report
        classification = classification_report(self.y_test, y_pred, target_names=["non spam", "spam"])
        output_text += "{}\n".format(classification)

        # Dự đoán thư
        output_text += "{}\n".format(self.emails["text"][2500])

        pred = classifier.predict(self.count_vectorizer.transform(self.emails["text"]))

        output_text += "Results: {} \n".format(pred[2500])
        output_text += "Main: {} \n".format(self.emails['spam'][2500])
        return output_text


    def filter_by_id(self, email_id):
        # Đưa dữ liệu bộ train vào model NBC
        classifier = MultinomialNB(alpha=1.0)
        classifier.fit(self.X_train, self.y_train)

        # Dự đoán trên bộ X_test
        y_pred = classifier.predict(self.X_test)

        # thử mô hình svm
        svc = LinearSVC()
        svc.fit(self.X_train, self.y_train)

        y_pred2 = svc.predict(self.X_test)

        # Thêm confusion matrix
        confu = confusion_matrix(self.y_test, y_pred)

        # Kiểm tra độ chính xác trên tập dữ liệu
        accuracy_score(self.y_test, y_pred)
        accuracy_score(self.y_test, y_pred, normalize=False)

        pred = classifier.predict(self.count_vectorizer.transform(self.emails["text"]))

        return pred[email_id]
