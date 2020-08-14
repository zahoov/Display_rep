import can


def main():
    arb_id = '0xCFF41F2'

    source_id = int(arb_id[7:9], 16)

    arb_id = int(arb_id, 16)

    wo_source = arb_id - source_id

    try:
        source_id = int(input('Input the new source address:\n'), 16)
    except ValueError:
        print("You dingus you didn't input anything")

    arb_id = wo_source + source_id


if __name__ == '__main__':
    main()
