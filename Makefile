ARXIV_FILES = figures/ \
							ieee-sp/ \
							acknowledgment.tex \
							IEEEtran.cls \
							imports.tex \
							main-arxiv.bbl \
							main-arxiv.tex \
							references.bib

all: main-arxiv.pdf main-ieeesp.pdf main-long-version.pdf arxiv-submit-files.tar.gz

clean:
	latexmk -pdf -C

main-arxiv.pdf, main-arxiv.bbl:
	latexmk -pdflatex='pdflatex -interaction nonstopmode' -bibtex -pdf main-arxiv.tex

main-ieeesp.pdf:
	latexmk -pdflatex='pdflatex -interaction nonstopmode' -bibtex -pdf main-ieeesp.tex

main-long-version.pdf:
	git rev-parse --short HEAD | xargs printf '\\newcommand*{\\version}{%s}' > version.tex
	latexmk -pdflatex='pdflatex -interaction nonstopmode' -bibtex -pdf main-long-version.tex

arxiv-submit-files.tar.gz: main-arxiv.bbl #need .bbl
	tar -czvf arxiv-submit-files.tar.gz $(ARXIV_FILES)
