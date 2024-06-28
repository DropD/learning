from rel_path_test.lib.rel_path import this_file_abs_path


def foo():
    pass


if __name__ == '__main__':
    print(this_file_abs_path())
    foo()
