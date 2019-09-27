FILE_NAME = 'sample_file.txt'


def generate_file(num_items):
    with open(FILE_NAME, 'w') as f:
        for x in range(num_items):
            f.write("front{}\n".format(x))
            f.write("back{}\n\n".format(x))
    return FILE_NAME

if __name__ == "__main__":
    generate_file(20)
