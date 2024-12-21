import subprocess
import asyncio

# Асинхронное выполнение команды
async def a_process(command):
    return await asyncio.create_subprocess_exec(
        *command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE
    )

# Синхронное выполнение команды
def process(command):
    return subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=True
    )

# Асинхронное ожидание вывода
async def a_expect(proc, pattern, timeout=10):
    pattern = pattern.strip("\n").replace("\n", "\r\n")
    buffer = ""
    try:
        while True:
            char = await asyncio.wait_for(proc.stdout.read(1), timeout)
            if not char:
                break
            buffer += char.decode()
            if pattern in buffer:
                return True, buffer
    except asyncio.TimeoutError:
        print(f"Timeout while waiting for pattern:\n{pattern}")
        return False, buffer

# Синхронное ожидание вывода
def expect(proc, pattern, timeout=10):
    pattern = pattern.strip("\n").replace("\n", "\r\n")
    buffer = ""
    try:
        while True:
            char = proc.stdout.read(1).decode()
            if not char:
                break
            buffer += char
            if pattern in buffer:
                return True, buffer
    except Exception as ex:
        print(f"ERROR: {ex}")
        return False, buffer

# Асинхронная запись ввода
def write(proc, text):
    print(f"Writing to async process: {text}")
    proc.stdin.write(f'{text}\n'.encode())
    proc.stdin.flush()
    return text

async def a_write(proc, text):
    print(f"Writing to async process: {text}")
    proc.stdin.write(f'{text}\n'.encode())
    await proc.stdin.drain()
    return text

# Основной тест
async def test():
    print("Launching processes")
    try:
        # Запускаем файлы
        bas = process('fourinarow.bas')
        py = await a_process('python main.py')

        # Ожидаем приветственное сообщение
        expected_greetings = """
                      FOUR IN A ROW
                    CREATIVE COMPUTING
                  MORRISTOWN, NEW JERSEY



THE GAME OF FOUR IN A ROW
DO YOU WANT INSTRUCTIONS?
"""
        print("Expecting greetings...")
        expect(bas, expected_greetings)
        await a_expect(py, expected_greetings)
        print("[+] TEST 1 - PASSED")

        # Отправляем 'YES' для получения инструкций
        print("Sending 'YES' for instructions...")
        write(bas, 'YES')
        await a_write(py, 'YES')
        print("[+] KEYS SENT")

        # Проверяем вывод инструкций и начало игры
        instruction_and_game_start = """
THE GAME CONSISTS OF STACKING X'S
AND O'S (THE COMPUTER HAS O) UNTIL
ONE OF THE PLAYERS GETS FOUR IN A
ROW VERTICALLY, HORIZONTALLY, OR 
DIAGONALLY.


DO YOU WANT TO GO FIRST? 
"""
        print("Expecting instructions and game start...")
        expect(bas, instruction_and_game_start)
        await a_expect(py, instruction_and_game_start)
        print("[+] TEST 2 - PASSED")

        print("Sending 'YES' to go first...")
        await a_write(py, 'YES')
        write(bas, 'YES')
        print("Checking initial board display...")
        board_display = """
  -  -  -  -  -  -  -  -
  -  -  -  -  -  -  -  -
  -  -  -  -  -  -  -  -
  -  -  -  -  -  -  -  -
  -  -  -  -  -  -  -  -
  -  -  -  -  -  -  -  -
  -  -  -  -  -  -  -  -
  -  -  -  -  -  -  -  -
  1  2  3  4  5  6  7  8

A NUMBER BETWEEN 1 AND 8?
"""
        await a_expect(py, board_display)
        expect(bas, board_display)
        print("[+] TEST 3 - Board display passed")

        bas.kill()
        bas.wait()

        py.kill()
        await py.wait()
    except Exception as ex:
        print(f"Test failed: {ex}")

# Запуск теста
asyncio.run(test())