#include <string>
#include <iostream>
#include <sstream>
#include <fstream>

#define ROTATE_LEFT(x, n) (((x) << (n)) | ((x) >> (32-(n))))

using namespace std;

class RIPEMD_320
{
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
    unsigned int bytes_to_uint(char* bytes);

    void extension();
    void adding_length();
    void initialize_ripemd();
    void message_processing();
    ostringstream result;
public:
    void read_message(string str);

    string ripemd_320();
};