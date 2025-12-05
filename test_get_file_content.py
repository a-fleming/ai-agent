from functions.get_file_content import get_file_content

if __name__ == "__main__":
    tests = [
        ("calculator", "lorem.txt"),
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
        ("calculator", "pkg/does_not_exist.py")
    ]
    

    for test in tests:
        working_directory, file_name = test
        print(f"Result for '{file_name}' in '{working_directory}/':")
        result = get_file_content(working_directory, file_name)
        if file_name == "lorem.txt":
            print(f"Content length: {len(result)}")
            print(result[-51:]) # Print File truncated message
        else:
            print(result)
        print("-" * 60)

