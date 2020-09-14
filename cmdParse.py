import argparse

def commandline_parser():
    parser = argparse.ArgumentParser(description='RSA Implementation by Lior Ben Dayan and Bar Lanyado')

    parser.add_argument('--gen', action='store_true', help='Generate keys to local folder')
    parser.add_argument('--enc', action='store_true', help='Execute encryption')
    parser.add_argument('--dec', action='store_true', help='Execute decryption')

    parser.add_argument('-int', action='store', type=int,
                        help='an integer for the accumulator')
    parser.add_argument('-string', action='store', type=str,
                        help='a text for the accumulator')
    parser.add_argument('-inPath', action='store', type=str,
                        help='a text file path for input')

    parser.add_argument('--img', action='store_true', help='encrypt an image')
    parser.add_argument('--bin', action='store_true', help='encrypt af file as binary')

    parser.add_argument('-outPath',action='store', default=None, type=str,
                        help='a file path for output (Only for string/integer encryption/decryption)')

    args = parser.parse_args()

    inC = 0
    if args.gen: inC = inC + 1
    if args.dec: inC = inC + 1
    if args.enc: inC = inC + 1

    if inC != 1:
        print("\n***\nPlease specify --enc or --dec or --gen\n***\n\nexit from program...\n")
        exit(0)

    inC = 0
    if args.int: inC = inC + 1
    if args.string: inC = inC + 1
    if args.inPath: inC = inC + 1

    if inC != 1 and not args.gen:
        print("\n***\nPlease insert one input source and a value\n***\n\nexit from program...\n")
        exit(0)

    # Creating a dictionary of parameters return to main

    data = dict()
    if args.gen:
        data["command"] = "generate"
    elif args.enc:
        data["command"] = "encrypt"
    else:
        data["command"] = "decrypt"

    if args.bin and args.gen:
        print("\n***\nCannot enable --img and --bin flags together...\n***\n\nexit from program...\n")
        exit(0)

    if args.int:
        data["inType"] = "int"
        data["inValue"] = args.int
    elif args.string:
        data["inType"] = "string"
        data["inValue"] = args.string
    elif args.inPath:
        if args.img:
            data["inType"] = "img"
        elif args.bin:
            data["inType"] = "bin"
        else:
            data["inType"] = "file"
        data["inValue"] = args.inPath
    else:
        data["inValue"] = args.inPath

    data["outPath"] = args.outPath
    return data
