project('linux-debugger', 'cpp', 'c', default_options: 'cpp_std=c++23')

linenoise_includes = include_directories('dependencies/linenoise')
libelfin_includes = include_directories('dependencies/libelfin')
includes = include_directories('include')

executable(
    'debugger',
    'src/main.cpp',
    'src/debugger.cpp',
    'src/breakpoint.cpp',
    'src/strings.cpp',
    'dependencies/linenoise/linenoise.c',
    include_directories: [includes, linenoise_includes, libelfin_includes]
)

executable(
    'print_to_stderr', 'src/print_to_stderr.cpp'
)
