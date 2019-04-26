from mobility.infrastructure.uartSerial import UartSerial

if __name__ == "__main__":
    port = UartSerial()
    while True:
        text = input("enter text to send")
        port.send(text.encode())
        print(port.recv())
