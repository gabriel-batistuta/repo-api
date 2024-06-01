import magic

def get_file_type(file_path):
    file_magic = magic.Magic()
    file_type = file_magic.from_file(file_path)
    return file_type

if __name__ == '__main__':
    file_path = 'example.txt'
    file_type = get_file_type('.txt')
    print(f"O tipo de arquivo é: {file_type}")