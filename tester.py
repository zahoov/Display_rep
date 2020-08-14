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



    def message_setup(self, dt):

        # Creates the CAN message --> arbitration_id = destination address
        try:
            self.toggle_msg = can.Message(arbitration_id=0xCFF41F2, data=self.msg_data)
        except AttributeError:
            bus_status = 0
        else:
            print('success')
            bus_status = 1

        while bus_status == 0:
            try:
                self.toggle_msg = can.Message(arbitration_id=0xCFF41F2, data=self.msg_data)
            except AttributeError:
                bus_status = 0
            else:
                bus_status = 1
            print(bus_status)

        # Sends the CAN message to whatever 'bus' was set to every period in seconds (0.25 = 250ms)
        try:
            if not isinstance(self.task, can.ModifiableCyclicTaskABC):
                print("This interface doesn't seem to support modification")
                self.task.stop()
                return
        except AttributeError:
            print('aw shit here we go again')
            pass