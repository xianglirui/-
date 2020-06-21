import pandas as pd
import jieba
import jieba.analyse
from pymongo import MongoClient

def read_data():
    """
    读取数据集，转换为DataFrame格式
    :return:
    :rtype:
    """
    df_news = pd.read_table('./data/val.txt', names=['category', 'theme', 'URL', 'content'], encoding='utf-8')
    df_news = df_news.dropna()
    return df_news


def jieba_cut(df_news):
    """
    使用结巴分词器对文本分词
    """
    content = df_news.content.values.tolist()

    content_S = []
    for line in content:
        current_segment = jieba.lcut(line)
        if len(current_segment) > 1 and current_segment != '\r\n':  # 换行符
            content_S.append(current_segment)

    df_content = pd.DataFrame({'content_S': content_S})
    stopwords = pd.read_csv("./data/stopwords.txt", index_col=False, sep="\t", quoting=3, names=['stopword'], encoding='utf-8')

    return df_content, stopwords


def drop_stopwords(contents,stopwords):
    """
    使用停用词表对文本进行筛选，筛除无关词
    :param contents:分词后的文本数据list
    :return:1.返回筛选后文本  2.将筛选后的单个词存入list，便于后面对单个词出现次数做统计
    :rtype:
    """
    contents_clean = []
    all_words = []
    for line in contents:
        line_clean = []
        for word in line:
            if word in stopwords:
                continue
            line_clean.append(word)
            all_words.append(str(word))
        contents_clean.append(line_clean)

    return contents_clean,all_words


def main():
    df_news = read_data()
    df_content, stopwords = jieba_cut(df_news)

    # 结巴分词要求传入的是一个list
    contents = df_content.content_S.values.tolist()
    stopwords = stopwords.stopword.values.tolist()
    contents_clean, all_words = drop_stopwords(contents, stopwords)

    df_train = pd.DataFrame({'contents_clean': contents_clean, 'label': df_news['category']})
    label_mapping = class_num()
    # 用数字替换掉文字标签
    df_train['label'] = df_train['label'].map(label_mapping)

    df_all_words = pd.DataFrame({'all_words': all_words})
    # 聚合统计每个词的次数，返回的是一个DataFrame
    words_count = df_all_words.groupby(by=['all_words'])['all_words'].agg({"count"})
    words_count = words_count.reset_index().sort_values(by=["count"], ascending=False)

    return words_count, df_train

def save_db():
    """
    将文本和标签数字存入数据库
    :return:
    :rtype:
    """
    w_cloud, train = main()
    conn = MongoClient('mongodb://localhost:27017/')
    db = conn.test
    contents_t = extract(train['contents_clean'].values)
    label_t = train['label'].values
    db.bayes.insert_one({"contents_clean":contents_t,"label":label_t.tolist()})
    print("存入完毕")

def extract(data):
    words = []
    for line_index in range(len(data)):
        try:
            words.append(' '.join(data[line_index]))
        except:
            print(line_index)
    return words

def class_num():
    return {"汽车": 1, "财经": 2, "科技": 3, "健康": 4, "体育": 5, "教育": 6, "文化": 7, "军事": 8, "娱乐": 9, "时尚": 0}

"""
真实需求开始
"""
def get_parameter(text):
    """
    接受请求中的文本参数，转换成DataFrame
    :param text:
    :type text:
    :return:
    :rtype:
    """
    ls = [text]
    data = {'content': ls}
    df_news = pd.DataFrame(data)
    df_content, stopwords = jieba_cut(df_news)

    contents = df_content.content_S.values.tolist()
    stopwords = stopwords.stopword.values.tolist()
    contents_clean, all_words = drop_stopwords(contents, stopwords)

    word_cloud = pd.DataFrame({"word_cloud":[x.strip() for x in contents_clean[0] if x.strip() != '']})
    # 去除'\n'，并将list元素转换成str
    contents_cleans = ' '.join([x.strip() for x in contents_clean[0] if x.strip() != ''])

    content_S_str = "".join([x.strip() for x in contents_clean[0] if x.strip() != ''])
    ten_top = jieba.analyse.extract_tags(content_S_str, topK=8, withWeight=True)

    return contents_cleans, word_cloud, ten_top



if __name__ == '__main__':

    # import txt
    # s = txt.text
    # print([s])
    # c,d,e = get_parameter(s)
    #
    #
    # from keyWordCloud import *
    # word(d)
    # print(d)
    #
    #
    print(0)
    main()


