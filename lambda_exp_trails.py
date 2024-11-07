# Define the original lambda expression
original_lambda = lambda u: lambda x: u(x)(u)

# Test values
u_function = lambda u: u + 1
x_value = 5

# Apply beta reduction
result = original_lambda(u_function)(x_value)

# Output
print("Result after beta reduction:", result)
