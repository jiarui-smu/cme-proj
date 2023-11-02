-- this is the sql file for all the data
-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9




/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `customer`
--
Drop DATABASE IF EXISTS quikkarts;
CREATE DATABASE IF NOT EXISTS quikkarts DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE quikkarts;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` ( 
  `customerEmail` VARCHAR(255) NOT NULL PRIMARY KEY,
  `phoneNum` VARCHAR(20) NOT NULL,
  `bankNum` VARCHAR(20) NOT NULL,
  `homeAddress` VARCHAR(255) NOT NULL
);

--
-- Dumping data for table `clothes`
--

INSERT INTO `customer` (customerEmail, phoneNum, bankNum, homeAddress)
VALUES
('john.doe@example.com', '87880300', '1234567890123456', '123 Main St.'),
('jane.smith@example.com', '97986025', '9876543210987654', '456 Elm St.'),
('bob.johnson@example.com', '87279051', '1111222233334444', '789 Oak St.'),
('ahkao@gmail.com','90664833','1111222233335555','343 Queens st.');



DROP TABLE IF EXISTS `clothes`;
CREATE TABLE IF NOT EXISTS `clothes` (
  `clothesID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(80) NOT NULL,
  `cost` decimal(10,2) NOT NULL,
  `size` varchar(13) NOT NULL,
  `description` varchar(300) NOT NULL,
  `color` varchar(80) NOT NULL,
  `image` varchar(4000) NOT NULL,
  `isOnPromotion` BOOLEAN NOT NULL
  );
CREATE INDEX idx_clothes_name ON clothes(name);
CREATE INDEX idx_clothes_size ON clothes(size);
CREATE INDEX idx_clothes_color ON clothes(color);

--
-- Dumping data for table `clothes`
--

-- INSERT INTO `clothes` (`clothesID`, `size`, `name`, `desc`, `color`, `cost`, `isPromoted`) VALUES
-- ('1234567890123', 'S', 'Blue Shirt', 'Just a blue shirt', 'Blue', '21.40', FALSE);
-- COMMIT;
INSERT INTO `clothes` (`size`, `name`, `description`, `color`, `cost`, `image`, `isOnPromotion`) VALUES
('S', 'Blue Shirt', 'Just a blue shirt', 'Blue', 21.40, 'img/blueshirt.jpg', False),
('M', 'Red Shirt', 'Just a red shirt', 'Red', 21.40, 'img/redshirt.jpg', False),
('S', 'Short sleeve waffle shirt in true navy', 'Waffle-textured cotton: lightweight, soft and strong.', 'Navy', 29.99, 'img/waffle_navy_shirt.PNG',False),
('M', 'Slim fit cotton oxford shirt in burgundy', 'Cotton: lightweight, soft, strong and breathable', 'Burgundy', 45.99, 'img/slim_oxford_shirt.jpg',False),
('M', 'Lettuce edge t-shirt in white', 'Ribbed jersey: soft and stretchy', 'White', 21.99, 'img/lettuce_edge_shirt.PNG',True),
('L', 'Suny v neck t-shirt in black', 'Jersey: soft and stretchy', 'Black', 13.99, 'img/Black_V_NeckShirt.PNG',True),
('S', 'Cotton checkered shirt in cream', 'Cotton: lightweight, soft, strong and breathable', 'Cream', 16.99, 'img/Cotton_Checkered_Shirt.PNG', False),
('S', 'Cotton T-Shirt', 'A soft and comfortable t-shirt made of 100% cotton', 'White', 19.99, 'img/White_Shirt.PNG',True),
('M', 'Denim Jeans', 'Classic blue denim jeans for everyday wear', 'Blue', 49.99, 'img/Denim_Jeans.PNG',False),
('L', 'Leather Jacket', 'A stylish and durable leather jacket for colder weather', 'Black', 149.99, 'img/B_leather_Jacket.PNG' ,True),
('XL', 'Athletic Shorts', 'Breathable and flexible shorts for working out or playing sports', 'Red', 29.99, 'img/Red_Shorts.PNG', False);





DROP TABLE IF EXISTS `order1`; 
CREATE TABLE IF NOT EXISTS `order1` (
  `order_id` int(255) NOT NULL,
  `customerEmail` varchar(32) NOT NULL,
  `clothesID` int(255) NOT NULL,
  `clothesName` char(100) NOT NULL,
  `size` varchar(13) NOT NULL,
  `color` varchar(80) NOT NULL,
  `quantity` int(11) NOT NULL,
  `totalPrice` decimal(10,2) NOT NULL,
  `refundStatus` boolean NOT NULL,
  `transactionID` int(255) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  FOREIGN KEY (`customerEmail`) REFERENCES `customer`(`customerEmail`),
  FOREIGN KEY (`clothesID`) REFERENCES `clothes`(`clothesID`),
  FOREIGN KEY (`size`) REFERENCES `clothes`(`size`),
  FOREIGN KEY (`color`) REFERENCES `clothes`(`color`),
  FOREIGN KEY (`clothesName`) REFERENCES `clothes`(`name`)
  
); 
CREATE INDEX idx_order_id ON order1(order_id);
--
-- Dumping data for table `order`
--

INSERT INTO `order1` (`order_id`, `customerEmail`, `clothesID`, `clothesName`, `size`, `color`, `quantity`, `totalPrice`, `refundStatus`) VALUES
(1, 'ahkao@gmail.com', 1, 'Blue Shirt', 'S', 'Blue', 1, 30, False);



DROP TABLE IF EXISTS `invoice`;
CREATE TABLE IF NOT EXISTS `invoice` (
  `invoiceID` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `customerEmail` varchar(32) NOT NULL,
  `order_id` int(11) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `totalPrice` decimal(10,2) NOT NULL,
  `payMethod` VARCHAR(100) NOT NULL,
  `stripe_id` varchar(500) NOT NULL,
  FOREIGN KEY (`customerEmail`) REFERENCES `customer`(`customerEmail`),
  FOREIGN KEY (`order_id`) REFERENCES `order1` (`order_id`)
); 


