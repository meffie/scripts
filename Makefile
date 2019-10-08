BINDIR=$(HOME)/.local/bin

.PHONY: install
install:
	install -d $(BINDIR)
	install af $(BINDIR)
	install openafs-release-team-report.sh $(BINDIR)
	install openafs-wiki-gerrits.py $(BINDIR)
	install rt-query.py $(BINDIR)
	install taskcolor $(BINDIR)
