
ML-Assignment 3
——————————————————-
Zheng Gao (zxg170430)
Ruolan Zeng (rxz171630)

———————————————————-
How to Run:
Executing with command `python3 NeuralNet.py [data path]` in corresponding directory.
If there is a error in data path, please modify path url from `https` to `http`.
————————————————————
Output summary:
For Iris dataset, Relu function gives the best result. Both training error and test error are smaller than sigmoid and tanh.
For Car dataset, tanh function gives the best result. Although its training error is not so small, the test error is the minimum.
For adult dataset, Sigmoid function give the best result. Both training error and test error are smaller than relu and tanh.
Details of results are in file "result.xlsx".
————————————————————
Assumptions:
We can ignore the bias neurons.
We can assume that the last column will be the class label column.
We can assume that the training and test datasets will have the same format i.e. same number and placement of columns.