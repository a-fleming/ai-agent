from functions.run_python_file import run_python_file

if __name__ == "__main__":
    tests = [
        ("calculator", "main.py"),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py"),
        ("calculator", "../main.py"),
        ("calculator", "nonexistent.py"),
        ("calculator", "lorem.txt")
    ]
    

    for test in tests:
        working_directory = test[0]
        file_name = test[1]
        args = []
        if len(test) == 3:
            args = test[2]
        print(f"Result for '{file_name}' in '{working_directory}/' with args '{args}':")
        result = run_python_file(working_directory, file_name, args)
        print(result)
        print("-" * 60)