#include <iostream>
#define data_type  int

void EncryptTEA(data_type *firstChunk, data_type *secondChunk, data_type* key)
{
    data_type y = *firstChunk;
    data_type z = *secondChunk;
    data_type sum = 0;

    data_type delta = 0x9e3779b9;

    for (int i = 0; i < 32; i++)//32轮运算(需要对应下面的解密核心函数的轮数一样)
    {
        sum += delta;
        y += ((z << 4) + key[0]) ^ (z + sum) ^ ((z >> 5) + key[1]);
        z += ((y << 4) + key[2]) ^ (y + sum) ^ ((y >> 5) + key[3]);
    }

    *firstChunk = y;
    *secondChunk = z;
}

void DecryptTEA(data_type *firstChunk, data_type *secondChunk, data_type* key)
{
    data_type  sum = 0;
    data_type  y = *firstChunk;
    data_type  z = *secondChunk;
    data_type  delta = 0x9e3779b9;

    sum = delta << 5; //32轮运算，所以是2的5次方；16轮运算，所以是2的4次方；8轮运算，所以是2的3次方

    for (int i = 0; i < 32; i++) //32轮运算
    {
        z -= (y << 4) + key[2] ^ y + sum ^ (y >> 5) + key[3];
        y -= (z << 4) + key[0] ^ z + sum ^ (z >> 5) + key[1];
        sum -= delta;
    }

    *firstChunk = y;
    *secondChunk = z;
}

//buffer：输入的待加密数据buffer，在函数中直接对元数据buffer进行加密；size：buffer长度；key是密钥；
void EncryptBuffer(char* buffer, int size, data_type* key)
{
    char *p = buffer;

    int leftSize = size;

    while (p < buffer + size &&
        leftSize >= sizeof(data_type) * 2)
    {
        EncryptTEA((data_type *)p, (data_type *)(p + sizeof(data_type)), key);
        p += sizeof(data_type) * 2;

        leftSize -= sizeof(data_type) * 2;
    }
}

//buffer：输入的待解密数据buffer，在函数中直接对元数据buffer进行解密；size：buffer长度；key是密钥；
void DecryptBuffer(char* buffer, int size, data_type* key)
{
    char *p = buffer;

    int leftSize = size;

    while (p < buffer + size &&
        leftSize >= sizeof(data_type) * 2)
    {
        DecryptTEA((data_type *)p, (data_type *)(p + sizeof(data_type)), key);
        p += sizeof(data_type) * 2;

        leftSize -= sizeof(data_type) * 2;
    }
}

int main()
{
    //-----设置密钥，必须需要16个字符或以上（这里的长度错误由评论#3楼legion提出修正，表示感谢。）
    data_type key[4] = {0x67616C66,0x6B61667B,0x6C665F65,0x7D216761};
    //-----读取文件
    unsigned int pSize = 0;
    char * pBuffer = NULL;
    FILE *fp;
    int err = fopen_s(&fp, "tea.png.out", "rb"); //sFileName是读取的加密/解密文件名 TODO:处理错误
    fseek(fp, 0, SEEK_END);
    pSize = ftell(fp); //得到长度
    fseek(fp, 0, SEEK_SET);
    pBuffer = new char[pSize]; //开辟内存空间
    pSize = fread(pBuffer, sizeof(char), pSize, fp); //读取内容
    fclose(fp); //关闭文件

    //-----对原始文件进行加密
    //EncryptBuffer(pBuffer, pSize, key);

    //如果是已经加密过的文件，则对应为解密函数
    DecryptBuffer(pBuffer, pSize, key);

    //-----将数据写入文件当中
    FILE *fDestFile=fopen("tea.png","wb");
    //fopen_s(&fDestFile, "tea.png", "wb"); //sTagetFileName是写入的加密/解密文件名
    fwrite(pBuffer, sizeof(char), pSize, fDestFile);
    fclose(fDestFile);//关闭文件

    delete[]pBuffer;
    system("pause");
    return 0;
}