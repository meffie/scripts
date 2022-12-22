BINDIR=$(HOME)/.local/bin
BINS= \
  $(BINDIR)/,, \
  $(BINDIR)/,af \
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
  $(BINDIR)/git-snapshot \
  $(BINDIR)/vmg \

TASKWARRIOR_HOOK_DIR=$(HOME)/.task/hooks
TASKWARRIOR_HOOKS= \
  $(TASKWARRIOR_HOOK_DIR)/on-add-create-kb-card.py

.PHONY: install
install: .requirements $(BINDIR) $(BINS) $(TASKWARRIOR_HOOKS)

.PHONY: remove
remove:
	rm -f $(BINS)
	rm -f .requirements

.requirements:
	python3 -m pip install --user -r requirements.txt
	touch .requirements

$(BINDIR):
	install -d $(BINDIR)

$(BINDIR)/%: src/%
	install $< $(BINDIR)

$(TASKWARRIOR_HOOK_DIR)/%: src/%
	install $< $(TASKWARRIOR_HOOK_DIR)
