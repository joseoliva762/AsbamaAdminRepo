from Apps.WiegandEngine import WiegandEngine


if __name__ == '__main__':
    w26 = WiegandEngine()
    while True:
        w26.read_card()