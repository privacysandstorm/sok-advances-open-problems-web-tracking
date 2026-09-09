ARXIV_FILES = figures/ \
    tables/ \
    short-version/ \
    appendix/ \
    acknowledgment.tex \
    custom-style.bst \
    usenix.sty \
    imports.tex \
    main-arxiv.bbl \
    main-arxiv.tex \
    refs.bib

all: main-arxiv.pdf main-usenix.pdf main-long-version.pdf arxiv-submit-files.tar.gz

clean:
	latexmk -pdf -C

main-arxiv.pdf, main-arxiv.bbl:
	latexmk -pdflatex='pdflatex -interaction nonstopmode' -bibtex -pdf main-arxiv.tex

main-usenix.pdf:
	latexmk -pdflatex='pdflatex -interaction nonstopmode' -bibtex -pdf main-usenix.tex

main-long-version.pdf:
	git rev-parse --short HEAD | xargs printf '\\newcommand*{\\version}{%s}' > version.tex
	latexmk -pdflatex='pdflatex -interaction nonstopmode' -bibtex -pdf main-long-version.tex

arxiv-submit-files.tar.gz: main-arxiv.bbl #need .bbl
	tar -czvf arxiv-submit-files.tar.gz $(ARXIV_FILES)
