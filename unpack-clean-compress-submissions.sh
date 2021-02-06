#!/usr/bin/env bash
if [[ $# != 1 ]]; then
    echo "usage: unpack-clean-compress-submissions.sh <sheet-number>"
    exit 1
fi

prefix='Blatt_'
path_to_compression_script=${HOME}/Seafile/exercise-scripts/compress-pdfs-in-subfolders.sh
# This script unpacks the file which matches the shell pattern
# '${prefix}${1}*.zip' and cleans it up. Then it puts all submissions into the
# folder `blatt-${1}`.

# TODO: how do I get this test to work?
#if [[ ! -f ${prefix}${1}*.zip ]]; then
#    echo "unpack-clean-compress-submissions.sh: No file found with name ${prefix}${1}*.zip"
#fi
echo "Unpacking the zip file."
unzip -q ${prefix}${1}*.zip

echo "Removing redundant subdirectories and then empty student folders."
rm -r ._oo_meta_ita_${prefix}${1}* &> /dev/null
rm ita_${prefix}${1}*/TUK*.xlsx &> /dev/null
rm -r ita_${prefix}${1}*/solutions &> /dev/null
find ita_${prefix}${1}* -name 1_task | xargs rm -r &> /dev/null
find ita_${prefix}${1}* -name '?_corrections' | xargs rm -r &> /dev/null
# delete empty dirs
rmdir --ignore-fail-on-non-empty ita_${prefix}${1}*/*/

echo "Unpacking and removing the ?_submissions folders."
# move everything from each ?_submissions directory one level up, then delete
# the ?_submissions directory.
for dir in ./ita_${prefix}${1}*/*/?_submissions; do
    if [[ -d ${dir} ]]; then
        mv ${dir}/* ${dir}/..
        rmdir ${dir}
    fi
done

echo "Unzipping zipped submissions."
for dir in ./ita_${prefix}${1}*/*/; do
    for archive in ${dir}/*.zip; do
        if [[ -f ${archive} ]]; then
            unzip "${archive}" -d "${dir}"
            rm "${archive}"
        fi
    done
done

echo "Compressing submissions."
"${path_to_compression_script}" ./ita_${prefix}${1}*/

echo "Moving submissions into folder blatt-${1}"
if [[ ! -d blatt-${1} ]]; then
    mkdir blatt-${1}
fi
rsync -auv ita_${prefix}${1}*/ blatt-${1}/ \
| grep --invert-match '.*/$'
rm -r ita_${prefix}${1}*/
