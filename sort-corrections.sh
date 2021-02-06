#!/usr/bin/env bash
if [[ $# != 1 ]]; then
    echo "usage: sort-corrections.sh <folder>"
    exit 1
fi
# LectureNotes uploads all corrections into a single folder, this should be
# ${1}. Olat puts each submission into a directory `user-string/`.
for source_pdf in ${1}/*.pdf; do
    nr_targets_found=0
    if [[ -f $source_pdf ]]; then
        for potential_target in ${1}/*/*.pdf; do
            if [[ $(basename "${source_pdf}") = $(basename "${potential_target}") ]]; then
                target=${potential_target}
                nr_targets_found+=1
            fi
        done
    fi
    if [[ nr_targets_found -ne 1 ]]; then
        echo "# ${nr_targets_found} match(es) found for file ${source_pdf}"
    else
        echo "mv ${source_pdf} ${target}"
    fi
done
