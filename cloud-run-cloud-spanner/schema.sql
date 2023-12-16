CREATE TABLE users (
	id STRING(32),
	username STRING(50)NOT NULL,
	password STRING(50) NOT NULL,
	email STRING(MAX) NOT NULL,
	created TIMESTAMP,
	updated TIMESTAMP
) PRIMARY KEY (id);

CREATE UNIQUE INDEX UsersUsername ON users(username) STORING(password);
