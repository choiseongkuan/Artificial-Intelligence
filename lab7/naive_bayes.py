from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


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
    cv = CountVectorizer()
    cv_fit = cv.fit_transform(text_input)  # 单词出现的次数
    ft_name = cv.get_feature_names_out()  # 对应的单词
    return ft_name, cv_fit.toarray()


def predict(text_ls, x_array, ft_name, emotion_counter):  # 预测情绪
    most_likely_emotion = 0  # 初始化最有可能的情绪
    max_probability = 0  # 初始化最可能情绪的概率
    offset = 0  # 单词未在训练集出现的个数（用于拉普拉斯平滑）
    for text in text_ls:  # 计算文本计算单词未出现的个数
        if text not in ft_name:
            offset += 1
    for i in range(x_array.shape[0]):  # 遍历6种情绪
        posterior_probability = emotion_counter[i]/sum(emotion_counter)  # 先验概率，这里是某情绪在训练集出现的概率
        sum_xi_with_smoothing = np.sum(x_array[i, :]) + x_array.shape[1] + offset  # 计算某情绪中总的单词出现次数（采用拉普拉斯平滑）
        for text in text_ls:  # 遍历文本的单词
            if text in ft_name:  # 如果单词在训练集中出现
                posterior_probability *= ((x_array[i][np.where(ft_name == text)[0][0]]+1) / sum_xi_with_smoothing)  # 计算该单词在该情绪中出现的条件概率
            else:
                posterior_probability *= 1 / sum_xi_with_smoothing
        if posterior_probability > max_probability:  # 如果求得某情绪的概率更大则更新
            max_probability = posterior_probability  # 更新最可能情绪的概率
            most_likely_emotion = i  # 更新最有可能的情绪
    return most_likely_emotion


def adjust(text_ls, x_array, emotion_label, ft_name, emotion_counter):  # 调整模型
    for text in text_ls:  # 遍历文本中的单词
        if text not in ft_name:  # 当单词不在训练集时创建单词向量并入
            ft_name = np.append(ft_name, text)  # 训练集中加入单词
            text_col = np.zeros((6, 1))  # 初始化单词列向量
            text_col[emotion_label][0] = 1  # 在对应情绪位置置1
            x_array = np.concatenate((x_array, text_col), axis=1)  # 把单词向量并入训练矩阵
        else:
            x_array[emotion_label][np.where(ft_name == text)[0][0]] += 1  # 增加情绪对应单词的出现次数
    return x_array, ft_name


if __name__ == "__main__":
    train_text, train_emotion_tag, train_emotions = read_file("train.txt")  # 读取文件，导出每行文本，导出情绪与行号的对应，导出每行情绪（训练集）
    train_ft_name, res = preprocessing(train_text)  # 提取文本特征，计算单词词频
    train_result = np.array([res[train_emotion_tag[i][1]].sum(axis=0) for i in range(1, len(train_emotion_tag)+1)])  # 按情绪和单词合并词频
    test_text, test_emotion_tag, test_emotions = read_file("test.txt")  # # 读取文件，导出每行文本，导出情绪与行号的对应，导出每行情绪（测试集）
    correct = 0  # 预测正确次数
    emotions_count = []  # 各情绪出现的次数
    for emotion in test_emotion_tag.values():  # 遍历情绪与行号的对应关系
        emotions_count.append(len(emotion[1]))  # 某情绪的行号列表长度就是某情绪出现的次数
    for sample, emotion in zip(test_text, test_emotions):  # 运行测试集
        predict_emotion = predict(sample.split(), train_result, train_ft_name, emotions_count)  # 进行预测
        if predict_emotion+1 == emotion:  # 预测正确的情况
            correct += 1  # 预测正确则次数加一
        train_result, train_ft_name = adjust(sample.split(), train_result, emotion-1, train_ft_name, emotions_count)  # 调整模型
    print(f"accuracy: {correct/len(test_text)}")  # 打印准确率
