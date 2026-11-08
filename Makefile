.DEFAULT_GOAL := help
PYTHON ?= python3
ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

.PHONY: help doctor check prepare iso verify clean

help:
	@printf 'SinisterNux Alpha 0.2 — make targets\n'
	@printf '  doctor   Check Arch build environment\n'
	@printf '  check    Run offline validations\n'
	@printf '  prepare  Stage and brand upstream releng + KDE\n'
	@printf '  iso      Prepare and build ISO with mkarchiso (sudo)\n'
	@printf '  verify   Verify ISO SHA-256 file(s)\n'
	@printf '  clean    Confirm removal of generated build files\n'

doctor:
	@bash "$(ROOT)/scripts/doctor.sh"

check:
	@$(PYTHON) -m unittest discover -s "$(ROOT)/tests" -p 'test_*.py' -v
	@bash -n "$(ROOT)/scripts/doctor.sh" "$(ROOT)/scripts/clean.sh" "$(ROOT)/desktop-overlay/airootfs/usr/local/sbin/sinisternux-create-live-user" "$(ROOT)/profile-overlay/airootfs/usr/local/bin/sinister-info" "$(ROOT)/profile-overlay/airootfs/etc/profile.d/90-sinister-welcome.sh"

prepare: check
	@$(PYTHON) "$(ROOT)/tools/prepare_profile.py"
	@$(PYTHON) "$(ROOT)/tools/prepare_desktop.py"

iso: prepare
	@command -v mkarchiso >/dev/null || { echo 'mkarchiso not found: install archiso inside an Arch VM' >&2; exit 1; }
	@mkdir -p "$(ROOT)/build/out"
	@sudo mkarchiso -v -w "$(ROOT)/build/work-alpha02" -o "$(ROOT)/build/out" "$(ROOT)/build/profile"
	@$(PYTHON) "$(ROOT)/tools/hash_isos.py" create "$(ROOT)/build/out"
	@echo 'ISO build finished. See build/out/'

verify:
	@$(PYTHON) "$(ROOT)/tools/hash_isos.py" verify "$(ROOT)/build/out"

clean:
	@bash "$(ROOT)/scripts/clean.sh"
