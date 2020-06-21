from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from pymongo import MongoClient

from dataTreating import *

def bayes(contents_clean):
    # 1.从数据库中获取数据
    df_train = find_db()
    # 2.划分数据集
    # x_train, x_test, y_train, y_test = train_test_split(df_train['contents_clean'], df_train['label'])

    x_train = df_train['contents_clean']
    y_train = df_train['label']


    # 3.特征抽取，用tf-idf进行文本特征提取
    transfer = TfidfVectorizer()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform([contents_clean])


    # 4.调用贝叶斯预估器
    classifier = MultinomialNB()
    classifier.fit(x_train, y_train)

    # 5.预估
    class_ =  classifier.predict(x_test)
    # 5.计算准确率
    # return classifier.score(x_test, [9])

    # 将类别和数字映射，输出标签
    label = [k for k, v in class_num().items() if v == class_[0]]

    return label[0]



def find_db():
    conn = MongoClient('mongodb://localhost:27017/')
    db = conn.test
    l = db.bayes.find_one()
    return l


if __name__ == '__main__':
    # import txt
    # s = txt.text
    # c, d = get_parameter(s)
    # print(bayes(c))


    print(0)

