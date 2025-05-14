build:
	rm -rf dist/
	make clean
	uv run builder/build_database.py
	cp models.db src/llm_mimetypes/data/models.db
	uv build

dev:
	make clean
	uv run builder/build_database.py
	cp models.db src/llm_mimetypes/data/models.db

clean:
	rm -f models.db
	rm -f src/llm_mimetypes/data/models.db
