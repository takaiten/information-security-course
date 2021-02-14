#include <string>
#include <iostream>
#include <sstream>
#include <fstream>
#include <bit>

namespace RIPEMD {
    using namespace std;

    namespace helpers {
        static uint32_t F(const uint8_t j, uint32_t x, uint32_t y, uint32_t z);
        static uint32_t K1(const uint8_t j);
        static uint32_t K2(const uint8_t j);
        static uint32_t inv(const uint32_t value);
        static uint32_t bytes_to_uint(const char *bytes);

        // Номера выбираемых из сообщения 32-битных слов
        static uint8_t R1[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                               7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
                               3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
                               1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
                               4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13};

        static uint8_t R2[] = {5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
                               6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
                               15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
                               8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
                               12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11};

        // Количество бит, на которое будут осуществляться сдвиги
        static uint8_t S1[] = {11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
                               7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
                               11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
                               11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
                               9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6};

        static uint8_t S2[] = {8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
                               9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
                               9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
                               15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
                               8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11};
    }

    class RIPEMD_320 {
        string message;

        unsigned long long bitlen;

        unsigned int **X;

        unsigned int blocks;

        unsigned int H0, H1, H2, H3, H4, H5, H6, H7, H8, H9;

        unsigned int A1, B1, C1, D1, E1, A2, B2, C2, D2, E2, T;

        unsigned int F(unsigned int j, unsigned int x, unsigned int y, unsigned int z);

        unsigned int K1(unsigned int j);

        unsigned int K2(unsigned int j);

        unsigned int inv(unsigned int value);

        unsigned int bytes_to_uint(char *bytes);

        void extension();

        void adding_length();

        void initialize_ripemd();

        void message_processing();

        ostringstream result;
    public:
        void read_message(string str);

        string ripemd_320();
    };
}
