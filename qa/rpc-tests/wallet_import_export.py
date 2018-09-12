#!/usr/bin/env python2
# Copyright (c) 2018 The Zcash developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_true, start_nodes

class WalletImportExportTest (BitcoinTestFramework):
    def setup_network(self, split=False):
        extra_args = [["-exportdir={}/export{}".format(self.options.tmpdir, i)] for i in range(2)]
        self.nodes = start_nodes(2, self.options.tmpdir, extra_args)

    def run_test(self):
        sprout_address0 = self.nodes[0].z_getnewaddress('sprout')
        sapling_address0 = self.nodes[0].z_getnewaddress('sapling')

        # node 0 should have the keys
        dump_path = self.nodes[0].z_exportwallet('walletdump')
        (t_keys0, sprout_keys0, sapling_keys0) = parse_wallet_file(dump_path)
        
        assert_true(sprout_address0 in sprout_keys0)
        assert_true(sapling_address0 in sapling_keys0)

        # node 1 should not
        dump_path = self.nodes[1].z_exportwallet('walletdump')
        (t_keys1, sprout_keys1, sapling_keys1) = parse_wallet_file(dump_path)
        
        assert_true(sprout_address0 not in sprout_keys1)
        assert_true(sapling_address0 not in sapling_keys1)

# Helper functions
def parse_wallet_file(dump_path):
    file_lines = open(dump_path, "r").readlines()

    (t_keys, i) = parse_wallet_file_lines(file_lines, 0)
    (sprout_keys, i) = parse_wallet_file_lines(file_lines, i)
    (sapling_keys, i) = parse_wallet_file_lines(file_lines, i)

    return (t_keys, sprout_keys, sapling_keys)

def parse_wallet_file_lines(file_lines, i):
    keys = []
    # skip blank lines and comments
    while i < len(file_lines) and (file_lines[i] == '\n' or file_lines[i].startswith("#")):
        i += 1
    # add keys until we hit another blank line or comment
    while  i < len(file_lines) and not (file_lines[i] == '\n' or file_lines[i].startswith("#")):
        keys.append(file_lines[i])
        i += 1
    return ("".join(keys), i)

if __name__ == '__main__':
    WalletImportExportTest().main()