import can


def main():
    max = 2 ** 29

    #print('That was too large a number. The max input is: ' + str(max - 255))
    arb_id = '0xCFF4124'
    print(max)
    token = input('Enter:\n')

    print(hex(int(token)))




    source_id = str(arb_id)[0:7]


    print(source_id)

    arb_id = source_id + str(hex(int(token)))[2:]

    print(arb_id)



if __name__ == '__main__':
    main()
