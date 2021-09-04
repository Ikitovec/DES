from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Progressbar, Style, Combobox
from tkinter import messagebox
import bitarray



def open_file():
    print("Загрузка из файла")
    filename = askopenfilename()
    if filename == "":
        return 0
    # Пытаемся открыть файл
    try:
        file = open(filename, "rb")
        inputText = file.read()
        file.close()
    except Exception as error:
        messagebox.showinfo('Ошибка при открытии файла', 'Не удалось открыть файл')
        return 0
    inputText = inputText.decode('ANSI')
    txt.delete(1.0, END)
    txt.insert(INSERT, inputText)
    print("Файл открыт")



def save_file():
    print("\nВыгрузка в файл\n")
    txt_original = txt2.get("1.0", 'end-1c')
    txt_2 = txt2.get(1.0, END)
    filename = asksaveasfilename()
    result = txt_original.encode('ANSI')

    try:
        file = open(filename, "wb")
        file.write(result)
        file.close()
        messagebox.showinfo('Выгрузка в файл', 'Данные успешно записаны!')
    except Exception as error:
        messagebox.showinfo('Ошибка при выгрузке в файл', 'Не удалось открыть файл, либо записать данные в файл')
        return 0


def open_txt_key():
    txt_key.delete(1.0, END)
    filename = askopenfilename()
    print(filename)
    with open(filename, "r", encoding='utf-8') as fin:
        for line in fin.readlines():
            txt_key.insert(INSERT, line)




def open_txt_posilka():
    txt_posilka.delete(1.0, END)
    filename = askopenfilename()
    with open(filename, "r", encoding='utf-8') as fin:
        for line in fin.readlines():
            txt_posilka.insert(INSERT, line)

def save_file_key():
    print("\nВыгрузка в файл\n")
    txt_original = txt_key.get("1.0", 'end-1c')
    filename = asksaveasfilename()
    #result = txt_original.encode('ANSI')

    try:
        file = open(filename, "w", encoding='utf-8')
        file.write(txt_original)
        file.close()
        messagebox.showinfo('Выгрузка в файл', 'Данные успешно записаны!')
    except Exception as error:
        messagebox.showinfo('Ошибка при выгрузке в файл', 'Не удалось открыть файл, либо записать данные в файл')
        return 0

def save_file_posilka():
    print("\nВыгрузка в файл\n")
    txt_original = txt_posilka.get("1.0", 'end-1c')
    filename = asksaveasfilename()
    # result = txt_original.encode('ANSI')

    try:
        file = open(filename, "w", encoding='utf-8')
        file.write(txt_original)
        file.close()
        messagebox.showinfo('Выгрузка в файл', 'Данные успешно записаны!')
    except Exception as error:
        messagebox.showinfo('Ошибка при выгрузке в файл', 'Не удалось открыть файл, либо записать данные в файл')
        return 0

def bin_to_8(letter):
    a=bin(letter)[2:]
    while len(a)<8:
        a='0'+a
    return a

def table_start_perestanovki(key_bit):
    table=[57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
           10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
           63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
           14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
    key=''

    for i in range(len(table)):
        key+=key_bit[table[i]]
    return key


def key_check(key_input):
    key=''
    if len(key_input)>7:
        key=key_input[:7]
    elif len(key_input)<7:
        i=0
        while len(key)<7:
            key+=key_input[i%len(key_input)]
            i+=1

    encoded_key = key.encode('ANSI')


    key_bits=''
    for i in range(len(key)):
        key_bits+=bin_to_8(encoded_key[i])

    key_added_bits=''
    count=0
    for i in range(len(key_bits)):
        key_added_bits+=key_bits[i]
        if key_bits[i]=='1':
            count+=1
        if (i+1)%7==0:
            if count%2==0:
                key_added_bits+='1'
            else:
                key_added_bits+='0'
            count=0
    return key_added_bits



def generation_round_keys(key_bits):
    table_sjatia=[14, 17, 11, 24, 1, 5, 3, 28,
                  15, 6, 21, 10, 23, 19, 12, 4,
                  26, 8, 16, 7, 27, 20, 13, 2,
                  41, 52, 31, 37, 47, 55, 30, 40,
                  51, 45, 33, 48, 44, 49, 39, 56,
                  34, 53, 46, 42, 50, 36, 29, 32]
    round_key=['']
    L=key_bits[:28]
    R=key_bits[28:]

    for i in range(16):
        if (i == 0) | (i == 1) | (i == 8) | (i == 15):
            sdvig_answer_left = L[2:28] + L[:2]
            sdvig_answer_right = R[2:28] + R[:2]

        else:
            sdvig_answer_left = L[1:28] + L[:1]
            sdvig_answer_right=R[1:28] + R[:1]

        L=sdvig_answer_left
        R=sdvig_answer_right

        answer=L+R

        answer_after_sjatia=''
        for j in range(0,len(table_sjatia)):
            answer_after_sjatia+=answer[table_sjatia[j]-1]
        round_key.append(answer_after_sjatia)


    round_key.pop(0)
    return round_key


def start_perestanovka_teksta(txt_original):
    table=[58, 50, 42, 34, 26, 18, 10, 2,
           60, 52, 44, 36, 28, 20, 12, 4,
           62, 54, 46, 38, 30, 22, 14, 6,
           64, 56, 48, 40, 32, 24, 16, 8,
           57, 49, 41, 33, 25, 17, 9, 1,
           59, 51, 43, 35, 27, 19, 11, 3,
           61, 53, 45, 37, 29, 21, 13, 5,
           63, 55, 47, 39, 31, 23, 15, 7]



    answer=''
    for i in range(len(txt_original)):
        answer+=txt_original[table[i]-1]
    return answer


def txt_shifr(txt_original,round_key):
    P_box_table = [32, 1, 2, 3, 4, 5,
                   4, 5, 6, 7, 8, 9,
                   8, 9, 10, 11, 12, 13,
                   12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21,
                   20, 21, 22, 23, 24, 25,
                   24, 25, 26, 27, 28, 29,
                   28, 29, 30, 31, 32, 1]

    p2_box_table=[16, 7, 20, 21, 29, 12, 28, 17,
                    1, 15, 23, 26, 5, 18, 31, 10,
                    2, 8, 24, 14, 32, 27, 3, 9,
                    19, 13, 30, 6, 22, 11, 4, 25]

    s_block_table=[[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        # S2
                   [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
        # S3
                   [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        # S4
                   [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
                       # S5
                   [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

                       # S6
                   [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

                       # S7
                   [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
                       # S8
                   [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]


    L=txt_original[0:32]
    R=txt_original[32:]
    for k in range(16):
        R_old=R
        txt_after_p_box=''
        for i in range(len(P_box_table)):
            txt_after_p_box+=R[P_box_table[i]-1]

        after_xor=bin(int(txt_after_p_box,2)^int(round_key[k],2))[2:]


        while len(after_xor)<48:
            after_xor='0'+after_xor



        after_s_block=''
        for i in range(len(after_xor)//6):
            temp=after_xor[i*6:i*6+6]

            temp_s=temp[0]+temp[5]
            #print(temp_s)
            temp_s_inside=temp[1:5]



            temp_after_s_block=bin(s_block_table[i][int(temp_s,2)][int(temp_s_inside,2)])[2:]
            while len(temp_after_s_block)<4:
                temp_after_s_block='0'+temp_after_s_block

            after_s_block+=temp_after_s_block

        after_p2_box=''
        for i in range(len(after_s_block)):
            after_p2_box+=after_s_block[p2_box_table[i]-1]

        final_xor=bin(int(after_p2_box,2)^int(L,2))[2:]

        while len(final_xor)<32:
            final_xor='0'+final_xor

        if k<15:
            R=final_xor
            L=R_old

        if k==15:
            L=final_xor
            R=R_old

    return L+R


def end_perestanovka_teksta(txt_original):
    table=[40, 8, 48, 16, 56, 24, 64, 32,
           39, 7, 47, 15, 55, 23, 63, 31,
           38, 6, 46, 14, 54, 22, 62, 30,
           37, 5, 45, 13, 53, 21, 61, 29,
           36, 4, 44, 12, 52, 20, 60, 28,
           35, 3, 43, 11, 51, 19, 59, 27,
           34, 2, 42, 10, 50, 18, 58, 26,
           33, 1, 41, 9, 49, 17, 57, 25]

    answer=''
    for i in range(len(txt_original)):
        answer+=txt_original[table[i]-1]
    return answer


def gamma_check(gamma):
    gamma_norm=''
    if len(gamma)>8:
        gamma_norm=gamma[:8]
    elif len(gamma)<8:
        i = 0
        while len(gamma_norm) < 8:
            gamma_norm += gamma[i % len(gamma)]
            i += 1
    elif len(gamma)==8:
        gamma_norm=gamma

    gamma_norm=gamma_norm.encode("ANSI")
    gamma_bits = ''
    for i in range(len(gamma_norm)):
        gamma_bits += bin_to_8(gamma_norm[i])
    return gamma_bits

def clicked():
    txt2.delete(1.0, END)
    total_code_result = ''
    txt_original = txt.get("1.0", 'end-1c')
    if len(txt_original)==0:
        messagebox.showinfo('Ошибка!', 'Шифруемый текст пуст!')
    added_symbols=0
    while len(txt_original) % 8 != 0:
        txt_original += 'a'
        added_symbols += 1

    txt_original = txt_original.encode('ANSI')

    s.configure("LabeledProgressbar", text="Готово", foreground='black',
                background='mediumseagreen')
    Progres_bar.configure(value=0)
    Progres_bar.update()

    if combo2.get()=='ECB — режим «электронной кодовой книги»':
        if combo.get() == 'Зашифровать':
            key_input = txt_key.get("1.0", 'end-1c')
            if len(key_input)==0:
                messagebox.showinfo('Ошибка!', 'Введите ключ!')
            # key_input='abc'
            # приводим в порядок сессионные ключ
            key = key_check(key_input)
            txt_key.delete(1.0, END)
            txt_key.insert(INSERT, str(added_symbols) + key_input)

            key_after_start_perestanovki = table_start_perestanovki(key)
            round_key = generation_round_keys(key_after_start_perestanovki)



            for l in range(len(txt_original)//8):

                txt_bits = ''
                for i in range(8):
                    txt_bits += bin_to_8(txt_original[l*8+i])
                txt_bits_current=txt_bits

                after_start_zamena=start_perestanovka_teksta(txt_bits_current)

                txt_after_shifr=txt_shifr(after_start_zamena,round_key)

                answer=end_perestanovka_teksta(txt_after_shifr)
                for o in range(8):
                    bit_tmp = bitarray.bitarray(answer[8 * o: 8 * o + 8])
                    coding_result = bit_tmp.tobytes()
                    total_code_result += coding_result.decode('ANSI')
                progress_check = (l / (len(txt_original) // 8)) * 100
                s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                Progres_bar.configure(value=progress_check)
                Progres_bar.update()
            txt2.insert(INSERT,total_code_result)

            s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
            Progres_bar.configure(value=100)
            Progres_bar.update()

        elif combo.get()=="Расшифровать":
            key_input = txt_key.get("1.0", 'end-1c')
            # key_input='abc'
            if len(key_input)==0:
                messagebox.showinfo('Ошибка!', 'Введите ключ!')

            added_symbols=int(key_input[0])
            key_input=key_input[1:]
            key = key_check(key_input)
            txt_key.delete(1.0, END)
            txt_key.insert(INSERT, str(added_symbols) + key_input)

            key_after_start_perestanovki = table_start_perestanovki(key)
            round_key = generation_round_keys(key_after_start_perestanovki)


            round_key=round_key[::-1]

            for l in range(len(txt_original)//8):

                txt_bits = ''
                for i in range(8):
                    txt_bits += bin_to_8(txt_original[l * 8 + i])
                txt_bits_current = txt_bits

                after_start_zamena=start_perestanovka_teksta(txt_bits_current)

                txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                answer = end_perestanovka_teksta(txt_after_shifr)
                for o in range(8):
                    bit_tmp = bitarray.bitarray(answer[8 * o: 8 * o + 8])
                    coding_result = bit_tmp.tobytes()
                    total_code_result += coding_result.decode('ANSI')

                progress_check = (l / (len(txt_original) // 8)) * 100
                s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                Progres_bar.configure(value=progress_check)
                Progres_bar.update()
            txt2.insert(INSERT,total_code_result[:len(total_code_result)-added_symbols])

            s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
            Progres_bar.configure(value=100)
            Progres_bar.update()


    elif combo2.get()=='CBC — режим сцепления блоков':
        if combo.get() == 'Зашифровать':
            gamma=txt_posilka.get("1.0", 'end-1c')
            if len(gamma)==0:
                messagebox.showinfo('Ошибка!', 'Введите синхропосылку!')
            else:
                gamma=gamma_check(gamma)


            # приводим в порядок сессионные ключ
            key_input = txt_key.get("1.0", 'end-1c')
            if len(key_input)==0:
                messagebox.showinfo('Ошибка!', 'Введите ключ!')
            else:
                # key_input='abc'
                key = key_check(key_input)
                txt_key.delete(1.0, END)
                txt_key.insert(INSERT, str(added_symbols) + key_input)
                key_after_start_perestanovki = table_start_perestanovki(key)
                round_key = generation_round_keys(key_after_start_perestanovki)

                txt_bits=''
                for i in range(8):
                    txt_bits += bin_to_8(txt_original[i])

                first_xor=bin(int(txt_bits,2)^int(gamma,2))[2:]

                while len(first_xor)<64:
                    first_xor='0'+first_xor


                #DES
                after_start_zamena = start_perestanovka_teksta(first_xor)
                txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                answer = end_perestanovka_teksta(txt_after_shifr)

                for o in range(8):
                    bit_tmp = bitarray.bitarray(answer[8 * o: 8 * o + 8])
                    coding_result = bit_tmp.tobytes()
                    total_code_result += coding_result.decode('ANSI')
                for l in range(1, len(txt_original) // 8):
                    txt_bits = ''
                    for i in range(8):
                        txt_bits += bin_to_8(txt_original[l * 8 + i])
                    xor=bin(int(answer,2)^int(txt_bits,2))[2:]

                    while len(xor) < 64:
                        xor = '0' + xor

                    after_start_zamena = start_perestanovka_teksta(xor)
                    txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                    answer = end_perestanovka_teksta(txt_after_shifr)
                    for o in range(8):
                        bit_tmp = bitarray.bitarray(answer[8 * o: 8 * o + 8])
                        coding_result = bit_tmp.tobytes()
                        total_code_result += coding_result.decode('ANSI')

                    progress_check = (l / (len(txt_original) // 8)) * 100
                    s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                    Progres_bar.configure(value=progress_check)
                    Progres_bar.update()
                txt2.insert(INSERT, total_code_result)
                s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                Progres_bar.configure(value=100)
                Progres_bar.update()

        elif combo.get()=="Расшифровать":
            gamma = txt_posilka.get("1.0", 'end-1c')
            if len(gamma)==0:
                messagebox.showinfo('Ошибка!', 'Введите синхропосылку!')
            else:
                gamma = gamma_check(gamma)

            key_input = txt_key.get("1.0", 'end-1c')
            if len(key_input)==0:
                messagebox.showinfo('Ошибка!', 'Введите ключ!')
            else:
                # key_input='abc'
                added_symbols = int(key_input[0])
                key_input = key_input[1:]
                key = key_check(key_input)
                txt_key.delete(1.0, END)
                txt_key.insert(INSERT, str(added_symbols) + key_input)

                key_after_start_perestanovki = table_start_perestanovki(key)
                round_key = generation_round_keys(key_after_start_perestanovki)
                round_key = round_key[::-1]


                txt_bits = ''
                for i in range(8):
                    txt_bits += bin_to_8(txt_original[i])

                after_start_zamena = start_perestanovka_teksta(txt_bits)
                txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                answer = end_perestanovka_teksta(txt_after_shifr)

                xor=bin(int(answer,2)^int(gamma,2))[2:]
                while len(xor)<64:
                    xor='0'+xor

                for o in range(8):
                    bit_tmp = bitarray.bitarray(xor[8 * o: 8 * o + 8])
                    coding_result = bit_tmp.tobytes()
                    total_code_result += coding_result.decode('ANSI')

                for l in range(1, len(txt_original) // 8):

                    txt_bits=''
                    txt_bits_old=''
                    for i in range(8):
                        txt_bits += bin_to_8(txt_original[l * 8 + i])
                        txt_bits_old+=bin_to_8(txt_original[(l-1) * 8 + i])

                    #DES
                    after_start_zamena = start_perestanovka_teksta(txt_bits)
                    txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                    answer = end_perestanovka_teksta(txt_after_shifr)

                    xor = bin(int(answer, 2) ^ int(txt_bits_old, 2))[2:]
                    while len(xor) < 64:
                        xor = '0' + xor

                    for o in range(8):
                        bit_tmp = bitarray.bitarray(xor[8 * o: 8 * o + 8])
                        coding_result = bit_tmp.tobytes()
                        total_code_result += coding_result.decode('ANSI')

                    progress_check = (l / (len(txt_original) // 8)) * 100
                    s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                    Progres_bar.configure(value=progress_check)
                    Progres_bar.update()

                txt2.insert(INSERT,total_code_result[:len(total_code_result)-added_symbols])

                s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                Progres_bar.configure(value=100)
                Progres_bar.update()

    elif combo2.get() == 'CFB — режим обратной связи по шифротексту':
        if combo.get() == 'Зашифровать':
            gamma = txt_posilka.get("1.0", 'end-1c')
            if len(gamma)==0:
                messagebox.showinfo('Ошибка!', 'Введите синхропосылку!')
            else:
                gamma = gamma_check(gamma)


            key_input = txt_key.get("1.0", 'end-1c')
            if len(key_input)==0:
                messagebox.showinfo('Ошибка!', 'Введите ключ!')
            else:
                # key_input='abc'
                # приводим в порядок сессионные ключ
                key = key_check(key_input)
                txt_key.delete(1.0, END)
                txt_key.insert(INSERT, str(added_symbols) + key_input)

                key_after_start_perestanovki = table_start_perestanovki(key)
                round_key = generation_round_keys(key_after_start_perestanovki)


                #DEs
                after_start_zamena = start_perestanovka_teksta(gamma)
                txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                answer = end_perestanovka_teksta(txt_after_shifr)

                txt_bits = ''
                for i in range(8):
                    txt_bits += bin_to_8(txt_original[i])

                xor=bin(int(answer, 2) ^ int(txt_bits, 2))[2:]
                while len(xor) < 64:
                    xor = '0' + xor
                for o in range(8):
                    bit_tmp = bitarray.bitarray(xor[8 * o: 8 * o + 8])
                    coding_result = bit_tmp.tobytes()
                    total_code_result += coding_result.decode('ANSI')

                for l in range(1, len(txt_original) // 8):
                    # DEs
                    after_start_zamena = start_perestanovka_teksta(xor)
                    txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                    answer = end_perestanovka_teksta(txt_after_shifr)

                    txt_bits = ''
                    for i in range(8):
                        txt_bits += bin_to_8(txt_original[l * 8 + i])

                    xor=bin(int(answer, 2) ^ int(txt_bits, 2))[2:]
                    while len(xor) < 64:
                        xor = '0' + xor

                    for o in range(8):
                        bit_tmp = bitarray.bitarray(xor[8 * o: 8 * o + 8])
                        coding_result = bit_tmp.tobytes()
                        total_code_result += coding_result.decode('ANSI')

                    progress_check = (l / (len(txt_original) // 8)) * 100
                    s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                    Progres_bar.configure(value=progress_check)
                    Progres_bar.update()
                txt2.insert(INSERT, total_code_result)

                s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                Progres_bar.configure(value=100)
                Progres_bar.update()

        elif combo.get()=='Расшифровать':
            gamma = txt_posilka.get("1.0", 'end-1c')
            if len(gamma)==0:
                messagebox.showinfo('Ошибка!', 'Введите синхропосылку!')
            else:
                gamma = gamma_check(gamma)

            key_input = txt_key.get("1.0", 'end-1c')
            if len(key_input)==0:
                messagebox.showinfo('Ошибка!', 'Введите ключ!')
            else:
                # key_input='abc'
                added_symbols = int(key_input[0])
                key_input = key_input[1:]
                key = key_check(key_input)
                #txt_key.delete(1.0, END)
                #txt_key.insert(INSERT, str(added_symbols) + key_input)

                key_after_start_perestanovki = table_start_perestanovki(key)
                round_key = generation_round_keys(key_after_start_perestanovki)


                #DES
                after_start_zamena = start_perestanovka_teksta(gamma)
                txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                answer = end_perestanovka_teksta(txt_after_shifr)

                txt_bits = ''
                for i in range(8):
                    txt_bits += bin_to_8(txt_original[i])

                xor = bin(int(answer, 2) ^ int(txt_bits, 2))[2:]
                while len(xor) < 64:
                    xor = '0' + xor

                for o in range(8):
                    bit_tmp = bitarray.bitarray(xor[8 * o: 8 * o + 8])
                    coding_result = bit_tmp.tobytes()
                    total_code_result += coding_result.decode('ANSI')

                for l in range(1, len(txt_original) // 8):
                    txt_bits = ''
                    txt_bits_old = ''
                    for i in range(8):
                        txt_bits += bin_to_8(txt_original[l * 8 + i])
                        txt_bits_old += bin_to_8(txt_original[(l - 1) * 8 + i])

                    after_start_zamena = start_perestanovka_teksta(txt_bits_old)
                    txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                    answer = end_perestanovka_teksta(txt_after_shifr)

                    xor = bin(int(answer, 2) ^ int(txt_bits, 2))[2:]
                    while len(xor) < 64:
                        xor = '0' + xor

                    for o in range(8):
                        bit_tmp = bitarray.bitarray(xor[8 * o: 8 * o + 8])
                        coding_result = bit_tmp.tobytes()
                        total_code_result += coding_result.decode('ANSI')

                    progress_check = (l / (len(txt_original) // 8)) * 100
                    s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                    Progres_bar.configure(value=progress_check)
                    Progres_bar.update()

                txt2.insert(INSERT, total_code_result[:len(total_code_result)-added_symbols])
                s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                Progres_bar.configure(value=100)
                Progres_bar.update()

    elif combo2.get()=='OFB — режим обратной связи по выходу':
        if combo.get() == 'Зашифровать':
            gamma = txt_posilka.get("1.0", 'end-1c')
            if len(gamma)==0:
                messagebox.showinfo('Ошибка!', 'Введите синхропосылку!')
            else:
                gamma = gamma_check(gamma)


            key_input = txt_key.get("1.0", 'end-1c')
            if len(key_input)==0:
                messagebox.showinfo('Ошибка!', 'Введите ключ!')
            else:
                # key_input='abc'
                # приводим в порядок сессионные ключ
                key = key_check(key_input)
                txt_key.delete(1.0, END)
                txt_key.insert(INSERT, str(added_symbols) + key_input)

                key_after_start_perestanovki = table_start_perestanovki(key)
                round_key = generation_round_keys(key_after_start_perestanovki)

                # DEs
                after_start_zamena = start_perestanovka_teksta(gamma)
                txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                answer = end_perestanovka_teksta(txt_after_shifr)

                txt_bits = ''
                for i in range(8):
                    txt_bits += bin_to_8(txt_original[i])

                xor = bin(int(answer, 2) ^ int(txt_bits, 2))[2:]
                while len(xor) < 64:
                    xor = '0' + xor
                for o in range(8):
                    bit_tmp = bitarray.bitarray(xor[8 * o: 8 * o + 8])
                    coding_result = bit_tmp.tobytes()
                    total_code_result += coding_result.decode('ANSI')


                for l in range(1, len(txt_original) // 8):
                    # DEs
                    after_start_zamena = start_perestanovka_teksta(answer)
                    txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                    answer = end_perestanovka_teksta(txt_after_shifr)

                    txt_bits = ''
                    for i in range(8):
                        txt_bits += bin_to_8(txt_original[l * 8 + i])

                    xor = bin(int(answer, 2) ^ int(txt_bits, 2))[2:]
                    while len(xor) < 64:
                        xor = '0' + xor
                    for o in range(8):
                        bit_tmp = bitarray.bitarray(xor[8 * o: 8 * o + 8])
                        coding_result = bit_tmp.tobytes()
                        total_code_result += coding_result.decode('ANSI')

                    progress_check = (l / (len(txt_original) // 8)) * 100
                    s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                    Progres_bar.configure(value=progress_check)
                    Progres_bar.update()

                txt2.insert(INSERT, total_code_result)
                s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                Progres_bar.configure(value=100)
                Progres_bar.update()

        elif combo.get() == 'Расшифровать':
            gamma = txt_posilka.get("1.0", 'end-1c')
            if len(gamma)==0:
                messagebox.showinfo('Ошибка!', 'Введите синхропосылку!')
            else:
                gamma = gamma_check(gamma)


            key_input = txt_key.get("1.0", 'end-1c')
            # key_input='abc'
            if len(key_input)==0:
                messagebox.showinfo('Ошибка!', 'Введите ключ!')
            else:
                added_symbols = int(key_input[0])
                key_input = key_input[1:]
                key = key_check(key_input)
                # txt_key.delete(1.0, END)
                # txt_key.insert(INSERT, str(added_symbols) + key_input)

                key_after_start_perestanovki = table_start_perestanovki(key)
                round_key = generation_round_keys(key_after_start_perestanovki)

                # DES
                after_start_zamena = start_perestanovka_teksta(gamma)
                txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                answer = end_perestanovka_teksta(txt_after_shifr)

                txt_bits = ''
                for i in range(8):
                    txt_bits += bin_to_8(txt_original[i])

                xor = bin(int(answer, 2) ^ int(txt_bits, 2))[2:]
                while len(xor) < 64:
                    xor = '0' + xor

                for o in range(8):
                    bit_tmp = bitarray.bitarray(xor[8 * o: 8 * o + 8])
                    coding_result = bit_tmp.tobytes()
                    total_code_result += coding_result.decode('ANSI')

                for l in range(1, len(txt_original) // 8):
                    # DEs
                    after_start_zamena = start_perestanovka_teksta(answer)
                    txt_after_shifr = txt_shifr(after_start_zamena, round_key)
                    answer = end_perestanovka_teksta(txt_after_shifr)

                    txt_bits = ''
                    for i in range(8):
                        txt_bits += bin_to_8(txt_original[l * 8 + i])

                    xor = bin(int(answer, 2) ^ int(txt_bits, 2))[2:]
                    while len(xor) < 64:
                        xor = '0' + xor
                    for o in range(8):
                        bit_tmp = bitarray.bitarray(xor[8 * o: 8 * o + 8])
                        coding_result = bit_tmp.tobytes()
                        total_code_result += coding_result.decode('ANSI')
                    progress_check = (l / (len(txt_original) // 8)) * 100
                    s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                    Progres_bar.configure(value=progress_check)
                    Progres_bar.update()

                txt2.insert(INSERT, total_code_result[:len(total_code_result) - added_symbols])
                s.configure("LabeledProgressbar", text="Готово", fg='black', bg='mediumseagreen')
                Progres_bar.configure(value=100)
                Progres_bar.update()



window = Tk()
window.title("DES")
window.geometry('1550x700')


lbl = Label(window, text="Ваше сообщение")
lbl.place(x=20,y=50)

txt=scrolledtext.ScrolledText(window, width=50, height=30)
txt.place(x=20, y=70)

lbl = Label(window, text="Расшифрованное сообщение:")
lbl.place(x=1100,y=50)

txt2=scrolledtext.ScrolledText(window, width=50, height=30)
txt2.place(x=1100, y=70)


lbl = Label(window, text="Ключ:")
lbl.place(x=500,y=230)
txt_key=scrolledtext.ScrolledText(window, width=50, height=5)
txt_key.place(x=500, y=250)


lbl = Label(window, text="Синхропосылка:")
lbl.place(x=500,y=350)
txt_posilka=scrolledtext.ScrolledText(window, width=50, height=5)
txt_posilka.place(x=500, y=370)

btn = Button(window, text="Открыть файл", command=open_file)
btn.place(x=180,y=565)
lbl = Label(window)

btn = Button(window, text="Сохранить в файл", command=save_file)
btn.place(x=1250,y=565)
lbl = Label(window)


combo = Combobox(window, width=30)
combo['values'] = ("Зашифровать", "Расшифровать")
combo.current(0)
combo.place(x=500, y=150)


combo2 = Combobox(window, width=50)
combo2['values'] = ("ECB — режим «электронной кодовой книги»", 'CBC — режим сцепления блоков',
                    'CFB — режим обратной связи по шифротексту', 'OFB — режим обратной связи по выходу')
combo2.current(0)
combo2.place(x=500, y=100)
btn = Button(window, text="Преобразовать", command=clicked)
btn.place(x=750,y=550)
lbl = Label(window)


btn = Button(window, text="Загрузить ключ", command=open_txt_key)
btn.place(x=950,y=250)
lbl = Label(window)

btn = Button(window, text="Сохранить ключ", command=save_file_key)
btn.place(x=950,y=300)
lbl = Label(window)



btn = Button(window, text="Загрузить синхропосылку", command=open_txt_posilka)
btn.place(x=925,y=380)
lbl = Label(window)

btn = Button(window, text="Сохранить синхропосылку", command=save_file_posilka)
btn.place(x=925,y=420)
lbl = Label(window)

s = Style(window)
s.layout("LabeledProgressbar", [('LabeledProgressbar.trough', {'children': [('LabeledProgressbar.pbar', {'side': 'left', 'sticky': 'ns'}), ("LabeledProgressbar.label", {"sticky": ""})], 'sticky': 'nswe'})])

# Сам виджет шкалы прогресса
Progres_bar = Progressbar(window, orient="horizontal", length=100, style="LabeledProgressbar")
Progres_bar.place(relx=0.36, rely=0.92, relwidth=0.281, relheight=0.03)

window.mainloop()