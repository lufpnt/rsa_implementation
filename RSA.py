from cmdParse import commandline_parser as cmd
from cyptoRSA import *


def fileOutput(path, value, append=False):
    # Output of string to file
    fo = open(path, 'w')
    fo.write(value)
    fo.close()
    print("Finished successfully ! \n\nThe result written to:\n" + path)


def fileOutputBin(path, value):
    # Output of binary file
    fo = open(path, 'wb')
    fo.write(value)
    fo.close()
    print("Finished successfully ! \n\nThe result written to:\n" + path)


def fileOutputTensor(path, value):
    # Output of tesnor to file
    fo = open(path, 'wb')
    np.save(fo, value)
    fo.close()
    print("Finished successfully ! \n\nThe result written to:\n" + path)


def readImageToTensor(imgPath):
    # Read tensor from image file
    img = cv2.imread(imgPath)
    return img


def main():

    # Parsing command line tools by using commandline_parser() function from cmdParse.py

    args = cmd()
    if args["command"] == "generate":
        # Keys generation. Checks if the size is correct and calls to gen_keys() function
        global key_sizes
        length = 0
        while length not in key_sizes:
            length = int(input('Please enter the keys length: (128/256/512/1024/2048/4096)'))
        gen_keys(length)

    init_chunk_size()
    if args["command"] == "encrypt":
        if args["inType"] == "string":
            # Text encryption.
            cipher = encrypt_text(args["inValue"])
        elif args["inType"] == "int":
            # Integer encryption.
            cipher = encrypt_integer(args["inValue"])
        elif args["inType"] == "file":
            # Text file encryption.
            msg = open(args["inValue"], 'r').read()
            cipher = encrypt_text(msg)
        elif args["inType"] == "bin":
            # Binary file encryption.
            msg = open(args["inValue"], 'rb').read()
            cipher = encrypt_bin(msg)
        elif args["inType"] == "img":
            # Image tensor encryption.
            img = readImageToTensor(args["inValue"])
            cipher = encrypt_tensor(img)

        if args["outPath"] is not None:
            # If output file is supplied by user
            if args["inType"] == "bin":
                # Binary output.
                fileOutput(args["outPath"], cipher)
            elif args["inType"] == "img":
                # Numpy tensor output.
                fileOutputTensor(args["outPath"], cipher)
            else:
                # Text file output.
                fileOutput(args["outPath"], cipher)
        elif args["inType"] != "img" and args["outPath"] is None:
            # Output to screen.
            print("Finished successfully ! \n\nThe result:\n\n" + str(cipher))

    elif args["command"] == "decrypt":
        if args["inType"] == "string":
            # String decryption.
            msg = decrypt_text(args["inValue"])
        elif args["inType"] == "int":
            # Integer decryption
            msg = decrypt_integer(args["inValue"])
        elif args["inType"] == "file":
            # Text file decryption
            cipher = open(args["inValue"], 'r').read()
            msg = decrypt_text(cipher)
        elif args["inType"] == "bin":
            # Binary file decryption
            cipher = open(args["inValue"], 'r').read()
            msg = decrypt_bin(cipher)
        elif args["inType"] == "img":
            # Numpy tensor file decryption
            cipher = open(args["inValue"], 'rb')
            tensor = np.load(cipher, allow_pickle=True)
            msg = decrypt_tensor(tensor)

        if args["outPath"] is not None:
            # If output file is supplied by user
            if args["inType"] == "bin":
                # Binary output.
                fileOutputBin(args["outPath"], msg)
            else:
                # Text file output.
                fileOutput(args["outPath"], msg)
        else:
            # Screen output.
            print("Finished successfully ! \n\nThe result:\n\n" + str(msg))


if __name__ == '__main__':
    main()
