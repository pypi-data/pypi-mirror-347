"""
cashcat - simple file integrity verification tool
Copyright (C) 2025  bitrate16

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import hashlib
import typing
import attr
import json
import os


@attr.s
class Args:
    root: list[str] = attr.ib()
    hashfile: str = attr.ib()
    mode: str = attr.ib()
    verbose: bool = attr.ib()


ALGORHITMS = (
    'md5',
    'sha1',
)


def parse_args() -> Args:
    parser = argparse.ArgumentParser('cashcat')

    parser.add_argument(
        'mode',
        choices=[ 'check', 'generate', 'update' ],
        help='action mode: check - checks files agains the hash store; generate - force regenerate all hashes; update - generate hashes only for new files',
        type=str,
    )

    parser.add_argument(
        '-r',
        '--root',
        help='paths to tree roots, at least 2 roots to compare',
        type=str,
        nargs='+',
        required=True,
    )

    parser.add_argument(
        '-s',
        '--hashfile',
        help='path to hash file store',
        type=str,
        default='./cashcat.json',
    )

    parser.add_argument(
        '-v',
        '--verbose',
        help='verbose logging',
        action='store_true',
    )

    parsed = parser.parse_args()

    args = Args(**vars(parsed))

    # Validate args.root
    args.root = list(
        sorted(
            list(
                set(
                    [
                        os.path.abspath(path)
                            for path in args.root
                    ] # btw i use lisp
                )
            )
        )
    )

    if len(args.root) < 1:
        log('Required at least one root path to check')
        exit(1)

    for root in args.root:
        if not os.path.exists(root):
            log(f'Root {root !r} not exists')
            exit(1)

    # Validate args.hashfile
    args.hashfile = os.path.abspath(args.hashfile)

    return args


@attr.s
class FileNode:
    type: int = attr.ib()
    path: str = attr.ib()


def collect_file_paths_set(path: str) -> set[str]:
    result = set()

    for root, dirs, files in os.walk(path):
        for file in files:
            result.add(
                os.path.abspath(os.path.join(root, file))
            )

        for dir in dirs:
            result.update(
                collect_file_paths_set(
                    os.path.join(root, dir)
                )
            )

    return result


def truncate_root(paths: set[str], root: str) -> set[str]:
    result = set()

    for path in paths:
        if len(path) != len(root):  # ==
            result.add(path[len(root) + 1:])

    return result


def load_store(path: str) -> dict[str, list[str]]:
    """Load hash store"""

    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    return dict()


def save_store(store: dict[str, list[str]], path: str) -> None:
    """Load hash store"""

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(store, f)


def log(*messages) -> None:
    print(*messages, flush=True)


def main():
    args = parse_args()

    # Collect reality
    root_path_data = {}
    for root in args.root:
        root_path_data[root] = truncate_root(collect_file_paths_set(root), root)

    # Common paths intersection
    common_paths = root_path_data[args.root[0]]
    for root in args.root[1:]:
        common_paths = common_paths.intersection(root_path_data[root])

    # Show whar is missing for each root
    header_written = False
    for root in sorted(args.root):
        missing = root_path_data[root].difference(common_paths)
        if len(missing):
            if not header_written:
                header_written = True
                log('Not all files exist in each root:')
                log()

            log(f'[MISS] Missing in {root !r}:')
            for miss in sorted(missing):
                log(f'       - Path: {os.path.join(root, miss) !r}')
                log(f'         File: {miss !r}')
            log()

    # Nothing to compare
    if len(common_paths) == 0:
        log('Nothing to compare')
        return

    store: dict[str, list[str]] = None
    if args.mode == 'generate':
        store = dict()
    else:
        store = load_store(args.hashfile)

        if args.verbose:
            log(f'Hash store has {len(store)} entries')
            log()

    if args.mode == 'check':
        log('Checking existing files using hash store')
        log()

        for path_index, path in enumerate(sorted(common_paths)):
            if args.verbose:
                log(f'> [{path_index + 1} / {len(common_paths)}] Processing {path !r}')

            if path not in store:
                log(f'[WARN] File not in store:')
                log(f'       File: {path !r}')
                log()

                continue

            # Compute hashes
            for hash in ALGORHITMS:
                store_for_path = store[path]

                if hash not in store_for_path:
                    log(f'[WARN] Hash not in store:')
                    log(f'       File: {path !r}')
                    log(f'       Hash: {hash}')
                    log()

                    continue

                root_hash = {}

                # Check that each root has the same file
                for root in args.root:
                    full_path = os.path.join(root, path)

                    if args.verbose:
                        log(f'[INFO] In {root !r}')
                        log(f'       Hash {hash}')
                        log(f'       Of {path}')

                    with open(full_path, 'rb') as f:
                        hash_value = hashlib.file_digest(f, hash).hexdigest()

                    if args.verbose:
                        log(f'       Is {hash_value}')
                        log()

                    root_hash[root] = hash_value

                one_of_hashes = store_for_path[hash]
                for root in args.root:
                    if one_of_hashes != root_hash[root]:
                        log(f'[FAIL] File variant hash mismatch:')
                        log(f'       File: {path !r}')
                        log(f'       Hash: {hash}')
                        log(f'       Expected: {store_for_path[hash]}')
                        log(f'       Variants:')
                        for subroot in args.root:
                            full_path = os.path.join(subroot, path)
                            log(f'         - Path: {full_path !r}')
                            log(f'           Hash: {root_hash[subroot]}')
                        log()

                        break
                else:
                    log(f'[OK]   File hash match:')
                    log(f'       File: {path !r}')
                    log(f'       Hash: {hash}')
                    log(f'       Value: {one_of_hashes}')
                    log()

    else:
        if args.mode == 'generate':
            log('Generating hashes for all files')
        else:
            log('Adding hashes for new file')

        log()

        for path in sorted(common_paths):
            if args.verbose:
                log(f'> Processing {path !r}')

            # Compute hashes
            for hash in ALGORHITMS:
                store_for_path = store.get(path, {})
                store[path] = store_for_path

                if hash in store_for_path:
                    log(f'[INFO] Hash in store:')
                    log(f'       File: {path !r}')
                    log(f'       Hash: {hash}')
                    log(f'       Value: {store_for_path[hash]}')
                    log()

                    continue

                root_hash = {}

                # Check that each root has the same file
                for root in sorted(args.root):
                    full_path = os.path.join(root, path)

                    if args.verbose:
                        log(f'[INFO] In {root !r}')
                        log(f'       Hash {hash}')
                        log(f'       Of {path}')

                    with open(full_path, 'rb') as f:
                        hash_value = hashlib.file_digest(f, hash).hexdigest()

                    if args.verbose:
                        log(f'       Is {hash_value}')
                        log()

                    root_hash[root] = hash_value

                one_of_hashes = root_hash[args.root[0]]
                for root in args.root[1:]:
                    if one_of_hashes != root_hash[root]:
                        log(f'[FAIL] File variant hash mismatch:')
                        log(f'       File: {path !r}')
                        log(f'       Hash: {hash}')
                        log(f'       Variants:')
                        for subroot in args.root:
                            full_path = os.path.join(subroot, path)
                            log(f'         - Path: {full_path !r}')
                            log(f'           Hash: {root_hash[subroot]}')
                        log()

                        break
                else:
                    log(f'[NEW]  New hash for file:')
                    log(f'       File: {path !r}')
                    log(f'       Hash: {hash}')
                    log()

                    store_for_path[hash] = hash_value

                    save_store(store, args.hashfile)


if __name__ == '__main__':
    main()
