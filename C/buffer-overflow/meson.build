project('buffer-overflow', 'c')
executable('vulnerable', 'vulnerable.c', c_args : ['-fno-stack-protector'])
executable('invulnerable', 'invulnerable.c', c_args : ['-fno-stack-protector'])
