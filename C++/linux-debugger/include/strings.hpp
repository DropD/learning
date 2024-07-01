#ifndef DEBUGGER_STRINGS_HPP
#define DEBUGGER_STRINGS_HPP

namespace debugger {
namespace strings {

std::vector<std::string> split(const std::string& input_string, char delimiter) ;

bool is_prefix(const std::string& input_string, const std::string& of);

}; // namespace strings
}; // namespace debugger
#endif
