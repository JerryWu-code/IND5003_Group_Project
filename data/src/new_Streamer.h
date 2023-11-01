// src/Streamer.h
#pragma once  // 防止头文件重复包含

#include <vector>  // 引入vector库
#include <algorithm>  // 引入algorithm库
#include <iostream>  // 引入iostream库
#include <fstream>  // 引入fstream库
#include <sstream>  // 引入sstream库
#include <iomanip>  // 引入iomanip库

#include "Global.h"  // 引入Global头文件
#include "Date.h"  // 引入Date头文件
#include "Macros.h"  // 引入Macros头文件

namespace minirisk {  // 定义命名空间minirisk

// streaming separator
const char separator = ';';  // 定义分隔符为分号

//
// Overload classes
//

struct my_ofstream  // 定义my_ofstream结构体
{
    my_ofstream(const string& fn)  // 构造函数，接收一个字符串引用作为参数
        : m_of(fn)  // 初始化m_of为fn
    {
    }
    void endl() { m_of << std::endl; }  // 定义endl函数，向m_of中插入换行符
    void close() { m_of.close(); }  // 定义close函数，关闭m_of
    std::ofstream m_of;  // 定义m_of为ofstream类型
};

struct my_ifstream  // 定义my_ifstream结构体
{
    my_ifstream(const string& fn)  // 构造函数，接收一个字符串引用作为参数
        : m_if(fn)  // 初始化m_if为fn
    {
        MYASSERT(!m_if.fail(), "Could not open file " << fn);  // 如果打开文件失败，抛出异常
    }

    bool read_line()  // 定义read_line函数，读取一行数据
    {
        std::getline(m_if, m_line);  // 从m_if中读取一行数据，存入m_line
        m_line_stream.str(m_line);   // 将m_line的内容设置为m_line_stream的内容
        return m_line.length() > 0;  // 如果m_line的长度大于0，返回true，否则返回false
    }

    inline string read_token()  // 定义read_token函数，读取一个token
    {
        string tmp;
        std::getline(m_line_stream, tmp, separator);  // 从m_line_stream中读取一个token，存入tmp
        return tmp;  // 返回tmp
    }

private:
    string m_line;  // 定义m_line为string类型
    std::istringstream m_line_stream;  // 定义m_line_stream为istringstream类型
    std::ifstream m_if;  // 定义m_if为ifstream类型
};

//
// Generic file streamer
//

template <typename T>
inline my_ifstream& operator>>(my_ifstream& is, T& v)  // 重载>>操作符，从is中读取一个T类型的值，存入v
{
    string tmp = is.read_token();  // 从is中读取一个token，存入tmp
    std::istringstream(tmp) >> v;  // 将tmp的内容转换为T类型，存入v
    return is;  // 返回is
}

template <typename T>
inline my_ofstream& operator<<(my_ofstream& os, const T& v)  // 重载<<操作符，将v的值插入到os中
{
    os.m_of << v << separator;  // 将v的值和分隔符插入到os的m_of中
    return os;  // 返回os
}

//
// Double streamer overloads
//

// when saving a double to a file in text format, use the maximum possible precision
inline my_ofstream& operator<<(my_ofstream& os, double v)  // 重载<<操作符，将double类型的v插入到os中
{
    os.m_of << std::scientific << std::setprecision(16) << v << separator;  // 将v的值以科学计数法的形式，保留16位精度，插入到os的m_of中
    return os;  // 返回os
}

// 重载<<操作符，将double类型转换为16进制表示
inline my_ofstream& operator<<(my_ofstream& os, const double& d) {  // 重载<<操作符，将double类型的d插入到os中
    union { double d; uint64_t u; } tmp;  // 定义一个联合体，包含double类型的d和uint64_t类型的u
    tmp.d = d;  // 将d的值赋给tmp.d
    os.m_of << std::hex << tmp.u << separator; // 将tmp.u的值以16进制的形式插入到os的m_of中
    return os;  // 返回os
}

// 重载>>操作符，将16进制表示转换为double类型
inline my_ifstream& operator>>(my_ifstream& is, double& d) {  // 重载>>操作符，从is中读取一个double类型的值，存入d
    union { double d; uint64_t u; } tmp;  // 定义一个联合体，包含double类型的d和uint64_t类型的u
    is >> std::hex >> tmp.u; // 从is中以16进制的形式读取一个值，存入tmp.u
    d = tmp.d;  // 将tmp.d的值赋给d
    return is;  // 返回is
}

//
// Vector streamer overloads
//

template <typename T, typename A>
inline std::ostream& operator<<(std::ostream& os, const std::vector<T, A>& v)  // 重载<<操作符，将vector类型的v插入到os中
{
    for (const T& i : v)  // 遍历v中的每一个元素i
        os << i << " ";  // 将i的值和一个空格插入到os中
    return os;  // 返回os
}

template <typename T>
inline my_ofstream& operator<<(my_ofstream& os, const std::vector<T>& v)  // 重载<<操作符，将vector类型的v插入到os中
{
    os << v.size();  // 将v的大小插入到os中
    for (const T& i : v)  // 遍历v中的每一个元素i
        os << i;  // 将i的值插入到os中
    return os;  // 返回os
}

template <typename T, typename A>
inline my_ifstream& operator>>(my_ifstream& is, std::vector<T, A>& v)  // 重载>>操作符，从is中读取一个vector类型的值，存入v
{
    size_t sz;  // 定义sz为size_t类型
    is >> sz; // 从is中读取一个值，存入sz
    v.resize(sz);  // 将v的大小调整为sz
    for (size_t i = 0; i < sz; ++i)  // 从0到sz-1，遍历每一个i
        is >> v[i];  // 从is中读取一个值，存入v的第i个元素
    return is;  // 返回is
}

//
// Date streamer overloads
//

inline std::ostream& operator<<(std::ostream& os, const Date& d)  // 重载<<操作符，将Date类型的d插入到os中
{
    os << d.to_string(true);  // 将d转换为字符串的形式，插入到os中
    return os;  // 返回os
}

inline my_ofstream& operator<<(my_ofstream& os, const Date& d)  // 重载<<操作符，将Date类型的d插入到os中
{
    os << d.to_string(false);  // 将d转换为字符串的形式，插入到os中
    return os;  // 返回os
}

inline my_ifstream& operator>>(my_ifstream& is, Date& v)  // 重载>>操作符，从is中读取一个Date类型的值，存入v
{
    string tmp;  // 定义tmp为string类型
    is >> tmp;  // 从is中读取一个值，存入tmp
    unsigned y = std::atoi(tmp.substr(0, 4).c_str());  // 将tmp的前4个字符转换为整数，存入y
    unsigned m = std::atoi(tmp.substr(4, 2).c_str());  // 将tmp的第4个到第5个字符转换为整数，存入m
    unsigned d = std::atoi(tmp.substr(6, 2).c_str());  // 将tmp的第6个到第7个字符转换为整数，存入d
    v.init(y, m, d);  // 用y，m，d初始化v
    return is;  // 返回is
}

} // namespace minirisk