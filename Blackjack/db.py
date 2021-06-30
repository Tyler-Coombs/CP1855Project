#module for writing and reading money.txt file

#function to read money file
def readMoney():
    with open ("money.txt") as file:
        for line in file:
            line = line.strip("\n")
            moneyAmount.append(line)
        return moneyAmount

#function to write to money file
def writeMoney():
    with open ("money.txt", "w") as file:
        for money in moneyAmount:
            file.write(money + "\n")

if __name__ == "__main__":
    main()
