
#DESTDIR=/usr
#PREFIX=/usr

dummy:
	@echo "Usage:"
	@echo "  make install		Install the executables into place"

install:
	install -d $(DESTDIR)/usr/bin
	install launchbear $(DESTDIR)/usr/bin/launchbear
	install install-for-user $(DESTDIR)/usr/bin/launchbear-wizard
	install -d $(DESTDIR)/usr/share/launchbear/backends
	install backends/* $(DESTDIR)/usr/share/launchbear/backends/.

