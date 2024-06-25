#include <vector>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <print>
#include <sstream>
#include <unistd.h>

#include "linenoise.h"

class debugger {
public:
    debugger (std::string prog_name, pid_t pid) : m_prog_name{std::move(prog_name)}, m_pid{pid} {}
    void run();

private:
    void handle_command(const std::string& line);
    void continue_execution();

    std::string m_prog_name;
    pid_t m_pid;
};

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
        ptrace(PT_TRACE_ME, 0, nullptr, 0);
        execl(prog, prog, nullptr);
    } else if (pid >= 1) {
        // parent process
        // execute debugger
        std::print("Started debugging process");
        debugger dbg{prog, pid};
        dbg.run();
    }
}

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

void debugger::handle_command(const std::string& line) {
    auto args = split(line, ' ');
    auto command = args[0];

    if (is_prefix(command, "continue")) {
        continue_execution();
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
