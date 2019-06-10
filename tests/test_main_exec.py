from os import system

def fail_without_args():
    return system('python3 bust')

def test_fail_without_args():
    assert fail_without_args() == 512

def exec_succeed_showing_help():
    return system('python3 bust -h')

def test_exec_succeed_showing_help():
    assert exec_succeed_showing_help() == 0
