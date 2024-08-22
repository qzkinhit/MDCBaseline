def getErrorNum(df_1, df_2, set):
    error_num0 = 0
    for i in set:
        try:
            error_num0 += max(df_1.compare(df_2).iloc[:][i]["self"].notnull().sum(),
                          df_1.compare(df_2).iloc[:][i]["other"].notnull().sum())

        except:
            print(i+" is same or dont hava_"+i)
            continue;
    return error_num0
def getCorrectRepairs(dfclean,dfrepair,dforigin, set):
    repair = dfrepair.compare(dforigin, keep_equal=True, keep_shape=True)#真正的修复
    origin = dfclean.compare(dforigin, keep_equal=True, keep_shape=True)#理想的修复
    error_num0=getErrorNum(dfclean, dforigin, set)#所有正确的修复个数
    graph=repair.compare(origin, keep_shape=True)#找到每个属性下面的self，非null部分，就是没修出来的
    error_num1 = 0
    for i in set:
        try:
            error_num1 += graph[:][i]["self"]["other"].notnull().sum()
        except:
            continue;
    return error_num0-error_num1;


def calculate_accuracy_and_recall(clean, dirty, cleaned, attributes):
    """
    计算指定属性集合下的修复准确率和召回率

    :param clean: 干净数据 DataFrame
    :param dirty: 脏数据 DataFrame
    :param cleaned: 清洗后数据 DataFrame
    :param attributes: 指定属性集合
    :return: 修复准确率和召回率
    """
    total_true_positives = 0
    total_false_positives = 0
    total_true_negatives = 0

    for attribute in attributes:
        clean_values = clean[attribute]
        dirty_values = dirty[attribute]
        cleaned_values = cleaned[attribute]

        # 对齐索引
        common_indices = clean_values.index.intersection(cleaned_values.index).intersection(dirty_values.index)
        clean_values = clean_values.loc[common_indices]
        dirty_values = dirty_values.loc[common_indices]
        cleaned_values = cleaned_values.loc[common_indices]

        # 正确修复的数据
        true_positives = ((cleaned_values == clean_values) & (dirty_values != cleaned_values)).sum()
        # 修错的数据
        false_positives = ((cleaned_values != clean_values) & (dirty_values != cleaned_values)).sum()
        # 应该需要修复的数据
        true_negatives = (dirty_values != clean_values).sum()

        # 打印 dirty_values 和 clean_values 不同的那些行及其索引
        mismatched_indices = dirty_values[dirty_values != clean_values].index
        print("打印 dirty_values 和 clean_values 不同的那些行")
        # print(f"Mismatched indices for {attribute}: {mismatched_indices.tolist()}")
        print(f"Dirty Values at mismatched indices:\n{dirty_values.loc[mismatched_indices]}")
        print(f"Clean Values at mismatched indices:\n{clean_values.loc[mismatched_indices]}")
        print("=" * 40)
        # 打印修复错误的数据
        print("打印没修复的数据")
        false_positives_indices = cleaned_values[
            (cleaned_values != clean_values) & (dirty_values == cleaned_values)].index
        # print(f"False positive indices for {attribute}: {false_positives_indices.tolist()}")
        print(f"Dirty Values at false positive indices:\n{dirty_values.loc[false_positives_indices]}")
        print(f"Clean Values at false positive indices:\n{clean_values.loc[false_positives_indices]}")
        print(f"Cleaned Values at false positive indices:\n{cleaned_values.loc[false_positives_indices]}")
        print("=" * 40)
        total_true_positives += true_positives
        total_false_positives += false_positives
        total_true_negatives += true_negatives
        print("Attribute:", attribute, "修复正确的数据:", true_positives, "修复错误的数据:", false_positives,
              "应该修复的数据:", true_negatives)

    # 总体修复的准确率
    accuracy = total_true_positives / (total_true_positives + total_false_positives)
    # 总体修复的召回率
    recall = total_true_positives / total_true_negatives
    # 计算 F1 值
    if accuracy + recall == 0:
        f1 = 0  # 防止除以零
    else:
        f1 = 2 * (accuracy * recall) / (accuracy + recall)

    print(f"F1 值: {f1}")
    print("总准确率:", accuracy, "总召回率:", recall)
    return accuracy, recall

# a,b = input().split(",")
# a = float(a)
# b = float(b)
# print(2*a*b/(a+b))