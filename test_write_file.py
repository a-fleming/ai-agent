from functions.write_file import write_file

if __name__ == "__main__":
    tests = [
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed")
    ]
    

    for test in tests:
        working_directory, file_name, content = test
        print(f"Result for '{file_name}' in '{working_directory}/':")
        result = write_file(working_directory, file_name, content)
        print(result)
        print("-" * 60)

