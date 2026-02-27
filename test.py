total = 0

def add_to_total(value: int) -> None:
    global total
    total = total+ value

    print(total)

add_to_total(15)