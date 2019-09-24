#include <openssl/evp.h>
#include <openssl/hmac.h>

#include <string>

namespace util::encoding {

namespace {
struct HmacCtx
{
    HMAC_CTX ctx;
    HmacCtx() { HMAC_CTX_init(&ctx); }
    ~HmacCtx() { HMAC_CTX_cleanup(&ctx); }
};
}

std::string hmac(const std::string& secret,
                 std::string msg,
                 std::size_t signed_len)
{
    static HmacCtx hmac;
    char signed_msg[64];

    HMAC_Init_ex(
      &hmac.ctx, secret.data(), (int)secret.size(), EVP_sha256(), nullptr);
    HMAC_Update(&hmac.ctx, (unsigned char*)msg.data(), msg.size());
    HMAC_Final(&hmac.ctx, (unsigned char*)signed_msg, nullptr);

    return {signed_msg, signed_len};
}

namespace {
constexpr char hexmap[] = {'0',
                           '1',
                           '2',
                           '3',
                           '4',
                           '5',
                           '6',
                           '7',
                           '8',
                           '9',
                           'a',
                           'b',
                           'c',
                           'd',
                           'e',
                           'f'};
}

std::string string_to_hex(unsigned char* data, std::size_t len)
{
    std::string s(len * 2, ' ');
    for (std::size_t i = 0; i < len; ++i) {
        s[2 * i] = hexmap[(data[i] & 0xF0) >> 4];
        s[2 * i + 1] = hexmap[data[i] & 0x0F];
    }
    return s;
}
}
