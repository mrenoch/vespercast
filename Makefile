.PHONY: help install install-backend install-frontend \
        run run-backend run-frontend \
        migrate makemigrations \
        shell check test \
        clean clean-db

# ── Geo library paths (Postgres.app GDAL) ─────────────────────────────────────
export PATH            := /Applications/Postgres.app/Contents/Versions/16/bin:$(PATH)
export GDAL_LIBRARY_PATH  := /Applications/Postgres.app/Contents/Versions/16/lib/libgdal.dylib
export GEOS_LIBRARY_PATH  := /Applications/Postgres.app/Contents/Versions/16/lib/libgeos_c.dylib
export PROJ_LIB           := /Applications/Postgres.app/Contents/Versions/16/share/proj
export DJANGO_SETTINGS_MODULE := config.settings.development

BACKEND  := backend
FRONTEND := frontend
MANAGE   := uv run python manage.py

help:
	@echo ""
	@echo "  VesperCast — available targets"
	@echo ""
	@echo "  Setup"
	@echo "    install           Install all backend + frontend dependencies"
	@echo "    install-backend   Install Python deps via uv"
	@echo "    install-frontend  Install Node deps via npm"
	@echo ""
	@echo "  Run"
	@echo "    run               Start backend (:8000) and frontend (:5173) together"
	@echo "    run-backend       Start Django dev server on :8000"
	@echo "    run-frontend      Start Vite dev server on :5173"
	@echo ""
	@echo "  Database"
	@echo "    migrate           Apply migrations"
	@echo "    makemigrations    Generate new migrations"
	@echo "    clean-db          Delete db.sqlite3 and re-migrate from scratch"
	@echo ""
	@echo "  Dev"
	@echo "    shell             Open Django shell"
	@echo "    check             Run Django system check"
	@echo "    test              Run backend tests"
	@echo "    clean             Remove Python caches and compiled files"
	@echo ""

# ── Install ───────────────────────────────────────────────────────────────────

install: install-backend install-frontend

install-backend:
	cd $(BACKEND) && uv sync

install-frontend:
	cd $(FRONTEND) && npm install

# ── Run ───────────────────────────────────────────────────────────────────────

run:
	@echo "Starting backend on :8000 and frontend on :5173 (Ctrl-C stops both)"
	@trap 'kill 0' INT; \
	  (cd $(BACKEND) && $(MANAGE) runserver) & \
	  (cd $(FRONTEND) && npm run dev) & \
	  wait

run-backend:
	cd $(BACKEND) && $(MANAGE) runserver

run-frontend:
	cd $(FRONTEND) && npm run dev

# ── Database ─────────────────────────────────────────────────────────────────

migrate:
	cd $(BACKEND) && $(MANAGE) migrate

makemigrations:
	cd $(BACKEND) && $(MANAGE) makemigrations

clean-db:
	rm -f $(BACKEND)/db.sqlite3
	cd $(BACKEND) && $(MANAGE) migrate

# ── Dev tools ────────────────────────────────────────────────────────────────

shell:
	cd $(BACKEND) && $(MANAGE) shell

check:
	cd $(BACKEND) && $(MANAGE) check

test:
	cd $(BACKEND) && $(MANAGE) test apps

clean:
	find $(BACKEND) -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find $(BACKEND) -name "*.pyc" -delete 2>/dev/null || true
