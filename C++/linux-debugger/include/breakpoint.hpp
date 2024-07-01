#ifndef DEBUGGER_BREAKPOINT_HPP
#define DEBUGGER_BREAKPOINT_HPP

#include <cstdint>

namespace debugger {

class breakpoint {
public:
    breakpoint() : m_pid{0}, m_addr{0}, m_enabled{false}, m_saved_data{} {}
    breakpoint(pid_t pid, caddr_t addr) : m_pid{pid}, m_addr{addr}, m_enabled{false}, m_saved_data{} {}

    void enable();
    void disable();

    auto is_enabled() const -> bool { return m_enabled; }
    auto get_address() const -> caddr_t { return m_addr; }

private:
    pid_t m_pid;
    caddr_t m_addr;
    bool m_enabled;
    uint8_t m_saved_data;
}; // class breakpoint

}; // namespace debugger
#endif
