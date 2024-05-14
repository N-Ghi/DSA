import os
import time

class UniqueInt:
    
    def __init__(self):
        self.seen = [False] * 2047  # Boolean array for integers from -1023 to 1023
        self.min_int = -1023

    def process_file(self, input_file_path, output_file_path):
        # Reset seen array for each file
        self.seen = [False] * 2047
        unique_numbers = self.read_unique_integers(input_file_path)
        self.write_unique_integers(unique_numbers, output_file_path)

    def read_unique_integers(self, input_file_path):
        unique_numbers = []
        with open(input_file_path, 'r') as input_file:
            for line in input_file:
                stripped_line = line.strip()
                if stripped_line:
                    if self.is_valid_integer_line(stripped_line):
                        number = int(stripped_line)
                        if -1023 <= number <= 1023:  # Ensure the number is within range
                            if not self.seen[number - self.min_int]:
                                self.seen[number - self.min_int] = True
                                unique_numbers.append(number)
                        else:
                            print(f"Number out of range: {number}")
        return self.sort_unique_numbers(unique_numbers)

    def is_valid_integer_line(self, line):
        try:
            int(line)
            return True
        except ValueError:
            print(f"Invalid integer line: {line}")
            return False

    def sort_unique_numbers(self, numbers):
        if not numbers:
            return numbers
        
        # Implementing Bubble Sort for simplicity
        n = len(numbers)
        for i in range(n):
            for j in range(0, n-i-1):
                if numbers[j] > numbers[j+1]:
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
        return numbers

    def write_unique_integers(self, unique_numbers, output_file_path):
        with open(output_file_path, 'w') as output_file:
            for number in unique_numbers:
                output_file.write(f"{number}\n")

if __name__ == "__main__":
    input_folder = "/Users/ghyghi/Documents/VS Code/dsa/hw01/sample_inputs"
    output_folder = "/Users/ghyghi/Documents/VS Code/dsa/hw01/sample_results"
    
    unique_int_processor = UniqueInt()

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{filename}_results.txt")

            # Timing for each file
            start_time = time.time()
            unique_int_processor.process_file(input_path, output_path)
            end_time = time.time()

            print(f"Processed {filename} in {end_time - start_time:.4f} seconds")
