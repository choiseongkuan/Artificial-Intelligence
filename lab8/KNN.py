from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue


train_size = 996
test_size = 250


class Sample:  # 样本点类
    def __init__(self, distance, emotion):
        self.distance = distance  # 与测试样本相差的距离
        self.emotion = emotion  # 该样本点的情绪

    def __lt__(self, other):
        return self.distance < other.distance  # 按距离升序排序


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
    tv = TfidfVectorizer(use_idf=False)  # 使用TF提取
    tv_fit = tv.fit_transform(text_input)  # 计算词频后进行归一化
    ft_name = tv.get_feature_names_out()  # 对应的单词（特征）
    return ft_name, tv_fit.toarray()


def predict(test_input, array, emotions, k):
    que = PriorityQueue()  # 初始化优先队列
    emotion_ls = [0 for i in range(6)]  # 初始化每个情绪出现的次数
    most_often = 0  # 最大的出现次数
    most_likely_emotion = 0  # 最可能的情绪
    for i in range(train_size):  # 遍历所有训练样本行
        distance = np.linalg.norm(array[i, :] - array[test_input, :])  # 计算测试样本和当前训练样本的欧式距离
        que.put(Sample(distance, emotions[i]))  # 把样本点入队
    for i in range(k):  # 计算前k个样本点在对应情绪的出现次数
        sample = que.get()
        # emotion_ls[sample.emotion-1] += 1 / (sample.distance+0.2)
        emotion_ls[sample.emotion - 1] += 1
    for i in range(len(emotion_ls)):  # 找出众数样本点对应的情绪
        if emotion_ls[i] > most_often:
            most_often = emotion_ls[i]
            most_likely_emotion = i+1
    return most_likely_emotion


if __name__ == "__main__":
    train_text, train_emotion_tag, train_emotions = read_file("train.txt")  # 读取文件，导出每行文本，导出情绪与行号的对应，导出每行情绪（训练集）
    test_text, test_emotion_tag, test_emotions = read_file("test.txt")  # 读取文件，导出每行文本，导出情绪与行号的对应，导出每行情绪（测试集）
    merge_text = train_text + test_text  # 合并训练文本和测试文本，用于一次性提取特征
    ft_n, arr = preprocessing(merge_text)  # 提取文本特征
    k_ls = []
    accuracy_ls = []
    maxa = 0
    for k in range(1, 100):
        correct = 0  # 预测正确次数
        total = 0  # 总预测次数
        for i in range(test_size):  # 遍历所有测试样本
            total += 1
            predict_emotion = predict(train_size+i, arr, train_emotions, k)  # 预测情绪
            if predict_emotion == test_emotions[i]:  # 预测正确的情况
                correct += 1
        print(f"accuracy： {correct/total}")
        k_ls.append(k)
        accuracy_ls.append(correct/total)
        if correct/total > maxa:
            maxa = correct/total
    print(maxa)
    plt.plot(k_ls, accuracy_ls)
    plt.xlabel("k")
    plt.ylabel("accuracy")
    plt.title("Relationship between k and accuracy")
    plt.show()
# k = 43
