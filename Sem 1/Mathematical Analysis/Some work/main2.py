import numpy as np
import matplotlib.pyplot as plt

# Takagi Function (T(x))
def takagi(x, n_max=20):
    result = 1/2
    for n in range(1, n_max + 1):
        term = (1/2**n) * max(0, 1 - 2**n * abs(2**n * x - int(2**n * x)))
        result -= term
    return result

# Weierstrass Function (W(x))
def weierstrass(x, k_max=100):
    result = 0
    for k in range(1, k_max + 1):
        result += np.cos(2**k * np.pi * x) / 3**k
    return result

print("For graphing these functions, as a good programmer, I'll let you choose the definition domain [first, last] and the accuracy (how many points to take in that interval you set).")
print("We begin with the Takagi function:")
print("Note: 0 < first < last < 1\n")

first = float(input("First = "))
last = float(input("Last = "))
accuracy = int(input("Accuracy = "))

print("\nNow, we continue with the Weierstrass function:")
print("Note: Use a small domain for the function to look good.\n")

first_w = float(input("First = "))
last_w = float(input("Last = "))
accuracy_w = int(input("Accuracy = "))

print("\nCalculating points for plotting the Takagi function...")

# Create x values for plotting
x = np.linspace(first, last, accuracy)

# Evaluate the functions for the x values
takagi_values = [takagi(xi) for xi in x]

print("\nCalculating points for plotting the Weierstrass function...")

# Create x values for the Weierstrass Function
x_weierstrass = np.linspace(first_w, last_w, accuracy_w)
weierstrass_values = [weierstrass(xi) for xi in x_weierstrass]

# Plot the functions
plt.figure(figsize=(12, 4))

print("\nMaking the Takagi function graph...")
# Takagi Function on the left half
plt.subplot(121)
plt.plot(x, takagi_values, label='T(x)')
plt.title('Takagi Function')
plt.grid(True)

print("\nMaking the Weierstrass function graph...")
# Weierstrass Function on the right half
plt.subplot(122)
plt.plot(x_weierstrass, weierstrass_values, label='W(x)')
plt.title('Weierstrass Function')
plt.grid(True)

print("\nHere they are:")
plt.tight_layout()
plt.show()
