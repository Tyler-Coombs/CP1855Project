#module for writing and reading money.txt file

#import sys for terminating program
import sys
def exit_program():
    print("Terminating program.")
    sys.exit()
    
#function to read money file
def readMoney():
    money = []
    try:
        with open("money.txt") as file:
            for line in file:
                line = line.replace("\n", "")
                money.append(line)
            return money
    except FileNotFoundError:
        print("Could not find money file.")
        exit_program()
    except Exception as e:
        print(type(e), e)
        exit_program()

#function to write to money file
def writeMoney(money):
    try:
        with open("money.txt", "w") as file:
            for row in money:
                file.write(str(row) + "\n")
    except OSError as e:
        print(type(e), e)
        exit_program()
    except Exception as e:
        print(type(e), e)
        exit_program()
        

if __name__ == "__main__":
    main()
