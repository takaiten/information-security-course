#include "ripemd.hpp"
#include <cstring>

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
uint32_t RIPEMD::helpers::bytes_to_uint(const char *bytes) {
    uint32_t res = 0;

    res |= ((uint32_t) bytes[3] << 24) & 0xFF000000;
    res |= ((uint32_t) bytes[2] << 16) & 0xFF0000;
    res |= ((uint32_t) bytes[1] << 8) & 0xFF00;
    res |= ((uint32_t) bytes[0] << 0) & 0xFF;

    return res;
}

// Добавляет дополнительных битов
void RIPEMD::RIPEMD_320::add_additional_bits(string &message) {
    // Добавляем в конец сообщения единичный бит
    message.push_back((uint8_t) 0x80);

    // До тех пор, пока длина сообщения не станет равной 448(mod 512),
    while ((message.size() * 8) % 512 != 448)
        // Заполняем сообщение нулями
        message.push_back(0);
}

// Добавление исходной длины сообщения
uint32_t **RIPEMD::RIPEMD_320::generate_blocks_array(uint32_t blocks, uint64_t bitlen, string &message) {
    // X - массив массивов блоков по 64 байта(512 бит)
    auto **X = new uint32_t *[blocks];

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
    return X;
}

// Инициализация буфера
uint32_t *RIPEMD::RIPEMD_320::get_initial_hashes() {
    static uint32_t initial_hash[N] = {0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0,
                                       0x76543210, 0xFEDCBA98, 0x89ABCDEF, 0x01234567, 0x3C2D1E0F};
    return initial_hash;
}

// Обработка сообщения в блоках
uint32_t *RIPEMD::RIPEMD_320::generate_hashes(uint32_t blocks, uint32_t **bit_msg) {
    static uint32_t *hashes = get_initial_hashes();

    // Цикл блоков сообщения
    for (uint32_t i = 0, T; i < blocks; i++) {
        uint32_t H[N] = {0};
        memcpy(H, hashes, N * sizeof(uint32_t));

        // Магия
        for (uint32_t j = 0; j < 80; j++) {
            T = rotl((H[0] + F(j, H[1], H[2], H[3]) + bit_msg[i][R1[j]] + K1(j)), S1[j]) + H[4];

            H[0] = H[4], H[4] = H[3], H[3] = rotl(H[2], N), H[2] = H[1], H[1] = T;

            T = rotl((H[5] + F(79 - j, H[6], H[7], H[8]) + bit_msg[i][R2[j]] + K2(j)), S2[j]) + H[9];

            H[5] = H[9], H[9] = H[8], H[8] = rotl(H[7], N), H[7] = H[6], H[6] = T;

#define swap(k)                     \
    {                               \
            T = H[(k)];             \
            H[(k)] = H[(k + 5)];    \
            H[(k + 5)] = T;         \
    }

            switch (j) {
                case 15: swap(1); break;
                case 31: swap(3); break;
                case 47: swap(0); break;
                case 63: swap(2); break;
                case 79: swap(4); break;
                default: break;
            }
        }
        // Обновляем значения
        for (int k = 0; k < N; k++) {
            hashes[k] += H[k];
        }
    }

    // Освобождаем память
    for (uint32_t i = 0; i < blocks; i++)
        delete[] bit_msg[i];

    delete[] bit_msg;

    return hashes;
}

// Алгоритм преобразования
std::string RIPEMD::RIPEMD_320::ripemd_320(string message) {
    // Размер сообщения в битах
    uint64_t bitlen = message.size() * 8;

    // Добавление дополнительных битов
    add_additional_bits(message);

    // Количество блоков для обработки
    uint32_t blocks = (uint32_t) (message.size() / 64) + 1;

    // Добавление исходной длины сообщения
    uint32_t **bit_msg = generate_blocks_array(blocks, bitlen, message);

    // Основной цикл
    uint32_t *hashes = generate_hashes(blocks, bit_msg);

    // Результат в виде хэш-сообщения
    ostringstream result;

    result << hex;
    for (size_t i = 0; i < N; i++) {
        result << inv(hashes[i]);
    }

    return result.str();
}