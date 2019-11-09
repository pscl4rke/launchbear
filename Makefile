
#DESTDIR=/usr
#PREFIX=/usr

dummy:
	@echo "Usage:"
	@echo "  make install		Install the executables into place"

install:
	install -d $(DESTDIR)/usr/bin
	install launchbear.py $(DESTDIR)/usr/bin/launchbear
	install launchbear_wizard.py $(DESTDIR)/usr/bin/launchbear-wizard
	install -d $(DESTDIR)/usr/share/launchbear/backends
	install backends/* $(DESTDIR)/usr/share/launchbear/backends/.
	install -d $(DESTDIR)/usr/share/man/man1
	install launchbear.1 $(DESTDIR)/usr/share/man/man1/launchbear.1
	install launchbear-wizard.1 $(DESTDIR)/usr/share/man/man1/launchbear-wizard.1

test:
	python2.7 -m unittest discover
