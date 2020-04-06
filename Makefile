BINDIR=$(HOME)/.local/bin
BINS= \
  $(BINDIR)/af \
  $(BINDIR)/afsutil-setup.sh \
  $(BINDIR)/afsutil-teardown.sh \
  $(BINDIR)/apt-get-zoom \
  $(BINDIR)/gen-virt-lab-cfg.py \
  $(BINDIR)/hostaddr \
  $(BINDIR)/jumble \
  $(BINDIR)/openafs-release-team-report.sh \
  $(BINDIR)/openafs-wiki-gerrits.py \
  $(BINDIR)/resize-photos \
  $(BINDIR)/rt-query.py \
  $(BINDIR)/taskcolor \
  $(BINDIR)/tasksync \
  $(BINDIR)/ticket

.PHONY: install
install: .requirements $(BINDIR) $(BINS)

.PHONY: remove
remove:
	rm -f $(BINS)
	rm -f .requirements

.requirements:
	pip install -r requirements.txt
	touch .requirements

$(BINDIR):
	install -d $(BINDIR)

$(BINDIR)/%: %
	install $< $(BINDIR)
