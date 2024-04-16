/* Create the database */
CREATE DATABASE  IF NOT EXISTS test_db;

/* Switch to the classicmodels database */
USE test_db;

/* Drop existing tables  */
DROP TABLE IF EXISTS Tests;


/* Create the tables */
CREATE TABLE Tests(
    TestId int AUTO_INCREMENT NOT NULL,
    TestName varchar(50) NOT NULL,
    PRIMARY KEY(TestId)
);

INSERT INTO Tests (TestId, TestName) VALUES
(1, 'Doc Test');