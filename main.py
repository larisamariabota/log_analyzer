from loader import load_file

if __name__ == "__main__":
    entries = load_file("test_logs/mixed_50.log")

    for e in entries:
        print("="*60)
        for key, value in e.items():
            print(f"{key:12}: {value}")



 