#include <sys/ptrace.h>

#include "breakpoint.hpp"

namespace debugger {

void breakpoint::enable() {
    auto data = ptrace(PT_READ_D, m_pid, m_addr, 0);

    m_saved_data = static_cast<uint8_t>(data & 0xff); // save bottom byte
    uint64_t int3 = 0xcc;
    uint64_t data_with_int3 = ((data & ~0xff) | int3); // set bottom byte to 0xcc
    ptrace(PT_WRITE_D, m_pid, m_addr, data_with_int3);

    m_enabled = true;
}

void breakpoint::disable() {
    auto data = ptrace(PT_READ_D, m_pid, m_addr, 0);
    auto restored_data = ((data & ~0xff) | m_saved_data);
    ptrace(PT_WRITE_D, m_pid, m_addr, restored_data);

    m_enabled = false;
}

}; // namespace debugger
