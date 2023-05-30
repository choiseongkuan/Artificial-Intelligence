from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


class Kmeans:
    def __init__(self, k, ft_arr):
        self.k = k
        self.ft_arr = ft_arr


def read_file(file_path):  # 读取文件
    text_ls = []  # 文本列表
    emotion_ls = []  # 情绪列表
    emotion_dict = {}  # 情绪与对应情绪行号的对照
    with open(file_path, 'r') as f:
        lines = f.readlines()  # 按行读取
        for i, line in enumerate(lines[1:]):
            word_list = line.split()  # 按空格分开提取
            emotion_num = int(word_list[1])  # 情绪编号
            if emotion_num not in emotion_dict:  # 当没有某情绪时添加该情绪
                emotion_dict[emotion_num] = (word_list[2], [])
            emotion_dict[emotion_num][1].append(i)  # 添加该行的情绪
            emotion_ls.append(emotion_num)  # 把行号加入到情绪所对应的列表
            text_ls.append(" ".join(word_list[3:]))  # 把按括号分开的文本重新组合成字符串加入文本列表
    emotion_dict_ = {}
    for i in range(1, 7):  # 按情绪编号顺序重排
        emotion_dict_[i] = emotion_dict[i]
    return text_ls, emotion_dict_, emotion_ls


def preprocessing(text_input):  # 提取文本特征
    cv = CountVectorizer(use_idf=False)
    cv_fit = cv.fit_transform(text_input)  # 计算词频后
    ft_name = cv.get_feature_names_out()  # 对应的单词（特征）
    return ft_name, cv_fit.toarray()


if __name__ == "__main__":
    train_text, train_emotion_tag, train_emotions = read_file("train.txt")  # 读取文件，导出每行文本，导出情绪与行号的对应，导出每行情绪（训练集
    train_ft_name, train_ft_arr = preprocessing(train_text)

