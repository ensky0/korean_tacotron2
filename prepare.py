#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, shutil, random
from zipfile import ZipFile

KSS_DATASET = 'archive.zip'
KSS_ORG_DIR = 'kss'
KSS_ORG_SCRIPT = 'transcript.v.1.4.txt'
KSS_SCRIPT = 'kss_script.txt'


def prepare_kss():
    ZipFile(KSS_DATASET).extractall()
    for dirname in sorted(os.listdir(KSS_ORG_DIR)):
        dirpath = os.path.join(KSS_ORG_DIR, dirname)
        if not os.path.isdir(dirpath):
            continue
        for filename in sorted(os.listdir(dirpath)):
            if not filename.endswith('.wav'):
                continue
            filepath = os.path.join(dirpath, filename)
            newfilepath = os.path.join(KSS_ORG_DIR, filename.replace('_', ''))
            os.system(f'sox {filepath} -r 22050 -b 16 -c 1 {newfilepath}')
        shutil.rmtree(dirpath)

    with open(KSS_ORG_SCRIPT) as rfp:
        lines = []
        for line in rfp:
            elems = line.strip().split('|')
            filename = elems[0].split('/', 1)[1].replace('_', '')
            sentence = elems[2]

            lines.append(f'{KSS_ORG_DIR}{os.sep}{filename}|{sentence}')

    lines = sorted(lines)
    with open(os.path.join(KSS_ORG_DIR, KSS_SCRIPT), 'w') as wfp:
        wfp.write('\n'.join(lines))

    random.seed(1)
    random.shuffle(lines)
    n_valid = int(len(lines) * 0.05)        # valid set: 5%

    base, ext = os.path.splitext(KSS_SCRIPT)
    with open(os.path.join(KSS_ORG_DIR, base+'_valid'+ext), 'w') as wfp:
        wfp.write('\n'.join(sorted(lines[:n_valid])))
    with open(os.path.join(KSS_ORG_DIR, base+'_train'+ext), 'w') as wfp:
        wfp.write('\n'.join(sorted(lines[n_valid:])))


def main(argv=sys.argv):
    prepare_kss()


if __name__ == "__main__":
    sys.exit(main())

