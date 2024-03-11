
DROP TABLE passwords;
DROP TABLE users;

CREATE TABLE IF NOT EXISTS users (
  id_user INTEGER PRIMARY KEY AUTO_INCREMENT,
  master_user TEXT NOT NULL,
  master_email TEXT NOT NULL,
  master_password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS passwords (
  id_password INTEGER PRIMARY KEY AUTO_INCREMENT,
  id_user INTEGER NOT NULL,
  s_url_path TEXT NOT NULL,
  s_username TEXT NOT NULL,
  s_password TEXT NOT NULL,
  FOREIGN KEY (id_user) REFERENCES users(id_user)
);