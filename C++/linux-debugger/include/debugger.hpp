#ifndef DEBUGGER_HPP
#define DEBUGGER_HPP

#include <unordered_map>

#include "breakpoint.hpp"

namespace debugger {

class debugger {
public:
    debugger (std::string prog_name, pid_t pid) : m_prog_name{std::move(prog_name)}, m_pid{pid} {}
    void run();
    void set_breakpoint_at_address(caddr_t addr);

private:
    void handle_command(const std::string& line);
    void continue_execution();

    std::string m_prog_name;
    pid_t m_pid;
    std::unordered_map<caddr_t, breakpoint> m_breakpoints;
};

};

#endif
