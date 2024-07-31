/* Create the database */
CREATE DATABASE  IF NOT EXISTS demo_db;

/* Switch to the classicmodels database */
USE demo_db;

/* Drop existing tables  */
DROP TABLE IF EXISTS Roles;
DROP TABLE IF EXISTS Pages;
DROP TABLE IF EXISTS Permission;
DROP TABLE IF EXISTS EventRequestData;
DROP TABLE IF EXISTS EventRequestStatus; 

/* Create the tables */
CREATE TABLE Roles(
    RoleId int AUTO_INCREMENT NOT NULL,
    RoleName varchar(50) NOT NULL,
    PRIMARY KEY(RoleId)
);

CREATE TABLE Pages(PageId int AUTO_INCREMENT NOT NULL,
    PageName varchar(50) NOT NULL,
    PRIMARY KEY(PageId)
);

CREATE TABLE Permission(
    PermissionId int AUTO_INCREMENT NOT NULL,
    RoleID int NULL,PageID int NULL,
    CanView bit(1) NOT NULL,
    CanEdit bit(1) NOT NULL,
    PRIMARY KEY(PermissionId)
);

CREATE TABLE EventRequestData (
    EventId INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    EventDate DATETIME NOT NULL,
    StartTime TIME NOT NULL,
    EndTime TIME NOT NULL,
    AgentPartyId INT NOT NULL,
    PresentingProduct INT NOT NULL,
    SubmissionType varchar(50) NULL,
    Isremoved INT NOT NULL,
    RemovedBy INT NULL,
    RemovedDate DATETIME NULL,
    RequestedDate DATETIME NOT NULL,
    RequestedBy INT NOT NULL,
    Status INT NOT NULL,
    USCAdvertizing INT NOT NULL,
    StoreId INT NULL,
    LaguageID INT NULL,
    MSMRejectionComments TEXT NULL,
    Planyear varchar(50) NULL,
    Season varchar(50) NULL,
    RejectedBy INT NULL,
    RejectedDate DATETIME NULL,
    EventRequestedTo INT NULL,
    createdBy INT NOT NULL,
    ApprovedBY INT NULL,
    ApprovedDate DATETIME NULL,
    SendERAStatus INT NULL,
    EraResponseStatus varchar(50) NULL,
    EraSendDate DATETIME NULL
);


CREATE TABLE EventRequestStatus(
    StatusId int AUTO_INCREMENT NOT NULL,
    Status varchar(50) NULL,
    PRIMARY KEY(StatusId)
);

/* Inserting data  */
INSERT INTO Roles (RoleId, RoleName) VALUES
(1, 'Super Admin'),
(2, 'Admin'),
(3, 'SD'),
(4, 'MSM'),
(5, 'SVP'),
(6, 'VPS'),
(7, 'SD'),
(8, 'MSM');

INSERT INTO Pages (PageId, PageName) VALUES
(1, 'Others'),
(2, 'Geo Master'),
(3, 'Stores'),
(4, 'Users'),
(5, 'Agent Master List'),
(6, 'SD Market Assignment'),
(7, 'Agent Assignment'),
(8, 'Approve Event'),
(9, 'Assign Store'),
(10, 'Event Request'),
(11, 'View Resource Materials');

INSERT INTO Permission (PermissionId, RoleID, PageID, CanView, CanEdit) VALUES
(1, 1, 1, 0, 0),
(2, 1, 2, 0, 0),
(3, 1, 3, 0, 0),
(4, 1, 4, 0, 0),
(5, 1, 5, 0, 0),
(6, 1, 6, 0, 0),
(7, 1, 7, 0, 0),
(8, 1, 8, 0, 0),
(9, 1, 9, 0, 0),
(10, 1, 10, 0, 0),
(11, 1, 11, 0, 0),
(12, 2, 1, 0, 0),
(13, 2, 2, 0, 0),
(14, 2, 3, 0, 0),
(15, 2, 4, 0, 0),
(16, 2, 5, 0, 0),
(17, 2, 6, 0, 0),
(18, 2, 7, 0, 0),
(19, 2, 8, 0, 0),
(20, 2, 9, 0, 0),
(21, 2, 10, 0, 0),
(22, 2, 11, 0, 0),
(23, 3, 1, 0, 0),
(24, 3, 2, 0, 0),
(25, 3, 3, 0, 0),
(26, 3, 4, 0, 0),
(27, 3, 5, 0, 0),
(28, 3, 6, 0, 0),
(29, 3, 7, 1, 1),
(30, 3, 8, 1, 1),
(31, 3, 9, 1, 1),
(32, 3, 10, 0, 0),
(33, 3, 11, 1, 1),
(34, 4, 1, 0, 0),
(35, 4, 2, 0, 0),
(36, 4, 3, 0, 0),
(37, 4, 4, 0, 0),
(38, 4, 5, 0, 0),
(39, 4, 6, 0, 0),
(40, 4, 7, 1, 1),
(41, 4, 8, 1, 1),
(42, 4, 9, 1, 1),
(43, 4, 10, 0, 0),
(44, 4, 11, 1, 1),
(45, 5, 1, 1, 1),
(46, 5, 2, 1, 1),
(47, 5, 3, 1, 1),
(48, 5, 4, 1, 1),
(49, 5, 5, 1, 1),
(50, 5, 6, 0, 0),
(51, 5, 7, 1, 1),
(52, 5, 8, 1, 1),
(53, 5, 9, 1, 1),
(54, 5, 10, 0, 0),
(55, 5, 11, 1, 1),
(56, 6, 1, 0, 0),
(57, 6, 2, 0, 0),
(58, 6, 3, 0, 0),
(59, 6, 4, 0, 0),
(60, 6, 5, 0, 0),
(61, 6, 6, 0, 0),
(62, 6, 7, 0, 0),
(63, 6, 8, 0, 0),
(64, 6, 9, 0, 0),
(65, 6, 10, 1, 1),
(66, 6, 11, 1, 1),
(67, 7, 1, 0, 0),
(68, 7, 2, 0, 0),
(69, 7, 3, 0, 0),
(70, 7, 4, 1, 0),
(71, 7, 5, 0, 0),
(72, 7, 6, 0, 0),
(73, 7, 7, 0, 0),
(74, 7, 8, 0, 0),
(75, 7, 9, 0, 0),
(76, 7, 10, 0, 0),
(77, 7, 11, 1, 1),
(78, 8, 1, 1, 1),
(79, 8, 2, 1, 1),
(80, 8, 3, 1, 1),
(81, 8, 4, 1, 1),
(82, 8, 5, 1, 1),
(83, 8, 6, 1, 1),
(84, 8, 7, 1, 1),
(85, 8, 8, 1, 1),
(86, 8, 9, 1, 1),
(87, 8, 10, 0, 0),
(88, 8, 11, 1, 1);

INSERT INTO EventRequestStatus (StatusId, Status) VALUES
(1, 'Pending'),
(2, 'Approved'),
(3, 'Removed'),
(4, 'Cancelled'),
(5, 'Rejected'),
(6, 'RemoveAfterEraSend'),
(7, 'RejectAfterEraSend');

INSERT INTO EventRequestData (EventId, EventDate, StartTime, EndTime, AgentPartyId, PresentingProduct, SubmissionType, Isremoved, RemovedBy, RemovedDate, RequestedDate, RequestedBy, Status, USCAdvertizing, StoreId, LaguageID, MSMRejectionComments, Planyear, Season, RejectedBy, RejectedDate, EventRequestedTo, createdBy, ApprovedBY, ApprovedDate, SendERAStatus, EraResponseStatus, EraSendDate) VALUES
(32235, '2023-10-31 00:00:00.000', '15:00:00', '19:00:00', 636873, 2, NULL, 0, NULL, NULL, '2023-10-25 03:36:07.610', 636873, 1, 1, 1942246541, 1, NULL, 2024, 'AEP', NULL, NULL, 689300, 636873, NULL, NULL, 0, NULL, NULL),
(32234, '2023-10-31 00:00:00.000', '13:00:00', '17:00:00', 690149, 1, NULL, 0, NULL, NULL, '2023-10-24 22:18:54.140', 690149, 2, 0, 1265461297, 1, NULL, 2024, 'AEP', NULL, NULL, 2829552, 690149, 2829552, '2023-10-24 22:20:05.530', 2, 'Success', '2023-10-25 09:45:08.377'),
(32233, '2023-10-31 00:00:00.000', '13:00:00', '17:00:00', 690397, 1, NULL, 0, NULL, NULL, '2023-10-24 22:17:39.890', 690397, 2, 0, 1811926843, 1, NULL, 2024, 'AEP', NULL, NULL, 2829552, 690397, 2829552, '2023-10-24 22:20:05.500', 2, 'Success', '2023-10-25 09:45:08.377'),
(32232, '2023-10-31 00:00:00.000', '09:00:00', '13:00:00', 533024, 1, NULL, 0, NULL, NULL, '2023-10-24 22:16:43.527', 533024, 2, 0, 1811926843, 1, NULL, 2024, 'AEP', NULL, NULL, 2829552, 533024, 2829552, '2023-10-24 22:20:05.453', 2, 'Success', '2023-10-25 09:45:08.377'),
(32231, '2023-11-03 00:00:00.000', '10:00:00', '15:00:00', 727127, 1, NULL, 0, NULL, NULL, '2023-10-24 18:04:31.403', 727127, 1, 0, 1831104926, 1, NULL, 2024, 'AEP', NULL, NULL, 568045, 727127, NULL, NULL, 0, NULL, NULL);

