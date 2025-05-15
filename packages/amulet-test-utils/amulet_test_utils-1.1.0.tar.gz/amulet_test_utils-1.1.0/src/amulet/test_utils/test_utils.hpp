#pragma once

#include <string>

template <typename T>
std::string cast_to_string(const T& obj)
{
    if constexpr (std::is_arithmetic_v<T>) {
        return std::to_string(obj);
    } else if constexpr (std::is_same_v<T, std::string> || std::is_convertible_v<T, std::string>) {
        return obj;
    } else {
        return "";
    }
}

#define _ASSERT_COMPARE(CLS, A, B, OP)                              \
    {                                                               \
        CLS assert_comp_a = [&]() {                                 \
            try {                                                   \
                CLS assert_comp_value = A;                          \
                return assert_comp_value;                           \
            } catch (const std::exception& e) {                     \
                std::string assert_comp_msg;                        \
                assert_comp_msg.reserve(200);                       \
                assert_comp_msg += "Failed evaluating A in file ";  \
                assert_comp_msg += __FILE__;                        \
                assert_comp_msg += " at line ";                     \
                assert_comp_msg += std::to_string(__LINE__);        \
                assert_comp_msg += ". ";                            \
                assert_comp_msg += e.what();                        \
                throw std::runtime_error(assert_comp_msg);          \
            }                                                       \
        }();                                                        \
        CLS assert_comp_b = [&]() {                                 \
            try {                                                   \
                CLS assert_comp_value = B;                          \
                return assert_comp_value;                           \
            } catch (const std::exception& e) {                     \
                std::string assert_comp_msg;                        \
                assert_comp_msg.reserve(200);                       \
                assert_comp_msg += "Failed evaluating B in file ";  \
                assert_comp_msg += __FILE__;                        \
                assert_comp_msg += " at line ";                     \
                assert_comp_msg += std::to_string(__LINE__);        \
                assert_comp_msg += ". ";                            \
                assert_comp_msg += e.what();                        \
                throw std::runtime_error(assert_comp_msg);          \
            }                                                       \
        }();                                                        \
        if (!(assert_comp_a OP assert_comp_b)) {                    \
            std::string assert_comp_msg;                            \
            assert_comp_msg.reserve(200);                           \
            assert_comp_msg += "A " #OP " B failed in file ";       \
            assert_comp_msg += __FILE__;                            \
            assert_comp_msg += " at line ";                         \
            assert_comp_msg += std::to_string(__LINE__);            \
            assert_comp_msg += ".";                                 \
            auto assert_comp_a_msg = cast_to_string(assert_comp_a); \
            if (!assert_comp_a_msg.empty()) {                       \
                assert_comp_msg += " A: " + assert_comp_a_msg;      \
            }                                                       \
            auto assert_comp_b_msg = cast_to_string(assert_comp_b); \
            if (!assert_comp_b_msg.empty()) {                       \
                assert_comp_msg += " B: " + assert_comp_b_msg;      \
            }                                                       \
            throw std::runtime_error(assert_comp_msg);              \
        }                                                           \
    }

#define ASSERT_EQUAL(CLS, A, B) _ASSERT_COMPARE(CLS, A, B, ==)
#define ASSERT_NOT_EQUAL(CLS, A, B) _ASSERT_COMPARE(CLS, A, B, !=)
#define ASSERT_LESS(CLS, A, B) _ASSERT_COMPARE(CLS, A, B, <)
#define ASSERT_LESS_EQUAL(CLS, A, B) _ASSERT_COMPARE(CLS, A, B, <=)
#define ASSERT_GREATER(CLS, A, B) _ASSERT_COMPARE(CLS, A, B, >)
#define ASSERT_GREATER_EQUAL(CLS, A, B) _ASSERT_COMPARE(CLS, A, B, >=)

#define ASSERT_RAISES(EXC, A)                                      \
    {                                                              \
        bool err_raised = false;                                   \
        try {                                                      \
            A;                                                     \
        } catch (const EXC&) {                                     \
            err_raised = true;                                     \
        } catch (...) {                                            \
            std::string assert_raise_msg;                          \
            assert_raise_msg.reserve(200);                         \
            assert_raise_msg += "Other exception raised in file "; \
            assert_raise_msg += __FILE__;                          \
            assert_raise_msg += " at line ";                       \
            assert_raise_msg += std::to_string(__LINE__);          \
            assert_raise_msg += ". ";                              \
            throw std::runtime_error(assert_raise_msg);            \
        }                                                          \
        if (!err_raised) {                                         \
            std::string assert_raise_msg;                          \
            assert_raise_msg.reserve(200);                         \
            assert_raise_msg += "Exception not raised in file ";   \
            assert_raise_msg += __FILE__;                          \
            assert_raise_msg += " at line ";                       \
            assert_raise_msg += std::to_string(__LINE__);          \
            assert_raise_msg += ". ";                              \
            throw std::runtime_error(assert_raise_msg);            \
        }                                                          \
    }
