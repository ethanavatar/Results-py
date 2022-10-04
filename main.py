from results import Result, Ok, Err

def main():
    res = Err(1)
    print(res.unwrap())

if __name__ == '__main__':
    main()