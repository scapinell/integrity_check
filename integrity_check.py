import os
import hashlib
import argparse


def check_line_format(line):
    """Checks if the lines in the input file are in the correct format:
    file_name hash_algorithm hash_sum,
    where hash_algorithm should be one of the following: mda5, sha1, sha256.
    Returns True if line format is correct, otherwise prints, what's wrong with it.
    """
    chunks = line.split()
    permitted_algos = ['sha1', 'sha256', 'md5']
    if len(chunks) == 3 and chunks[1] in permitted_algos:
        return (True, '')
    elif len(chunks) == 1:
        return (False, 'Please specify hash algorithm for the ' + chunks[0])
    elif len(chunks) == 2:
        return (False, 'Please specify hash sum for the ' + chunks[0])
    elif chunks[1] not in permitted_algos:
        return (False, 'Please use one of the following hash algorithms for the ' + chunks[0] + ': mda5, sha1, sha256')
    else:
        return (False, 'Something but hash algorithm and hash sum was specified for the ' + chunks[0])


def hashsum(path, hash_type):
    """Calculates hash sum for the input file using given hash algorithm."""
    hashinst = hash_type()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(hashinst.block_size * 128), b''):
            hashinst.update(chunk)
    return hashinst.hexdigest()


def check_integrity(string, path_to_files_dir):
    """Checks integrity of the file specified in given string by checking if specified sum matches with calculated."""
    if not check_line_format(string)[0]:
            return check_line_format(string)[1]

    file_hash_data = string.split()
    (file_name, algo, hash_result) = (file_hash_data[0], file_hash_data[1], file_hash_data[2])
    path_to_file = os.path.join(path_to_files_dir, file_name)
    if not os.path.exists(path_to_file):
        return file_name + ' NOT FOUND'
    else:
        hash_algo = getattr(hashlib, algo)
        if hashsum(path_to_file, hash_algo) == hash_result:
            return file_name + ' OK'
        else:
            return file_name + ' FAIL'



def check_file(path_to_sum_file, path_to_files_dir):
    """Checks integrity of files specified in the input file using check_integrity function for each line."""
    with open(path_to_sum_file, 'r') as f1:
        if not os.stat(path_to_sum_file):
            print('File with hash data is empty')
        for line in f1:
            if line == "\n":
                continue
            print(check_integrity(line, path_to_files_dir))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='integrity_check.py', description='''This program checks the integrity of the 
                                            files specified in the input file''')
    parser.add_argument('path_to_sum_file', help='path to the file with hash data')
    parser.add_argument('path_to_files_dir', help='path to the directory containing the files to check')
    args = parser.parse_args()
    if not os.path.isfile(args.path_to_sum_file):
        print('path_to_sum_file does not exist or is not a file')
    elif not os.path.isdir(args.path_to_files_dir):
        print('path_to_files_dir does not exist or is not a directory')
    else:
        check_file(args.path_to_sum_file, args.path_to_files_dir)
