#!/usr/bin/env bats

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
    test_var=$(make.env test_var)
    echo $test_var
}
