import random

async def print_board(board):
    for row in reversed(board):
        print(" ", "  ".join(row))
    print("  " + "  ".join(map(str, range(1, 9))))
    print()

async def check_winner(board, symbol):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(8):
        for col in range(8):
            if board[row][col] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                for step in range(1, 4):
                    r, c = row + dr * step, col + dc * step
                    if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == symbol:
                        count += 1
                    else:
                        break
                if count == 4:
                    return True
    return False

async def make_move(board, column, symbol):
    for row in range(8):
        if board[row][column] == "-":
            board[row][column] = symbol
            return row
    return -1

async def evaluate_position(board, row, col, symbol):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    score = 0

    for dr, dc in directions:
        count = 0
        blocked = 0
        for step in range(-3, 4):
            r, c = row + dr * step, col + dc * step
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == symbol:
                    count += 1
                elif board[r][c] != "-":
                    blocked += 1
            if count == 4:
                return float('inf')
        if blocked < 2:
            score += count ** 2

    return score

async def get_computer_move(board):
    best_move = None
    best_score = -float('inf')

    for col in range(8):
        row = await make_move(board, col, "O")
        if row == -1:
            continue

        score = await evaluate_position(board, row, col, "O")

        # Check opponent's responses
        for opponent_col in range(8):
            opponent_row = await make_move(board, opponent_col, "X")
            if opponent_row != -1:
                score -= await evaluate_position(board, opponent_row, opponent_col, "X")
                board[opponent_row][opponent_col] = "-"

        board[row][col] = "-"

        if score > best_score:
            best_score = score
            best_move = col

    return best_move if best_move is not None else random.randint(0, 7)

async def prompt(text):
    return input(text)

async def main():
    print("                      FOUR IN A ROW")
    print("                    CREATIVE COMPUTING")
    print("                  MORRISTOWN, NEW JERSEY")
    print()
    print()
    print()

    print("THE GAME OF FOUR IN A ROW")

    while True:
        instructions = (await prompt("DO YOU WANT INSTRUCTIONS? ")).strip()
        if instructions == "YES":
            print("THE GAME CONSISTS OF STACKING X'S")
            print("AND O'S (THE COMPUTER HAS O) UNTIL")
            print("ONE OF THE PLAYERS GETS FOUR IN A")
            print("ROW VERTICALLY, HORIZONTALLY, OR")
            print("DIAGONALLY.")
            print()
            print()
            break
        elif instructions == "NO":
            break
        else:
            print("YES OR NO")

    first_input = (await prompt("DO YOU WANT TO GO FIRST? ")).strip()

    first = True if first_input != "NO" else False

    board = [["-" for _ in range(8)] for _ in range(8)]

    while True:
        await print_board(board)
        if first:
            valid_move = False
            while not valid_move:
                try:
                    column = int(await prompt("A NUMBER BETWEEN 1 AND 8? ")) - 1
                    if 0 <= column < 8 and await make_move(board, column, "X") != -1:
                        valid_move = True
                    else:
                        print("ILLEGAL MOVE, TRY AGAIN.")
                except ValueError:
                    print("!NUMBER EXPECTED - RETRY INPUT LINE")  # Сообщаем об ошибке
                    print(f"? {column}")


            if await check_winner(board, "X"):
                await print_board(board)
                print("Y O U   W I N !!!")
                break
        else:
            column = await get_computer_move(board)
            await make_move(board, column, "O")
            print(f"COMPUTER PICKS COLUMN {column + 1}")

            if await check_winner(board, "O"):
                await print_board(board)
                print("C O M P U T E R   W I N S !!!")
                break

        if all(board[7][col] != "-" for col in range(8)):
            print("T I E   G A M E ...")
            break

        first = not first

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
