#!/usr/bin/env bash
gdbus call --session --dest com.muskmelon.MuskMelon \
    --object-path /com/muskmelon/MuskMelon/Object \
    --method com.muskmelon.MuskMelon.Open "['$1']" {}
