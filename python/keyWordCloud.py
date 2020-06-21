from wordcloud import WordCloud
import matplotlib.pyplot as plt
from qiniu import Auth, put_file, etag
import qiniu.config
from qiniu.services.cdn.manager import create_timestamp_anti_leech_url
import time
import requests

import matplotlib


def word(words):
    """
    生词词云图片
    :param words:
    :type words:
    :return:
    :rtype:
    """
    words_count = words.groupby(by=['word_cloud'])['word_cloud'].agg({"count"})
    words_count = words_count.reset_index().sort_values(by=["count"], ascending=False)

    matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)

    wordcloud=WordCloud(font_path="./data/simhei.ttf",background_color=None,max_font_size=80)
    word_frequence = {x[0]: x[1] for x in words_count.head(100).values}
    wordcloud=wordcloud.fit_words(word_frequence)
    plt.imshow(wordcloud)
    wordcloud.to_file('./data/wordcloud.png')

    url = qiniu_picture()

    return url


def qiniu_picture():

    """
    上传图片到七牛云服务器
    注：ak、sk、bucket_name、base_url需要去七牛云配置空间，然后填写自己的信息
    """
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'ak'
    secret_key = 'sk'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'name'
    # 上传后保存的文件名
    key = 'python-bayes-ciyun.png'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key)
    # 要上传文件的本地路径
    localfile = './data/wordcloud.png'
    ret, info = put_file(token, key, localfile)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)

    """
    生成下载链接
    """

    # 或者直接输入url的方式下载
    base_url = 'http://baidu.com/'+key
    # 可以设置token过期时间
    private_url = q.private_download_url(base_url, expires=3600)
    print(private_url)
    r = requests.get(private_url)
    assert r.status_code == 200


    return private_url


if __name__ == '__main__':
    print(0)
