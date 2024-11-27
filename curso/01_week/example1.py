import numpy as np

# Assuming we have some data X and labels y
# X: data points (n x d)
# y: true labels (+1, -1) (n x 1)

# Parameters
n, d = 100, 2  # 100 samples, 2-dimensional data
k = 10  # Number of classifiers to sample

# Random data and labels (for illustration purposes)
X = np.random.randn(n, d)  # n samples, d features
y = np.random.choice([1, -1], size=n)  # Random labels (+1 or -1)

# Define a simple error function (e.g., misclassification error)
def error(theta, theta_0, X, y):
    predictions = np.sign(np.dot(X, theta) + theta_0)  # Linear prediction
    return np.mean(predictions != y)  # Misclassification rate

# Randomly sample classifiers and choose the best one
best_error = float('inf')
best_theta = None
best_theta_0 = None

for j in range(k):
    # Randomly sample theta (d-dimensional) and theta_0
    theta_j = np.random.randn(d)  # Random vector in R^d
    theta_0_j = np.random.randn()  # Random scalar

    # Calculate the error for the current classifier
    current_error = error(theta_j, theta_0_j, X, y)
    
    # Update the best classifier if current one is better
    if current_error < best_error:
        best_error = current_error
        best_theta = theta_j
        best_theta_0 = theta_0_j

print("Best classifier parameters:")
print("θ:", best_theta)
print("θ0:", best_theta_0)
print("Error:", best_error)
