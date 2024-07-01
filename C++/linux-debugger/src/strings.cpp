#include <vector>
#include <sstream>

#include "strings.hpp"

namespace debugger {
namespace strings {

std::vector<std::string> split(const std::string& input_string, char delimiter) {
    std::vector<std::string> out{};
    std::stringstream ss {input_string};
    std::string item;

    while (std::getline(ss, item, delimiter)) {
        out.push_back(item);
    }

    return out;
}

bool is_prefix(const std::string& input_string, const std::string& of) {
    if (input_string.size() > of.size()) return false;
    return std::equal(input_string.begin(), input_string.end(), of.begin());
}

}; // namespace strings
}; // namespace debugger
