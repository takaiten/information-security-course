#include "ripemd.hpp"

using namespace RIPEMD::helpers;

// Нелинейная побитовая функция F
uint32_t RIPEMD::helpers::F(uint32_t j, uint32_t x, uint32_t y, uint32_t z) {
    switch (j) {
        case 0 ... 15:
            return x ^ y ^ z;
        case 16 ... 31:
            return (x & y) | (~x & z);
        case 32 ... 47:
            return (x | ~y) ^ z;
        case 48 ... 63:
            return (x & z) | (y & ~z);
        case 64 ... 79:
            return x ^ (y | ~z);
        default:
            throw invalid_argument("Helpers::f: j must be in range from 0 to 70");
    }
}

// Добавляемые 16-ичные константы
uint32_t RIPEMD::helpers::K1(uint32_t j) {
    switch (j) {
        case 0 ... 15:
            return 0x00000000;
        case 16 ... 31:
            return 0x5A827999;
        case 32 ... 47:
            return 0x6ED9EBA1;
        case 48 ... 63:
            return 0x8F1BBCDC;
        case 64 ... 79:
            return 0xA953FD4E;
        default:
            throw invalid_argument("Helpers::K1: j must be in range from 0 to 70");
    }
}

// Добавляемые 16-ичные константы
uint32_t RIPEMD::helpers::K2(uint32_t j) {
    switch (j) {
        case 0 ... 15:
            return 0x50A28BE6;
        case 16 ... 31:
            return 0x5C4DD124;
        case 32 ... 47:
            return 0x6D703EF3;
        case 48 ... 63:
            return 0x7A6D76E9;
        case 64 ... 79:
            return 0x00000000;
        default:
            throw invalid_argument("Helpers::K2: j must be in range from 0 to 70");
    }
}

// Смена порядка бит
uint32_t RIPEMD::helpers::inv(uint32_t value) {
    uint32_t res = 0;

    res |= ((value >> 0) & 0xFF) << 24;
    res |= ((value >> 8) & 0xFF) << 16;
    res |= ((value >> 16) & 0xFF) << 8;
    res |= ((value >> 24) & 0xFF) << 0;

    return res;
}

// Преобразование 4-х байт в uint32_t
uint32_t RIPEMD::helpers::bytes_to_uint(char *bytes) {
    uint32_t res = 0;

    res |= ((uint32_t) bytes[3] << 24) & 0xFF000000;
    res |= ((uint32_t) bytes[2] << 16) & 0xFF0000;
    res |= ((uint32_t) bytes[1] << 8) & 0xFF00;
    res |= ((uint32_t) bytes[0] << 0) & 0xFF;

    return res;
}

// Считывание сообщения
void RIPEMD::RIPEMD_320::read_message(string str) { message = str; }

// Добавление дополнительных битов
void RIPEMD::RIPEMD_320::extension() {
    // Исходная длина сообщения в битах
    bitlen = message.size() * 8;

    // Добавляем в конец сообщения единичный бит
    message.push_back((uint8_t) 0x80);

    // До тех пор, пока длина сообщения не станет равной 448(mod 512),
    while ((message.size() * 8) % 512 != 448)
        // Заполняем сообщение нулями
        message.push_back(0);

    // Количество блоков для обработки
    blocks = (uint32_t) (message.size() / 64) + 1;
}

// Добавление исходной длины сообщения
void RIPEMD::RIPEMD_320::adding_length() {
    // X - массив массивов блоков по 64 байта(512 бит)
    X = new uint32_t *[blocks];

    for (uint32_t i = 0; i < blocks; i++) {
        X[i] = new uint32_t[16];

        // Если это не последний блок, то переносим преобразованное message в X
        // Если блок послений, то делаем то же самое, но оставляем 8 байт под bitlen
        for (uint32_t j = 0; j < (i == blocks - 1 ? 14 : 16); j++)
            X[i][j] = bytes_to_uint(&message[(j * 4) + 64 * i]);

        // Если это после дний блок
        if (i == blocks - 1) {
            // добавляются младшие 64 бита, взятые из побитового представления
            // REMOVED & 0xFFFFFFFF
            X[i][14] = bitlen;
            // исходной длина сообщения
            X[i][15] = bitlen >> 32;
        }
    }
}

// Инициализация буфера
void RIPEMD::RIPEMD_320::initialize_ripemd() {
    H0 = 0x67452301, H1 = 0xEFCDAB89, H2 = 0x98BADCFE, H3 = 0x10325476, H4 = 0xC3D2E1F0;
    H5 = 0x76543210, H6 = 0xFEDCBA98, H7 = 0x89ABCDEF, H8 = 0x01234567, H9 = 0x3C2D1E0F;
}

// Обработка сообщения в блоках
void RIPEMD::RIPEMD_320::message_processing() {
    uint32_t D[10] = {H0, H1, H2, H3, H4, H5, H6, H7, H8, H9};
    uint32_t T;

    // Цикл блоков сообщения
    for (uint32_t i = 0; i < blocks; i++) {
        uint32_t H[10] = {H0, H1, H2, H3, H4, H5, H6, H7, H8, H9};
//        A1 = H0, B1 = H1, C1 = H2, D1 = H3, E1 = H4;
//        A2 = H5, B2 = H6, C2 = H7, D2 = H8, E2 = H9;

        // Магия
        for (uint32_t j = 0; j < 80; j++) {
            T = rotl((H[0] + F(j, H[1], H[2], H[3]) + X[i][R1[j]] + K1(j)), S1[j]) + H[4];

            H[0] = H[4];
            H[4] = H[3];
            H[3] = rotl(H[2], 10);
            H[2] = H[1];
            H[1] = T;

            T = rotl((H[5] + F(79 - j, H[6], H[7], H[8]) + X[i][R2[j]] + K2(j)), S2[j]) + H[9];

            H[5] = H[9];
            H[9] = H[8];
            H[8] = rotl(H[7], 10);
            H[7] = H[6];
            H[6] = T;

#define swap(k)                     \
    {                               \
            T = H[(k)];             \
            H[(k)] = H[(k + 5)];    \
            H[(k + 5)] = T;         \
    }

            switch (j) {
                case 15: swap(1);
                    break;
                case 31: swap(3);
                    break;
                case 47: swap(0);
                    break;
                case 63: swap(2);
                    break;
                case 79: swap(4);
                    break;
                default:
                    break;
            }


            // Обновляем значения
            for (int k = 0; k < 10; k++) {
                D[k] += H[k];
            }
//        H0 = H0 + A1;
//        H1 = H1 + B1;
//        H2 = H2 + C1;
//        H3 = H3 + D1;
//        H4 = H4 + E1;
//        H5 = H5 + A2;
//        H6 = H6 + B2;
//        H7 = H7 + C2;
//        H8 = H8 + D2;
//        H9 = H9 + E2;
        }
    }

    // Освобождаем память
    for (uint32_t i = 0; i < blocks; i++)
        delete[] X[i];

    delete[] X;
}

// Алгоритм преобразования
std::string RIPEMD::RIPEMD_320::ripemd_320() {
    // Добавление дополнительных битов
    extension();
    // Добавление исходной длины сообщения
    adding_length();
    // Инициализация буфера
    initialize_ripemd();
    // Основной цикл
    message_processing();

    // Результат в виде хэш-сообщения
    result << hex << inv(H0) << inv(H1) << inv(H2) << inv(H3) << inv(H4)
           << inv(H5) << inv(H6) << inv(H7) << inv(H8) << inv(H9);

    return result.str();
}