

# Quadratic function
def f(x, y, b):
    return 1/2 * (x**2 + b*y**2)

# Gradient of the function
def gradient(x, y, b):
    grad_x = x
    grad_y = b * y
    return np.array([grad_x, grad_y])

# Gradient descent function
def gradient_descent(x0, y0, b, learning_rate, iterations):
    x_vals, y_vals = [x0], [y0]

    for _ in range(iterations):
        grad = gradient(x0, y0, b)
        sk = (x0**2 + (b*y0)**2) / (x0**2 + b**3 * y0**2)
        x0 = x0 - learning_rate * sk * grad[0]
        y0 = y0 - learning_rate * sk * grad[1]
        x_vals.append(x0)
        y_vals.append(y0)

    return x_vals, y_vals

# Plotting the gradient descent iterations and contour lines
b_values = [1, 1/2, 1/5, 1/10]
learning_rate = 0.1
iterations = 50

# Create grid for plotting
x_range = np.linspace(-5, 5, 100)
y_range = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x_range, y_range)

# Plotting the function from the side for different b values
fig = plt.figure(figsize=(16, 8))


#DUMITRASCU CONSTANTIN ALEXANDRU


for b_value in b_values:
    #generate function plot
    ax1 = fig.add_subplot(2, 4, b_values.index(b_value) + 1)
    ax1.contour(X, Y, f(X, Y, b_value), levels=20, cmap='viridis')
    ax1.set_title(f'Contour Plot for b = {b_value}')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')

    # Perform gradient descent
    x_vals, y_vals = gradient_descent(2, 2, b_value, learning_rate, iterations)

    # Generate 3D plot and
    ax2 = fig.add_subplot(2, 4, b_values.index(b_value) + 5, projection='3d')
    ax2.plot_surface(X, Y, f(X, Y, b_value), cmap='viridis', alpha=0.3)
    ax2.scatter(x_vals, y_vals, [f(x, y, b_value) for x, y in zip(x_vals, y_vals)], c='red', label='Gradient Descent Iterations')
    ax2.set_title(f'Function Plot for b = {b_value}')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('f(x, y)')
    ax2.legend()

    # Show iterations on the top view
    ax1.scatter(x_vals, y_vals, c='blue', label='Gradient Descent Iterations')
    ax1.legend()

plt.tight_layout()
plt.show()
