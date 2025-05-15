import numpy as np

def main():
    # Create a 2x2 matrix of zeros
    matrix = np.zeros((2, 2))

    # Add 1 to each element
    matrix += 1

    # Print the matrix
    print("Matrix:")
    print(matrix)

if __name__ == "__main__":
    main()