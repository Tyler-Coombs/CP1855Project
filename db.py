#module for writing and reading money.txt file

#function to read money file
def readMoney():
    try:
        with open("money.txt") as file:
            money = file.read()
        return float(money)
    except FileNotFoundError:
        print("Could not find money file.")
        exit_program()
    except Exception as e:
        print(type(e), e)
        exit_program()

#function to write to money file
def writeMoney():
    with open("money.txt", "w") as file:
        file.write(money)

if __name__ == "__main__":
    main()
