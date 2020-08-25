
def main():

    arb_id = '0xCFF41F2'
    check = input('Enter the new destination ID:\n')

    front_mid = arb_id[2:5]
    rear = arb_id[7:9]
    no_caps = arb_id[0:2]
    new_id = (str(hex(int(check))))[2:]

    completed = no_caps + front_mid.upper() + new_id.upper() + rear.upper()

    print(completed)

    coolant_temp = (enforceMaxV(((int(msg[0:2], 16))), 250) * 1.0) - 40.0  # Unit = °C


if __name__ == '__main__':
    main()


