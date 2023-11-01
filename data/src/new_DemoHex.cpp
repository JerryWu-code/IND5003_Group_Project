#include <sstream>

// 重载<<操作符，将double类型转换为16进制表示
std::ostream& operator<<(std::ostream& os, const double& d) {
    union { double d; uint64_t u; } tmp;
    tmp.d = d;
    os << std::hex << tmp.u; // 将double转换为16进制表示
    return os;
}

// 重载>>操作符，将16进制表示转换为double类型
std::istream& operator>>(std::istream& is, double& d) {
    union { double d; uint64_t u; } tmp;
    is >> std::hex >> tmp.u; // 从16进制表示读取double
    d = tmp.d;
    return is;
}
