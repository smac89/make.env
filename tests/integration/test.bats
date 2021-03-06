#!/usr/bin/env bats

export PYTHONUNBUFFERED=1
export BATS_LIB_PATH=${BATS_LIB_PATH:-'/usr/lib/:usr/lib/bats/'}
bats_load_library 'bats-support'
bats_load_library 'bats-assert'

setup() {
    mv -f .env{.test,}
    mv -f Makefile{.test,}
}

teardown() {
    mv -f .env{,.test}
    mv -f Makefile{,.test}
}

setup_file() {
    cd "$BATS_TEST_DIRNAME"
}

@test "env variables same as make variables" {
    if ! command -v make; then
        skip "make not found"
    fi

    test_var=$(make.env test_var)
    foo_bar=$(make.env foo_bar)
    source .env
    refute [ -z "$test_var" ]
    refute [ -z "$foo_bar" ]
    assert_equal $test_var "$TEST_VAR"
    assert_equal $foo_bar "$FOO_BAR"
}

@test "env variables exported with existing --eval" {
    if ! command -v make; then
        skip "make not found"
    fi

    run make.env --eval 'export FOO=bar' foo
    assert_line --index 1 'bar'
    source .env
    run make.env --eval 'export FOO=bar' foo test_var
    assert_line --index 1 'bar'
    assert_line --index 2 "$TEST_VAR"
}

@test "env variable with unclosed quote" {
    if ! command -v make; then
        skip "make not found"
    fi

    run make.env another_var
    assert_line --index 1 '"hello world'
}
