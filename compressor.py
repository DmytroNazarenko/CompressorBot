
class Compressor:

    @staticmethod
    def compress_file(file_name, out_file_name):
        with open(file_name+".txt","r", encoding='utf-8') as file_read,\
                open(out_file_name+".txt","w",encoding='utf-8') as file_write:
            text = file_read.read()
            compressed_text, dictionary = Compressor.__encode(text)
            list, dict = Compressor.__list_convert(compressed_text, dictionary)
            file_write.write(dict + "$$ ")
            file_write.write(list)

    @staticmethod
    def compress_text(text):
        compressed_text, dictionary = Compressor.__encode(text)
        list, dict = Compressor.__list_convert(compressed_text, dictionary)
        return dict + "$$ " + list

    @staticmethod
    def decompress_file(in_file_name, out_file_name):
        with open(in_file_name+".txt", "r",encoding='utf-8') as file_read,\
                open(out_file_name+".txt", "w", encoding='utf-8') as file_write:
            input = file_read.read()
            dict = Compressor.__dict_create(input)
            text_to_ord = list(map(ord, input[len(dict)+3:]))
            decoded = Compressor.__decode(text_to_ord, dict)
            file_write.write(''.join(map(str,decoded)))

    @staticmethod
    def decompress_text(input):
        dict = Compressor.__dict_create(input)
        text_to_ord = list(map(ord, input[len(dict) + 3:]))
        decoded = Compressor.__decode(text_to_ord, dict)
        return ''.join(map(str, decoded))

    @staticmethod
    def __dict_create(text):
        dict = []
        for i in range(len(text)):
            if text[i] == '$' and text[i+1] == '$':
                if text[i+2] == '$':
                    dict.append('$')
                break
            dict.append(text[i])
        return dict

    @staticmethod
    def __list_convert(list, dict):
        result1 = ""
        for a in list:
            result1 += chr(a)
        result2 = ""
        for c in dict:
            result2 += str(c)
        return result1,result2

    @staticmethod
    def __encode(input_string):
        dictionary = []
        base_dict = []
        encoded_version = []
        for char in input_string:
            if char in dictionary:
                continue
            else:
                dictionary.append(char)
                base_dict.append(char)
        dictionary.sort()
        base_dict.sort()
        next = ""
        for char in input_string:
            word = next + char
            if word in dictionary:
                next = word
            else:
                next = word[-1]
                dictionary_word = word[0:-1]
                dictionary.append(word)
                encoded_version.append(dictionary.index(dictionary_word))
        encoded_version.append(dictionary.index(next))
        return encoded_version, base_dict

    @staticmethod
    def __decode(encoded_version, dictionary):
        decoded_version = []
        old = encoded_version[0]
        decoded_version.append(dictionary[old])
        s = ""
        c = ''
        for new_symbol in encoded_version[1:]:
            if new_symbol < len(dictionary):
                s = dictionary[new_symbol]
            else:
                s = dictionary[old]
                s += c
            decoded_version.append(s)
            c = s[0]
            dictionary.append(dictionary[old] + c)
            old = new_symbol
        return decoded_version


#Compressor.compress_file("compress_text", "compressed_text1")
# Compressor.decompress_file("compressed_text1", "my_text1")
#print(chr(34598))
# encodeLzw(input_string)
# decoded_version = decodeLzw(encoded_version)
# print("The encoded version of the given string is: ", encoded_version)
# print("The Decoded version of the encoded string is: ", decoded_version)
# print(dictionary)
