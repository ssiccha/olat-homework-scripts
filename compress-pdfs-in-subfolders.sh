#!/usr/bin/env bash
if [[ $# != 1 ]] && [[ $# != 2 ]]; then
    echo "usage: compress-pdfs-in-subfolders.sh <directory> [<quality>]"
    echo "default <quality> is 'low'"
    exit 1
fi

# This script uses ghostscript to compress all pdfs found in subfolders of
# <directory>.
if [[ -n "${2+x}" ]] && [[ ${2} != "high" ]] && [[ ${2} != "low" ]]; then
    echo "compress-pdfs-in-subfolders.sh: <quality> must be \"high\" or \"low\""
    exit 1
fi

# Check whether ghostscript is available
hash gs || { echo >&2 "ghostscript is not available"; exit 1; }

if [[ ${2:-"low"} = "high" ]]; then
    gs_quality="printer"
else
    gs_quality="ebook"
fi

if [[ ! -d ${1} ]]; then
    echo "compress-pdfs-in-subfolders.sh: no directory found with name ${1}"
fi
# use ** below to recurse over all subdirectories
shopt -s globstar
if [[ -d ${1} ]]; then
    echo Entering ${1}
    for submission in ${1}/**/*.pdf; do
        if [[ -f ${submission} ]]; then
            echo Compressing "${submission}"
            gs -sDEVICE=pdfwrite -dPDFSETTINGS=/${gs_quality} \
                -dNOPAUSE -dQUIET -dBATCH \
                -sOutputFile=__temporary_output.pdf \
                "${submission}"
            mv __temporary_output.pdf "${submission}"
        fi
    done
fi
