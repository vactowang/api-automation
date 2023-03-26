import pytest

def main():
    
    # Run Pytest command
    pytest.main(['-s', '-v', '--capture=sys'])


if __name__ == '__main__':
    main()