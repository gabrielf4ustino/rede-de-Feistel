def generate_pa_pb():
    pa = []
    pb = []
    cont = 0
    for i in range(512):
        if cont == 256:
            cont = 0
        if cont % 2 == 0:
            pa.append(cont)
        else:
            pb.append(cont)
        cont += 1
    return pa, pb


def rotate(array, num):
    i = len(array)
    return array[i - num:i] + array[0:i - num]


# Generate key with rc4 algorithm
def rc4(key_rc4, cont):
    final_key = []
    pa, pb = generate_pa_pb()
    for i in range(cont):
        if i % 2 == 0:
            s = list(pa)
        else:
            s = list(pb)
        if i % 2 == 0 and i != 0:
            key_rc4 = rotate(key_rc4, 1)
        t = []
        for i in range(256):
            t.append(key_rc4[i % len(key_rc4)])
        j = 0
        for i in range(256):
            j = (j + s[i] + t[i]) % 256
            x = s[i]
            y = s[j]
            s[i] = y
            s[j] = x
        final_key.append(s)
    return final_key


# Does mono alpha replacement on two arrays
def sub_mono(one, two):
    to_return = list(one)
    for i in range(len(one)):
        aux = to_return[i]
        to_return[i] = two[aux]
    return to_return


# Xor two arrays bitwise
def x_or(one, two):
    to_return = []
    for i in range(len(one)):
        to_return.append(one[i] ^ two[i])
    return to_return


# Run the feistel algorithm
def feistel(block, cont, key_rc4):
    i = int(len(block) / 2)
    left = block[0:i]
    right = block[i:]
    for i in range(cont):
        aux = list(left)
        left = list(right)
        right = x_or(aux, sub_mono(right, key_rc4[i]))
    return right + left


# Read inputs and exec the functions
def main():
    initialized = False
    while True:
        input_line = input()
        input_line = input_line.split()
        if len(input_line) == 0:
            break
        if input_line[0] == 'I':
            rounds = int(input_line[1])
            input_line = list(map(int, input_line[2:]))
            if 8 <= input_line[0] <= 32:
                if len(input_line[1:]) == input_line[0]:
                    generated_key = rc4(input_line[1:], rounds)
                else:
                    print("ERRO! A quantidade de elementos da chave não corresponde com o parâmentro passado.")
                    break
            else:
                print("ERRO!")
                break
            initialized = True
        elif initialized and (input_line[0] == 'C' or input_line[0] == 'D'):
            key = generated_key
            if input_line[0] == 'D':
                key = generated_key[::-1]
            input_line = list(map(int, input_line[1:]))
            output = feistel(input_line, rounds, key)
            print('C ' + ' '.join(str(s) for s in output))


if __name__ == "__main__":
    main()
