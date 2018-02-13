def batch_gradient_descent(x, y, theta, alpha, m, max_iter):
    iterr = 0
    diff = [0, 0]
    error = 0;
    for i in range(m):
        error += (theta[0] + theta[1] * x[i] - y[i]) ** 2
    print("Initially deviation=", error)    #这个结果不对

    while iterr < max_iter:
        for i in range(m):
            diff[0] += theta[0] + theta[1] * x[i] - y[i]
            diff[1] += (theta[0] + theta[1] * x[i] - y[i]) * x[i]
        theta[0] = theta[0] - alpha * diff[0] / m
        theta[1] = theta[1] - alpha * diff[1] / m
        diff = [0, 0]     #别忘记置0！
        error = 0
        for i in range(m):
            error += (theta[0] + theta[1] * x[i] - y[i]) ** 2/ (2 * m)
        print('error=', error)
        print('theta=', theta)
        iterr = iterr + 1
        print('iters=', iterr)


matrix_x = [3, 1, 0, 4]
matrix_y = [2, 2, 1, 3]
MAX_ITER = 5
theta = [0, 1]
ALPHA = 0.1

batch_gradient_descent(matrix_x, matrix_y, theta, ALPHA, 4, MAX_ITER)
