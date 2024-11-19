import numpy as np

def random_linear_classifier(X, y, k):

    n_samples, n_feature = X.shape 

    best_w = None 
    best_error = float('inf') 

    for _ in range(k):
        w = np.random.randn(n_feature)
        predictions = np.sign(X @ w)
        error = np.mean(predictions != y)

        if error < best_error:
            best_w = w
            best_error = error 

    return best_w, best_error 

if __name__ == "__main__":
    np.random.seed(42)
    X  = np.random.randn(100,2)
    true_w = np.array([2,-1])
    y = np.sign(X @ true_w)

    k = 1000
    best_w, best_error = random_linear_classifier(X, y, k)

    print("Best parameter vector:", best_w)
    print("Best training error :", best_error)
