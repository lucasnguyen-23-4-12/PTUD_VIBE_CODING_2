-- SQLite schema (reference). The app also creates tables automatically via SQLAlchemy.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS majors (
  major_id INTEGER PRIMARY KEY AUTOINCREMENT,
  major_name TEXT NOT NULL UNIQUE,
  description TEXT
);

CREATE TABLE IF NOT EXISTS readers (
  reader_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  class TEXT NOT NULL,
  birth_date TEXT NOT NULL, -- ISO date (YYYY-MM-DD)
  gender TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS book_titles (
  title_id INTEGER PRIMARY KEY AUTOINCREMENT,
  title_name TEXT NOT NULL,
  publisher TEXT NOT NULL,
  pages INTEGER NOT NULL,
  size TEXT NOT NULL,
  author TEXT NOT NULL,
  total_quantity INTEGER NOT NULL DEFAULT 0,
  major_id INTEGER NOT NULL,
  FOREIGN KEY (major_id) REFERENCES majors(major_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS book_copies (
  copy_id INTEGER PRIMARY KEY AUTOINCREMENT,
  title_id INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'available', -- available|borrowed
  import_date TEXT NOT NULL, -- ISO date (YYYY-MM-DD)
  FOREIGN KEY (title_id) REFERENCES book_titles(title_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS librarians (
  librarian_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL -- admin|librarian
);

CREATE TABLE IF NOT EXISTS borrow_records (
  borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
  copy_id INTEGER NOT NULL,
  reader_id INTEGER NOT NULL,
  librarian_id INTEGER NOT NULL,
  borrow_date TEXT NOT NULL, -- ISO date-time
  status TEXT NOT NULL DEFAULT 'borrowed', -- borrowed|returned
  FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id) ON DELETE RESTRICT,
  FOREIGN KEY (reader_id) REFERENCES readers(reader_id) ON DELETE RESTRICT,
  FOREIGN KEY (librarian_id) REFERENCES librarians(librarian_id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS ix_borrow_records_reader_status ON borrow_records(reader_id, status);
CREATE INDEX IF NOT EXISTS ix_borrow_records_copy_status ON borrow_records(copy_id, status);
CREATE INDEX IF NOT EXISTS ix_book_copies_title_status ON book_copies(title_id, status);

