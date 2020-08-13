import can


def main():


    # Creates the CAN message --> arbitration_id = destination address
    #toggle_msg = can.Message()
    bus = can.interface.Bus()

    print(type(bus))
    #print(bus)


    pass





if __name__ == '__main__':
    main()