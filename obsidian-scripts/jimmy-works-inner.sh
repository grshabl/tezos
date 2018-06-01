#!/usr/bin/env bash
set -eux

if [ "X${1:-}" != "Xexisting" ]; then
    obsidian-scripts/jimmy-sandbox-setup.sh
fi

monitored-bakers.sh bootstrap0 bootstrap1

tezos-sandbox-client.sh import ledger secret key my-ledger ed25519
attempt() {
    while ! "$@"; do
        echo 'Failed'
        sleep 3
    done
    sleep 2
}
extract_operation_id() {
    tail -n1 | cut -f2 -d"'"
}

attempt tezos-sandbox-client.sh set delegate for bootstrap0 to my-ledger
attempt tezos-sandbox-client.sh set delegate for bootstrap1 to my-ledger
attempt ledger/reset.sh 00000000 # Reset high water mark

exec tezos-sandbox-client.sh launch daemon my-ledger -B -E -D
#exec tezos-bake-monitor --port 9803 --rpchost 127.0.0.1:18733 --client `which tezos-sandbox-client.sh` --identity my-ledger
