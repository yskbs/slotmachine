import random


MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS =3


symbol_count={
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8
}
#below is a multipler to calculate reward
symbol_value={
    'A': 5,
    'B': 4,
    'C': 3,
    'D': 2
}


def check_winnings(columns, lines, bet,values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check: 
                break
        else:
            winnings += values[symbol]* bet
            winning_lines.append(line + 1)
    return winnings, winning_lines   


def get_slot_machine_spin(rows,cols, symbols):
    #all_symbol is a pool for every column to select from
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):#
            # add the symbol symbol_count times to the all_symbol list
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        # we use a copy of all_symbols. Once we pick a value, we need to remove it from the list so we can't choose that value again.
        # every column has the same pool all_symbols to select from;
        # writing current_symbols= all_symbol, current_symbols stores the same object as all_symbols, that means anything i do in current_symbols affect all_symbols, that's a reference, we want a copy

        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            # .remove would find the 1st instance of this value in the list and get rid of it
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

#can't test the above code till we're able to print it. All our columns are laid out as rows, need to transpose these rows;
def print_slot_machine(columns):
    #len(columns[0]) assumes we at least have one column, if there's no columns, it will crash; take the goal row as out loop and column as inner loop, read and write the columns and goal matrix horizontally;
    #using index to transpose
    for row in range(len(columns[0])):
        #for every row, loop through every column, and for every column, we only print the current row we're on
        for i, column in enumerate(columns):
            #only put the pipe operator here if we're  not printing the last column(need index to know whether it's the lsat column), don't want the pipe operator at the row end
            if i != len(columns) -1:
                #the default end is '\n' go to the next line,
                print(column[row],  end = ' | ')
            else:
                #print columns[row] and stay in the line
                print(column[row],end= '')
        
        #for every row, we need to go to the next line
        print()

def deposit():
    while True:
        amount = input('What would you ilke to deposit? $')
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print('Amount must be greater than 0.')
        else:
            print('Please enter a number.')
    return amount


def get_number_of_lines():
    while True:
            lines = input('Enter the number of lines to bet on (1-'+ str(MAX_LINES) +')?')
            if lines.isdigit():
                lines = int(lines)
                if 1 <= lines <= MAX_LINES:
                    break
                else:
                    print('Enter a valid number of lines.')
            else:
                print('Please enter a number.')
    return lines

def get_bet():
    while True:
        amount = input('What would you ilke to bet on each line? $')
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <=amount <= MAX_BET:
                break
            else:
                print(f'Amount must be between ${MIN_BET}-${MAX_BET}.')
        else:
            print('Please enter a number.')
    return amount


def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f'You do not have enough to bet that amount, your current balance is ${balance}')
        else:
            break

    print(f'You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}')
    print(balance,lines)
    #  below returns columns, but we call it slots
    slots = get_slot_machine_spin(ROWS,COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won {winnings}.")    
    # * unpacks the ones in winning_lines
    print(f'You won on', *winning_lines)
    return winnings - total_bet

def main():
    balance= deposit()
    while True:
        print(f'Current balance is ${balance}')
        answer = input('Press enter to play (q to quit). ')
        if answer == 'q':
            break
        balance += spin(balance)
    print(f'You left with ${balance}')


main()