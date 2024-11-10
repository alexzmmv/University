import numpy as np
import matplotlib.pyplot as plt

# Define the convex function f(x)
def convex_function(x):
    return x**2

# Define the derivative of f(x)
def convex_derivative(x):
    return 2 * x

# Define a non-convex function for case 4
def non_convex_function_2(x):
    return x**4 - 2*x**3 - x**2 + 3*x

# Define the derivative of the non-convex function
def non_convex_derivative_2(x):
    return 4*x**3 - 6*x**2 - 2*x + 3

# Gradient Descent function
def gradient_descent(eta, x0, iterations, func, derivative):
    history = []
    x = x0
    for _ in range(iterations):
        history.append(x)
        x = x - eta * derivative(x)
    return history

# Plot the function and the gradient descent path
def plot_function_and_path(x, func, path, title):
    plt.plot(x, func(x), label='Function')  # Plot the function line
    plt.scatter(path, [func(xi) for xi in path], color='red', label='Gradient Descent Path')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.title(title)
    plt.show()

# Main menu
while True:
    print("Gradient Descent Properties:")
    print("1. Convergence to Minimum for Small η (Convex Function)")
    print("2. Converge Faster by Increasing η (Convex Function)")
    print("3. Divergence with Too Large η (Convex Function)")
    print("4. Getting Stuck in a Local Minimum (Non-Convex Function)")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        eta_small = 0.1
        x0 = 3
        iterations = 20
        path = gradient_descent(eta_small, x0, iterations, convex_function, convex_derivative)
        plot_function_and_path(np.linspace(-5, 5, 100), convex_function, path, "Convergence to Minimum (Small η)")

    elif choice == '2':
        eta_large = 0.9
        x0 = 3
        iterations = 20
        path = gradient_descent(eta_large, x0, iterations, convex_function, convex_derivative)
        plot_function_and_path(np.linspace(-5, 5, 100), convex_function, path, "Converge Faster by Increasing η")

    elif choice == '3':
        eta_too_large = 1.2
        x0 = 2
        iterations = 5
        path = gradient_descent(eta_too_large, x0, iterations, convex_function, convex_derivative)
        plot_function_and_path(np.linspace(-10, 10, 100), convex_function, path, "Divergence with Too Large η")

    elif choice == '4':
        x0_non_convex = 0.9
        iterations = 100  # Increase the number of iterations for a better view
        path = gradient_descent(0.1, x0_non_convex, iterations, non_convex_function_2, non_convex_derivative_2)
        plot_function_and_path(np.linspace(-1.5, 2, 100), non_convex_function_2, path, "Getting Stuck in a Local Minimum (Non-Convex Function)")

    elif choice == '5':
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please select a valid option.")
