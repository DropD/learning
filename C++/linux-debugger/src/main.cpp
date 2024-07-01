#include <sys/ptrace.h>
#include <print>
#include <unistd.h>

#include "debugger.hpp"

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::print(stdout, "Program name not specified.");
        return -1;
    }
    
    auto prog = argv[1];

    auto pid = fork();
    if (pid == 0) {
        // child process
        // execute debuggee
        personality(ADDR_NO_RANDOMIZE);
        ptrace(PT_TRACE_ME, 0, nullptr, 0);
        execl(prog, prog, nullptr);
    } else if (pid >= 1) {
        // parent process
        // execute debugger
        std::print("Started debugging process");
        debugger::debugger dbg{prog, pid};
        dbg.run();
    }

    return 0;
}
