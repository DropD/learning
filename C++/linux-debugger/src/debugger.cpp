#include <vector>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <print>

#include "linenoise.h"

#include "strings.hpp"
#include "breakpoint.hpp"
#include "debugger.hpp"

namespace debugger {

void debugger::run() {
    int wait_status;
    auto options = 0;
    waitpid(m_pid, &wait_status, options);

    char* line = nullptr;
    while ((line = linenoise("debugger>")) != nullptr) {
        handle_command(line);
        linenoiseHistoryAdd(line);
        linenoiseFree(line);
    }
}

void debugger::set_breakpoint_at_address(caddr_t addr) {
    std::println("Set breakoint at address 0x{}", addr);
    breakpoint bp {m_pid, addr};
    bp.enable();
    m_breakpoints[addr] = bp;
}

void debugger::handle_command(const std::string& line) {
    auto args = strings::split(line, ' ');
    auto command = args[0];

    if (strings::is_prefix(command, "continue")) {
        continue_execution();
    } else if (strings::is_prefix(command, "break")) {
        std::string addr {args[1], 2}; // naively assume that the user has written 0xADDRESS
        set_breakpoint_at_address(addr.data());
    } else {
        std::print("Unknown command\n");
    }
}

void debugger::continue_execution() {
    ptrace(PT_CONTINUE, m_pid, nullptr, 0);

    int wait_status;
    auto options = 0;
    waitpid(m_pid, &wait_status, options);
}

};
