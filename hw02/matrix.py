import os
import re

class SparseMatrix:
    """
        A class to represent a sparse matrix.
        
        Attributes
        ----------
        Rows : int
            Number of rows in the matrix
        Colu : int
            Number of columns in the matrix
        elements : dict
            Dictionary to store non-zero elements with keys as (row, col) and values as the element value
        
        Methods
        -------
        read_from_file(filePath):
            Reads the sparse matrix from a file.
        getElement(currRow, currCol):
            Returns the element at the specified position.
        setElement(currRow, currCol, value):
            Sets the element at the specified position.
        add(other):
            Adds two sparse matrices.
        subtract(other):
            Subtracts two sparse matrices.
        multiply(other):
            Multiplies two sparse matrices.
        __str__():
            Returns the string representation of the sparse matrix.
        process_file(input_file_path, output_file_path, operation, other_matrix_file_path):
            Processes the input files, performs the specified operation, and writes the result to the output file.
    """
        
    def __init__(self):
        """
        Initializes a SparseMatrix object with zero rows, zero columns, and an empty dictionary for elements.
        """
        self.Rows = 0
        self.Colu = 0
        self.elements = {}

    def read_from_file(self, filePath):
        """
        Reads the sparse matrix from a file.
        
        Parameters
        ----------
        filePath : str
            The path to the input file.
        
        Raises
        ------
        ValueError
            If the input file has the wrong format.
        """
        self.elements = {}
        try:
            with open(filePath, 'r') as file:
                lines = file.readlines()
                self.Rows = int(lines[0].split('=')[1])
                self.Colu = int(lines[1].split('=')[1])
                for line in lines[2:]:
                    line = line.strip()
                    if line:
                        match = re.match(r'\((\d+),\s*(\d+),\s*(-?\d+)\)', line)
                        if match:
                            row, col, value = map(int, match.groups())
                            self.setElement(row, col, value)
                        else:
                            raise ValueError("Input file has wrong format")
        except Exception as e:
            raise ValueError("Input file has wrong format")

    def getElement(self, currRow, currCol):
        """
            Returns the element at the specified position.
            
            Parameters
            ----------
            currRow : int
                The row index.
            currCol : int
                The column index.
            
            Returns
            -------
            int
                The element value at the specified position.
        """
        return self.elements.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        """
            Sets the element at the specified position.
            
            Parameters
            ----------
            currRow : int
                The row index.
            currCol : int
                The column index.
            value : int
                The value to set at the specified position.
        """
        if value != 0:
            self.elements[(currRow, currCol)] = value
        elif (currRow, currCol) in self.elements:
            del self.elements[(currRow, currCol)]

    def add(self, other):
        """
            Adds two sparse matrices.
            
            Parameters
            ----------
            other : SparseMatrix
                The other sparse matrix to add.
            
            Returns
            -------
            SparseMatrix
                The result of the addition.
            
            Raises
            ------
            ValueError
                If the dimensions of the matrices do not match.
        """
        if self.Rows != other.Rows or self.Colu != other.Colu:
            raise ValueError("Matrices dimensions do not match for addition")
        result = SparseMatrix()
        result.Rows = self.Rows
        result.Colu = self.Colu
        all_keys = set(self.elements.keys()).union(other.elements.keys())
        for key in all_keys:
            result.setElement(key[0], key[1], self.getElement(key[0], key[1]) + other.getElement(key[0], key[1]))
        return result

    def subtract(self, other):
        """
            Subtracts two sparse matrices.
            
            Parameters
            ----------
            other : SparseMatrix
                The other sparse matrix to subtract.
            
            Returns
            -------
            SparseMatrix
                The result of the subtraction.
            
            Raises
            ------
            ValueError
                If the dimensions of the matrices do not match.
        """
        if self.Rows != other.Rows or self.Colu != other.Colu:
            raise ValueError("Matrices dimensions do not match for subtraction")
        result = SparseMatrix()
        result.Rows = self.Rows
        result.Colu = self.Colu
        all_keys = set(self.elements.keys()).union(other.elements.keys())
        for key in all_keys:
            result.setElement(key[0], key[1], self.getElement(key[0], key[1]) - other.getElement(key[0], key[1]))
        return result

    def multiply(self, other):
        """
            Multiplies two sparse matrices.
            
            Parameters
            ----------
            other : SparseMatrix
                The other sparse matrix to multiply.
            
            Returns
            -------
            SparseMatrix
                The result of the multiplication.
            
            Raises
            ------
            ValueError
                If the number of columns of the first matrix does not match the number of rows of the second matrix.
        """
        if self.Colu != other.Rows:
            raise ValueError("Matrices dimensions do not match for multiplication")
        result = SparseMatrix()
        result.Rows = self.Rows
        result.Colu = other.Colu
        for (i, k) in self.elements.keys():
            for j in range(other.Colu):
                result.setElement(i, j, result.getElement(i, j) + self.getElement(i, k) * other.getElement(k, j))
        return result

    def __str__(self):
        """
            Returns the string representation of the sparse matrix.
            
            Returns
            -------
            str
                The string representation of the sparse matrix.
        """
        output = []
        for (i, j), value in self.elements.items():
            output.append(f"({i}, {j}, {value})")
        return '\n'.join(output)

    def process_file(self, input_file_path, output_file_path, operation, other_matrix_file_path):
        """
            Processes the input files, performs the specified operation, and writes the result to the output file.

            Parameters
            ----------
            input_file_path : str
                The path to the first input file.
            output_file_path : str
                The path to the output file.
            operation : str
                The operation to perform ('add', 'subtract', 'multiply').
            other_matrix_file_path : str
                The path to the second input file.
            
            Raises
            ------
            ValueError
                If an invalid operation is specified.
        """
        self.read_from_file(input_file_path)
        other_matrix = SparseMatrix()
        other_matrix.read_from_file(other_matrix_file_path)
        
        if operation == 'add':
            result = self.add(other_matrix)
        elif operation == 'subtract':
            result = self.subtract(other_matrix)
        elif operation == 'multiply':
            result = self.multiply(other_matrix)
        else:
            raise ValueError("Invalid operation")

        with open(output_file_path, 'w') as file:
            file.write(f"rows={result.Rows}\n")
            file.write(f"cols={result.Colu}\n")
            file.write(str(result))

if __name__ == "__main__":
    input_folder = "/Users/ghyghi/Documents/VS Code/DSA/hw02/sample_inputs"
    output_folder = "/Users/ghyghi/Documents/VS Code/DSA/hw02/sample_results"
    
    sparse_matrix_processor = SparseMatrix()

    for filename in os.listdir(input_folder):
        if filename.endswith("_1.txt"):
            matrix1_path = os.path.join(input_folder, filename)
            matrix2_path = os.path.join(input_folder, filename.replace("_2.txt", "_3.txt"))
            
            if not os.path.isfile(matrix2_path):
                print(f"Matrix file {matrix2_path} does not exist, skipping.")
                continue
            
            output_path_add = os.path.join(output_folder, f"{filename.replace('_1.txt', '')}_add_results.txt")
            output_path_subtract = os.path.join(output_folder, f"{filename.replace('_1.txt', '')}_subtract_results.txt")
            output_path_multiply = os.path.join(output_folder, f"{filename.replace('_1.txt', '')}_multiply_results.txt")

            # Process addition
            try:
                sparse_matrix_processor.process_file(matrix1_path, output_path_add, 'add', matrix2_path)
                print(f"Addition result written to {output_path_add}")
            except ValueError as e:
                print(f"Failed to add matrices for {filename}: {e}")

            # Process subtraction
            try:
                sparse_matrix_processor.process_file(matrix1_path, output_path_subtract, 'subtract', matrix2_path)
                print(f"Subtraction result written to {output_path_subtract}")
            except ValueError as e:
                print(f"Failed to subtract matrices for {filename}: {e}")

            # Process multiplication
            try:
                sparse_matrix_processor.process_file(matrix1_path, output_path_multiply, 'multiply', matrix2_path)
                print(f"Multiplication result written to {output_path_multiply}")
            except ValueError as e:
                print(f"Failed to multiply matrices for {filename}: {e}")
