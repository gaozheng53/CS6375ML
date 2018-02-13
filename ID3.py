import csv
import math
import pandas
import sys
import random


# Compute last column's entropy and return the value
def entropyclass(dataSet):
    countone = 0
    countzero = 0
    for row in dataSet:
        curr = row[-1]
        if curr == "0":
            countzero = countzero + 1
        elif curr == "1":
            countone = countone + 1
    temp = countone / (countzero + countone)
    entro = -temp * math.log2(temp) - (1 - temp) * math.log2(1 - temp)
    return entro


# Return the specific column's H
def attrh(columnno, dataSet):
    countone = 0
    countzero = 0
    YY = 0
    ZY = 0
    ZZ = 0
    YZ = 0
    HY = 0
    HZ = 0
    for row in dataSet:
        curr = row[columnno]
        if curr == "0":
            countzero = countzero + 1
            if row[-1] == '0':
                ZZ = ZZ + 1
            elif row[-1] == '1':
                ZY = ZY + 1
        elif curr == "1":
            countone = countone + 1
            if row[-1] == '0':
                YZ = YZ + 1
            elif row[-1] == '1':
                YY = YY + 1
    if countone != 0:
        if YY == 0:
            HY = - (YZ / countone) * math.log2(YZ / countone)
        elif YZ == 0:
            HY = -(YY / countone) * math.log2(YY / countone)
        else:
            HY = -(YY / countone) * math.log2(YY / countone) - (YZ / countone) * math.log2(YZ / countone)
    if countzero != 0:
        if ZZ == 0:
            HZ = -(ZY / countzero) * math.log2(ZY / countzero)
        elif ZY == 0:
            HZ = (ZZ / countzero) * math.log2(ZZ / countzero)
        else:
            HZ = -(ZY / countzero) * math.log2(ZY / countzero) - (ZZ / countzero) * math.log2(ZZ / countzero)
    H = (countone / (countone + countzero)) * HY + (countzero / (countone + countzero)) * HZ  # smaller H, larger IG
    return H


# return the dataset with specific column value and without outputting this column
def split(dataset, attrcolumn, value):
    if attrcolumn >= len(dataset[0]) - 1:  # exceed attributes column
        return []
    out1 = []
    for row in dataset:
        if row[attrcolumn] == str(value):
            sub = row[:attrcolumn]
            sub.extend(row[attrcolumn + 1:])
            out1.append(sub)
    return out1


# return the number of current attributesy
def getattrnum(dataset):
    return len(dataset[0]) - 1


# return the columnno with the largest IG
def choosebestig(dataset):
    attrnum = getattrnum(dataset)
    entropyclassval = entropyclass(dataset)
    IG = 0
    bestcolumn = -1
    for columnno in range(attrnum):
        h = attrh(columnno, dataset)
        ig = entropyclassval - h
        if ig > IG:
            IG = ig
            bestcolumn = columnno
    return bestcolumn


# if pure return its pure class, otherwise return -1
def testpure(dataset):
    count1 = 0
    count0 = 0
    for row in dataset:
        curr = row[-1]
        if curr == '0':
            count0 += 1
        elif curr == '1':
            count1 -= 1
    if count0 == 0:
        return 1
    elif count1 == 0:
        return 0
    return -1



def majorclass(dataset):
    countone = 0
    countzero = 0
    for row in dataset:
        curr = row[-1]
        if curr == "1":
            countone += 1
        elif curr == "0":
            countzero += 1
    if countone > countzero:
        return 1
    else:
        return 0


# return decision tree as nest dictionary format
def createtree(parent, dataset, attrset, node_list):
    tp = testpure(dataset)
    if tp == 0 or tp == 1:  # pure
        return tp
    if len(dataset[0]) == 1:  # no attribute available or all attributes are pure,classify as majority class
        return majorclass(dataset)
    bestcolumn = choosebestig(dataset)
    bestcolumnname = attrset[bestcolumn]
    tree = {bestcolumnname: {}}  # construct decision tree
    attrset.remove(str(bestcolumnname))
    bestcolumnval = [row[bestcolumn] for row in dataset]
    uniqueval = set(bestcolumnval)  # get the best column's value set(shrink together)
    for value in uniqueval:
        if value == '0' or value == '1':
            subattr = attrset[:]  # copy
            tree[bestcolumnname][value] = createtree(tree, split(dataset, bestcolumn, str(value)), subattr, node_list)
    tree[bestcolumnname]["majority"] = majorclass(dataset)
    tree[bestcolumnname]["parent"] = parent
    if parent is not None:
        node_list.append(tree)
    return tree


def entry(dataset, node_list):
    return createtree(None, dataset, dataset[0][:-1], node_list)


def printtree(obj, indent=' '):
    def printt(obj, indent):
        for i, tup in enumerate(obj.items()):
            k, v = tup
            if k is "majority" or k is "parent":
                continue
            if isinstance(k, str): k = '%s' % k
            if isinstance(v, str): v = '%s' % v
            if isinstance(v, dict):
                v = ''.join(printt(v, indent + ' ' * len(str(k) + ': ')))  # calculate next level's indent
            if i == 0:
                if len(obj) == 1:
                    yield '\n%s%s = %s' % (indent, k, v)
                else:
                    yield '%s : %s\n' % (k, v)
            elif i == len(obj) - 3:
                yield '%s %s : %s' % (indent, k, v)  # loss sth
            else:
                yield '%s%s : %s\n' % (indent, k, v)

    print(''.join(printt(obj, indent)))


# count the number of leaves
def count_leaf(d):
    count = 0
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, dict):
                for key, value in v.items():
                    if key is "0":
                        count += count_leaf(value)
                    elif key is "1":
                        count += count_leaf(value)
    else:
        return 1
    return count


def classify(dic, instance):
    if isinstance(dic, dict):
        for key, value in dic.items():
            columnno = labels.index(key)
            ins_value = instance[columnno]
            sub = value[str(ins_value)]
            return classify(sub, instance)
    else:
        return dic


def prune(node_list, node_count, factor):
    prune_count = round(float(node_count)*factor)
    print("Number of node to prune:", prune_count)
    prune_index = random.sample(range(len(node_list)), min(prune_count,len(node_list)))
    for index in prune_index:
        node = node_list[index]
        for node_name, v in node.items():
            if "parent" in v.keys():
                parent = v["parent"]
                for parent_name, pv in parent.items():
                    for key, value in pv.items():
                        if isinstance(value, dict):
                            if node_name in value.keys():
                                pv[key] = v["majority"]


if __name__ == '__main__':
    # training_set.csv test_set.csv validation_set.csv 0.2

    # print(sys.argv)

    if len(sys.argv) != 5:
        print("Usage: python3 ID3-old.py [training file path] [testing file path] [validation file path] [prune factor]")

    train_file, test_file, valid_file, factor = sys.argv[1:]
    factor = float(factor)

    # pre_accuracy
    data1 = pandas.read_csv(train_file)
    colrow1 = data1.shape
    training_list = list(csv.reader(open(train_file)))
    labels = training_list[0][:-1]
    # print(labels)
    training_csvlist = list(csv.reader(open(train_file)))
    node_list = []
    dic1 = entry(training_list, node_list)  # dic1 is traininged tree
    printtree(dic1)
    # print(dic1)
    count_correct = 0
    for item in training_csvlist:
        if (item[0] == '0' or item[0] == '1') and str(classify(dic1, item[:-1])) == item[-1]:
            count_correct += 1
    print("Number of training instances = " + str(colrow1[0]))
    print("Number of training attributes = " + str(colrow1[1] - 1))
    node_count = str(dic1).count('X') + count_leaf(dic1)
    print("Total number of nodes in the tree = " + str(node_count))
    print("Number of leaf nodes in the tree = " + str(count_leaf(dic1)))
    print("Accuracy of the model on the training dataset = " + str(count_correct / len(training_csvlist)))

    valid_csvlist = list(csv.reader(open(valid_file)))
    count_correct = 0
    for item in valid_csvlist:
        if (item[0] == '0' or item[0] == '1') and str(classify(dic1, item[:-1])) == item[-1]:
            count_correct += 1
    data2 = pandas.read_csv(valid_file)
    colrow2 = data2.shape
    print("Number of validation instances = " + str(colrow2[0]))
    print("Number of validation attributes = " + str(colrow2[1] - 1))
    print("Accuracy of the model on the validation dataset before pruning = " + str(count_correct / len(valid_csvlist)))

    test_csvlist = list(csv.reader(open(test_file)))
    count_correct = 0
    for item in test_csvlist:
        if (item[0] == '0' or item[0] == '1') and str(classify(dic1, item[:-1])) == item[-1]:
            count_correct += 1
    data2 = pandas.read_csv(test_file)
    colrow2 = data2.shape
    print("Number of testing instances = " + str(colrow2[0]))
    print("Number of testing attributes = " + str(colrow2[1] - 1))
    print("Accuracy of the model on the testing dataset before pruning = " + str(count_correct / len(test_csvlist)))

    print("\n\n============ Start Pruning ============\n")
    prune(node_list, node_count, factor)

    print("\n============ After Pruning ============\n\n")

    valid_csvlist = list(csv.reader(open(train_file)))
    count_correct = 0
    for item in valid_csvlist:
        if (item[0] == '0' or item[0] == '1') and str(classify(dic1, item[:-1])) == item[-1]:
            count_correct += 1
    data2 = pandas.read_csv(train_file)
    colrow2 = data2.shape
    print("Number of training instances = " + str(colrow2[0]))
    print("Number of training attributes = " + str(colrow2[1] - 1))
    node_count = str(dic1).count('X') + count_leaf(dic1)
    print("Total number of nodes in the tree = " + str(node_count))
    print("Number of leaf nodes in the tree = " + str(count_leaf(dic1)))
    print("Accuracy of the model on the training dataset before pruning = " + str(count_correct / len(valid_csvlist)))

    valid_csvlist = list(csv.reader(open(valid_file)))
    count_correct = 0
    for item in valid_csvlist:
        if (item[0] == '0' or item[0] == '1') and str(classify(dic1, item[:-1])) == item[-1]:
            count_correct += 1
    data2 = pandas.read_csv(valid_file)
    colrow2 = data2.shape
    print("Number of validation instances = " + str(colrow2[0]))
    print("Number of validation attributes = " + str(colrow2[1] - 1))
    print("Accuracy of the model on the validation dataset before pruning = " + str(count_correct / len(valid_csvlist)))

    test_csvlist = list(csv.reader(open(test_file)))
    count_correct = 0
    for item in test_csvlist:
        if (item[0] == '0' or item[0] == '1') and str(classify(dic1, item[:-1])) == item[-1]:
            count_correct += 1
    data2 = pandas.read_csv(test_file)
    colrow2 = data2.shape
    print("Number of testing instances = " + str(colrow2[0]))
    print("Number of testing attributes = " + str(colrow2[1] - 1))
    print("Accuracy of the model on the testing dataset before pruning = " + str(count_correct / len(test_csvlist)))

    # listtest = list(csv.reader(open('self-test.csv')))
    # node_list = []
    # dic = entry(listtest, node_list)
    # printtree(dic)
    # print(len(node_list))
    # print(count_leaf(dic))