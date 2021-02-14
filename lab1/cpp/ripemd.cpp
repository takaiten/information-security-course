#include "ripemd.hpp"

unsigned int RIPEMD_320::F(unsigned int j, unsigned int x, unsigned int y, unsigned int z)  //Нелинейная побитовая функция F
{
    if (j <= 15)
        return x ^ y^ z;
    else if (j <= 31)
        return (x & y) | (~x & z);
    else if (j <= 47)
        return (x | ~y) ^ z;
    else if (j <= 63)
        return (x & z) | (y & ~z);
    else if (j <= 79)
        return x ^ (y | ~z);
    else
        return 0;
}

unsigned int RIPEMD_320::K1(unsigned int j)                                                 //Добавляемые 16-ичные константы
{
    if (j <= 15)
        return 0x00000000;
    else if (j <= 31)
        return 0x5A827999;
    else if (j <= 47)
        return 0x6ED9EBA1;
    else if (j <= 63)
        return 0x8F1BBCDC;
    else if (j <= 79)
        return 0xA953FD4E;
    else
        return 0;
}

unsigned int RIPEMD_320::K2(unsigned int j)                                                 //Добавляемые 16-ичные константы
{
    if (j <= 15)
        return 0x50A28BE6;
    else if (j <= 31)
        return 0x5C4DD124;
    else if (j <= 47)
        return 0x6D703EF3;
    else if (j <= 63)
        return 0x7A6D76E9;
    else if (j <= 79)
        return 0x00000000;
    else
        return 0;
}

unsigned int RIPEMD_320::inv(unsigned int value)                                            //Смена порядка бит
{
    unsigned int res = 0;

    res |= ((value >> 0) & 0xFF) << 24;
    res |= ((value >> 8) & 0xFF) << 16;
    res |= ((value >> 16) & 0xFF) << 8;
    res |= ((value >> 24) & 0xFF) << 0;

    return res;
}

unsigned int RIPEMD_320::bytes_to_uint(char* bytes)                                         //Преобразование 4-х байт в unsigned int
{
    unsigned int res = 0;

    res |= ((unsigned int)bytes[3] << 24) & 0xFF000000;
    res |= ((unsigned int)bytes[2] << 16) & 0xFF0000;
    res |= ((unsigned int)bytes[1] << 8) & 0xFF00;
    res |= ((unsigned int)bytes[0] << 0) & 0xFF;

    return res;
}

void  RIPEMD_320::read_message(string str){ message = str; }                                // Считывание сообщения

void RIPEMD_320::extension()                                                                //Добавление дополнительных битов
{
    bitlen = message.size() * 8;                                                            //Исходная длина сообщения в битах

    message.push_back((unsigned char)0x80);                                              //Добавляем в конец сообщения единичный бит

    while ((message.size() * 8) % 512 != 448)                                               //До тех пор, пока длина сообщения не станет равной 448(mod 512),
        message.push_back(0);                                                               //Заполняем сообщение нулями

    blocks = (unsigned int)(message.size() / 64) + 1;                                       //Количество блоков для обработки
}

void RIPEMD_320::adding_length()                                                            //Добавление исходной длины сообщения
{
    X = new unsigned int*[blocks];                                                          //X - массив массивов блоков по 64 байта(512 бит)

    for (unsigned int i = 0; i < blocks; i++)
    {
        X[i] = new unsigned int[16];

        for (int j = 0; j < (i == blocks - 1 ? 14 : 16); j++)                               //Если это не последний блок, то переносим преобразованное message в X,
            X[i][j] = bytes_to_uint(&message[(j * 4) + 64 * i]);                      //Если блок послений, то делаем то же самое, но оставляем 8 байт под bitlen

        if (i == blocks - 1)                                                                //Если это последний блок
        {
            X[i][14] = bitlen & 0xFFFFFFFF;                                                 //добавляются младшие 64 бита, взятые из побитового представления
            X[i][15] = bitlen >> 32 & 0xFFFFFFFF;                                           //исходной длина сообщения
        }
    }
}

void RIPEMD_320::initialize_ripemd()                                                        //Инициализация буфера
{
    H0 = 0x67452301, H1 = 0xEFCDAB89, H2 = 0x98BADCFE, H3 = 0x10325476, H4 = 0xC3D2E1F0;
    H5 = 0x76543210, H6 = 0xFEDCBA98, H7 = 0x89ABCDEF, H8 = 0x01234567, H9 = 0x3C2D1E0F;
}

//Номера выбираемых из сообщения 32-битных слов

unsigned int R1[] = {   0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                        7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
                        3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
                        1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
                        4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13 };

unsigned int R2[] = {   5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
                        6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
                        15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
                        8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
                        12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11 };

//Количество бит, на которое будут осуществляться сдвиги

unsigned int S1[] = {   11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
                        7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
                        11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
                        11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
                        9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6 };

unsigned int S2[] = {   8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
                        9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
                        9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
                        15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
                        8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11 };

void RIPEMD_320::message_processing()                                                       //Обработка сообщения в блоках
{
    for (unsigned int i = 0; i < blocks; i++)                                               //Цикл блоков сообщения
    {
        A1 = H0, B1 = H1, C1 = H2, D1 = H3, E1 = H4;
        A2 = H5, B2 = H6, C2 = H7, D2 = H8, E2 = H9;

        //Магия
        for (unsigned int j = 0; j < 80; j++)
        {
            T = ROTATE_LEFT((A1 + F(j, B1, C1, D1) + X[i][R1[j]] + K1(j)), S1[j]) + E1;

            A1 = E1, E1 = D1, D1 = ROTATE_LEFT(C1, 10), C1 = B1, B1 = T;

            T = ROTATE_LEFT((A2 + F(79 - j, B2, C2, D2) + X[i][R2[j]] + K2(j)), S2[j]) + E2;

            A2 = E2, E2 = D2, D2 = ROTATE_LEFT(C2, 10), C2 = B2, B2 = T;

            if (j == 15) { T = B1; B1 = B2; B2 = T; }
            if (j == 31) { T = D1; D1 = D2; D2 = T; }
            if (j == 47) { T = A1; A1 = A2; A2 = T; }
            if (j == 63) { T = C1; C1 = C2; C2 = T; }
            if (j == 79) { T = E1; E1 = E2; E2 = T; }
        }

        H0 = H0 + A1; H1 = H1 + B1; H2 = H2 + C1; H3 = H3 + D1;                             //Обновляем значения
        H4 = H4 + E1; H5 = H5 + A2; H6 = H6 + B2; H7 = H7 + C2;
        H8 = H8 + D2; H9 = H9 + E2;
    }

    for (unsigned int i = 0; i < blocks; i++)
        delete [] X[i];                                                                     //Освобождаем память

    delete [] X;
}

string RIPEMD_320::ripemd_320()                                                             //Алгоритм преобразования
{
    extension();                                                                            //Добавление дополнительных битов
    adding_length();                                                                        //Добавление исходной длины сообщения
    initialize_ripemd();                                                                    //Инициализация буфера
    message_processing();                                                                   //Основной цикл

    result << hex << inv(H0) << inv(H1) << inv(H2) << inv(H3) << inv(H4)
                  << inv(H5) << inv(H6) << inv(H7) << inv(H8) << inv(H9);                   //Результат в виде хэш-сообщения

    return result.str();                                                                    //Возвращаем результат в виде хэш-сообщения
}