#include <sstream>
#include <string.h>
#include <bitset>
#include <vector>
#include <tuple>

#include "ripemd.hpp"
#include "helpers.hpp"
#include "const.hpp"

const uint32_t N = 10;

#define ROTL(x, n) (((x) << (n)) | ((x) >> (32-(n))))

// Добавляет дополнительных битов
void methods::add_additional_bits(std::string &message) {
    // Добавляем в конец сообщения единичный бит
    message.push_back((uint8_t) 0x80);

    // До тех пор, пока длина сообщения не станет равной 448(mod 512),
    while ((message.size() * 8) % 512 != 448)
        // Заполняем сообщение нулями
        message.push_back(0);
}

// Добавление исходной длины сообщения
uint32_t **methods::generate_blocks_array(uint32_t blocks_count, uint64_t bitlen, std::string &message) {
    // X - массив массивов блоков по 64 байта(512 бит)
    auto **X = new uint32_t *[blocks_count];

    for (uint32_t i = 0; i < blocks_count; i++) {
        X[i] = new uint32_t[16];

        // Если это не последний блок, то переносим преобразованное message в X
        // Если блок послений, то делаем то же самое, но оставляем 8 байт под bitlen
        for (uint32_t j = 0; j < (i == blocks_count - 1 ? 14 : 16); j++)
            X[i][j] = bytes_to_uint(&message[(j * 4) + 64 * i]);

        // Если это после дний блок
        if (i == blocks_count - 1) {
            // добавляются младшие 64 бита, взятые из побитового представления
            // REMOVED & 0xFFFFFFFF
            X[i][14] = bitlen;
            // исходной длина сообщения
            X[i][15] = bitlen >> 32;
        }
    }
    return X;
}

void methods::change_bit(uint32_t **blocks, uint64_t bit_pos) {
    // индекс строки
    uint32_t row = bit_pos >> 9;

    // индекс бита в строке
    uint32_t bit_index_in_row = bit_pos % 512;

    // индекс uint32_t (4 байта) в blocks[row]
    uint32_t column = bit_index_in_row >> 5;

    // индекс бита в blocks[row][column]
    uint32_t bit_index_in_4bytes = bit_index_in_row % 32;

    // blocks[row][column] xor pow(2, 31 - bit_index_in_4bytes)
    blocks[row][column] ^= 1 << (31 - bit_index_in_4bytes);

    /* пример для 8 бит:
     * p = 1111 1111, нужно поменять 2-й слева бит (отсчет с нуля)
     * делаем xor с числом a == 0010 0000
     * a == 1 << (7 - 2) == 1 << 5 == 0000 0001 << 5 == 0010 0000
     * p xor a == 1101 1111
     * => поменяли ровно 2-й слева бит */
}

// Обработка сообщения в блоках
std::pair<uint32_t*, std::vector<uint32_t>> methods::generate_hashes(uint32_t blocks_count, uint32_t **blocks) {
    // Инициализация буфера
    static uint32_t hashes[N] = {0};
    memcpy(hashes, initial_hashes, N * sizeof(uint32_t));
    std::vector<uint32_t> changed_bits_count(80 * blocks_count, 0);

    // Цикл блоков сообщения
    for (uint32_t i = 0, T; i < blocks_count; i++) {
        uint32_t H[N] = {0};
        memcpy(H, hashes, N * sizeof(uint32_t));

        // Магия
        for (uint32_t j = 0; j < 80; j++) {
            uint32_t H_before[N] = {0};
            memcpy(H_before, H, N * sizeof(uint32_t));

            T = ROTL((H[0] + F(j, H[1], H[2], H[3]) + blocks[i][R1[j]] + K1(j)), S1[j]) + H[4];

            H[0] = H[4], H[4] = H[3], H[3] = ROTL(H[2], N), H[2] = H[1], H[1] = T;

            T = ROTL((H[5] + F(79 - j, H[6], H[7], H[8]) + blocks[i][R2[j]] + K2(j)), S2[j]) + H[9];

            H[5] = H[9], H[9] = H[8], H[8] = ROTL(H[7], N), H[7] = H[6], H[6] = T;

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

            for (int k = 0; k < N; k++) {
                std::bitset<32> before(H_before[k]);
                std::bitset<32> after(H[k]);

                changed_bits_count[i * blocks_count + j] += (before ^ after).count();
            }
        }
        // Обновляем значения
        for (int k = 0; k < N; k++) {
            hashes[k] += H[k];
        }
    }

    // Освобождаем память
    for (uint32_t i = 0; i < blocks_count; i++)
        delete[] blocks[i];
    delete[] blocks;

    return std::make_pair(hashes, changed_bits_count);
}

// Алгоритм преобразования
std::string ripemd320(std::string message) {
    using namespace methods;
    
    // Размер сообщения в битах
    uint64_t bitlen = message.size() * 8;

    // Добавление дополнительных битов
    add_additional_bits(message);

    // Количество блоков для обработки
    uint32_t blocks_count = (uint32_t) (message.size() / 64) + 1;

    // Генерация массива блоков по 512 бит (добавление исходной длины сообщения)
    uint32_t **blocks = generate_blocks_array(blocks_count, bitlen, message);

    // Основной цикл
    uint32_t *hashes = generate_hashes(blocks_count, blocks).first;

    // Результат в виде хэш-сообщения
    std::ostringstream result;

    result << std::hex;
    for (size_t i = 0; i < N; i++) {
        result << inv(hashes[i]);
    }

    return result.str();
}

std::pair<std::string, std::vector<uint32_t>> ripemd320_with_bit_change(std::string message, uint64_t bit_pos) {
    using namespace methods;

    // Размер сообщения в битах
    uint64_t bitlen = message.size() * 8;

    // Добавление дополнительных битов
    add_additional_bits(message);

    // Количество блоков для обработки
    uint32_t blocks_count = (uint32_t) (message.size() / 64) + 1;

    // Генерация массива блоков по 512 бит (добавление исходной длины сообщения)
    uint32_t **blocks = generate_blocks_array(blocks_count, bitlen, message);

    if (bit_pos < bitlen) {
        change_bit(blocks, bit_pos);
    }

    // Основной цикл
    auto pair = generate_hashes(blocks_count, blocks);

    // Результат в виде хэш-сообщения
    std::ostringstream result;

    result << std::hex;
    for (size_t i = 0; i < N; i++) {
        result << inv(pair.first[i]);
    }

    return std::make_pair(result.str(), pair.second);
}
