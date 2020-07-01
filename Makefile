BINDIR=$(HOME)/.local/bin
BINS= \
  $(BINDIR)/,, \
  $(BINDIR)/,af \
  $(BINDIR)/,aulogin \
  $(BINDIR)/,ausetup \
  $(BINDIR)/,auteardown \
  $(BINDIR)/,gerrits2wiki \
  $(BINDIR)/,getzoom \
  $(BINDIR)/,hostaddr \
  $(BINDIR)/,patchreport \
  $(BINDIR)/,resizeimages \
  $(BINDIR)/,rtquery \
  $(BINDIR)/,taskcolor \
  $(BINDIR)/,tasksync \
  $(BINDIR)/,ticket \
  $(BINDIR)/,vlabcfg \
  $(BINDIR)/vmg \

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

$(BINDIR)/%: src/%
	install $< $(BINDIR)
