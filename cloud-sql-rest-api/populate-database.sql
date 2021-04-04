CREATE TABLE breeds (
  name varchar(30) UNIQUE,
  type varchar(30),
  lifeExpectancy INT,
  origin varchar(30)
);

INSERT INTO breeds VALUES ('poodle', 'sporting', 14, 'Germany');
