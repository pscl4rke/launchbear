
#DESTDIR=/usr
#PREFIX=/usr

dummy:
	@echo "Usage:"
	@echo "  make install		Install the executables into place"

install:
	install launchbear /usr/bin/launchbear
	install install-for-user /usr/bin/launchbear-wizard
	install -d /usr/share/launchbear/backends
	install backends/* /usr/share/launchbear/backends/.

