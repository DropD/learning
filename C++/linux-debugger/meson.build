project('linux-debugger', 'cpp', 'c', default_options: 'cpp_std=c++23')
linenoise_includes = include_directories('dependencies/linenoise')
libelfin_includes = include_directories('dependencies/libelfin')
executable('debugger', 'src/main.cpp', 'dependencies/linenoise/linenoise.c', include_directories: [linenoise_includes, libelfin_includes])
