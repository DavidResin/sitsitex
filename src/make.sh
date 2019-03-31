#!/bin/sh

file=$1
prefix=${file%.tex}
order=""
comma=""

echo "\n@@ Printing sequential PDF:\n"
latexmk -quiet -pdf $file

pages=$(pdftk $prefix.pdf dump_data|grep NumberOfPages| awk '{print $2}')
sheets=$(expr $(expr $pages + 3) / 4)

for i in $(seq 0 $(expr $sheets - 1));
do
	v1=$(expr 4 \* $sheets - 2 \* $i)
	v2=$(expr 2 \* $i + 1)
	v3=$(expr $v2 + 1)
	v4=$(expr $v1 - 1)

	order="$order$comma$v1,$v2,$v3,$v4"
	comma=","
done

echo "\n@@ Printing arranged PDF ($pages pages, $sheets sheets):\n"
pdflatex --interaction=batchmode \
	-jobname="$prefix-arranged" \
	"\def\sso{$order} \def\ssf{$prefix.pdf} \input{sitsitex-arranger.tex}"