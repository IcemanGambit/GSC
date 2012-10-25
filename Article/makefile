all: pdf
pdf:
	if test ! -d bin; then mkdir ./bin/; fi
	pdflatex -output-directory ./bin/ ./d903.tex
	bibtex ./bin/d903.aux
	pdflatex -output-directory ./bin/ ./d903.tex
	pdflatex -output-directory ./bin/ ./d903.tex
	echo  
	if ! cat ./bin/*.log  | grep -A 3 Warning; then echo No warnings; fi
clean:
	rm ./bin/*
open: pdf
	xdg-open ./bin/d903.pdf
cleanopen: clean open
TODO:
	find ./ -name "*.tex" | xargs grep -n TODO | sed -e 's/:\([0-9]*\):.*%TODO[: ]\?/: \1:\n\t/' -e 's/^.\///' -e 's/^src\///' | fmt > TODO
todo: 
	find ./ -name "*.tex" | xargs grep -n TODO | sed -e 's/:\([0-9]*\):.*%TODO[: ]\?/: \1:\n\t/' -e 's/^.\///' -e 's/^src\///' | fmt > TODO
	less TODO
