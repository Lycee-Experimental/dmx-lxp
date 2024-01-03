class Pin:
    def __init__(self) -> None:
        self.value = 0
        self.postion = 0
    def update(self, value):
        self.value = value
        self.postion = value

class Board:
    def __init__(self) -> None:
        self.GP0 = Pin()
        self.D0 = Pin()
        self.D1 = Pin()
        self.D2 = Pin()
        self.D3 = Pin()
        self.D4 = Pin()
        self.D5 = Pin()
        self.D6 = Pin()
        self.D7 = Pin()
        self.D8 = Pin()
        self.D9 = Pin()
        self.D10 = Pin()
        self.D11 = Pin()
        self.D12 = Pin()
        self.D13 = Pin()
        self.A0 = Pin()
        self.A1 = Pin()
        self.A2 = Pin()
        self.A3 = Pin()
        self.A4 = Pin()
        self.A5 = Pin()

        self.js_speed = 2500
    def update(self, type, count):
        match type:
            case "slider":
                self.update_dim_slider(count)
            case "js_x":
                self.update_js_x(count)
            case "js_y":
                self.update_js_y(count)
                
    
    def update_js_x(self, count):
        """Fait passer periodiquement A1 de self.js_speed à -self.js_speed"""
        if count%20<10:
            self.A1.update(self.js_speed)
        else:
            self.A1.update(0-self.js_speed)

    def update_js_y(self, count):
        """Fait passer periodiquement A2 de self.js_speed à -self.js_speed"""
        if count%20<10:
            self.A2.update(self.js_speed)
        else:
            self.A2.update(0-self.js_speed)
    
    # FIXME
    def update_dim_slider(self, count):
        if count%20<10:
            self.D9.update(self.A1.value+100)
        else:
            self.D9.update(self.A1.value-100)