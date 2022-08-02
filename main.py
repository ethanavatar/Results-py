from results import Result

def main():
    res = Result.Err(1)
    print(res.unwrap())

if __name__ == '__main__':
    main()