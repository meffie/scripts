BINDIR=$(HOME)/.local/bin

.PHONY: install
install:
	install -d $(BINDIR)
	install af $(BINDIR)
	install hostaddr $(BINDIR)
	install jumble $(BINDIR)
	install openafs-release-team-report.sh $(BINDIR)
	install openafs-wiki-gerrits.py $(BINDIR)
	install resize-photos $(BINDIR)
	install rt-query.py $(BINDIR)
	install taskcolor $(BINDIR)
	install tasksync $(BINDIR)
