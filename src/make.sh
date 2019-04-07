#!/bin/sh

# This script is the central part of SitsiTeX. To run it, just do:
# 	sh make.sh songbook.tex

file=$1
prefix=${file%.tex}
order=""
comma=""
auxdir="./aux_files"
outdir="./outputs.pdf"

# Compilation of the main songbook file

echo "\n@@ Printing sequential PDF:\n"
latexmk -quiet \
	-auxdir=$auxdir \
	-outdir=$auxdir \
	-pdf $file

echo "\n@@ Done"

# Computation of the number of pages and sheets for a booklet

pages=$(pdftk $auxdir/$prefix.pdf dump_data|grep NumberOfPages| awk '{print $2}')
sheets=$(expr $(expr $pages + 3) / 4)

# Creation of the appropriate sequence of pages for a booklet

for i in $(seq 0 $(expr $sheets - 1));
do
	v1=$(expr 4 \* $sheets - 2 \* $i)
	v2=$(expr 2 \* $i + 1)
	v3=$(expr $v2 + 1)
	v4=$(expr $v1 - 1)

	order="$order$comma$v1,$v2,$v3,$v4"
	comma=","
done

# Compilation of the booklet

echo "\n@@ Printing booklet ($pages pages, $sheets sheets):\n"
pdflatex --interaction=batchmode \
	-output-directory=$auxdir \
	-jobname="$prefix-booklet" \
	"\def\sso{$order} \def\ssf{$auxdir/$prefix.pdf} \input{booklet.tex}"

echo "\n@@ Done"

# Copying PDF files to output directory

echo "\n@@ Moving output files"

[ -e "$outdir/$prefix.pdf" ] && rm "$outdir/$prefix.pdf"
cp "$auxdir/$prefix.pdf" "$outdir"
[ -e "$outdir/$prefix-booklet.pdf" ] && rm "$outdir/$prefix-booklet.pdf"
cp "$auxdir/$prefix-booklet.pdf" "$outdir"

echo "\n@@ Done"