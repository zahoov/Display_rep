
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


BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            size: root.width, root.height * 0.2

            Label:
                text: app.error_base
                background_color: 0, 0, 0, 0
                size_hint_x: 0.25
                color: 1, 0, 0, 1
                font_size: ((self.parent.width + self.parent.height) / 2) * 0.1
                #on_press: app.root.current = 'fourth'

            Label:
        	    id: gauge_title
        	    size_hint_x: 0.5
			    text: 'H2 Injection'
			    text_size: self.size
			    color: 1, 1, 1, 1
			    font_size: ((root.width + root.height) / 2) * 0.1
                size: self.texture_size
                bold: True

			Label:
			    id: hMode
			    canvas.before:
                    Color:
                        rgba: 0, 0, 0, 1
                    Line:
                        width: 5
                        rectangle: self.x, self.y, self.width, self.height
			    text: app.engine_mode
			    size_hint_x: 0.25
			    font_size: ((self.parent.width + self.parent.height) / 2) * 0.1
			    color: app.mode_color