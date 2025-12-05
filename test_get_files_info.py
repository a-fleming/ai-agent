from functions.get_files_info import get_files_info

if __name__ == "__main__":
    tests = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../")
    ]

    for test in tests:
        working_directory, directory = test
        print(f"Result for '{directory}' in '{working_directory}/':")
        result = get_files_info(working_directory, directory)
        print(result)
        print("-" * 60)

