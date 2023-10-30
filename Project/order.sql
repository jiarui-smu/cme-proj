-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 12, 2020 at 02:17 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `order`
--
CREATE DATABASE IF NOT EXISTS `order1` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `order1`;

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

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
  `transactionID` int(255) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`transactionID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `order`
--

INSERT INTO `order1` (`order_id`, `customerEmail`, `clothesID`, `clothesName`, `size`, `color`, `quantity`, `totalPrice`, `refundStatus`) VALUES
(0, 'test@gmail.com', 0, 'test', 's', 'test', 1, 1.0, False);
COMMIT;
-- --------------------------------------------------------

--
-- Table structure for table `order_item`
--

-- DROP TABLE IF EXISTS `order_item`;
-- CREATE TABLE IF NOT EXISTS `order_item` (
--   `item_id` int(11) NOT NULL AUTO_INCREMENT,
--   `order_id` int(11) NOT NULL,
--   `book_id` char(13) NOT NULL,
--   `quantity` int(11) NOT NULL,
--   PRIMARY KEY (`item_id`),
--   KEY `FK_order_id` (`order_id`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `order_item`
--

-- INSERT INTO `order_item` (`item_id`, `order_id`, `book_id`, `quantity`) VALUES
-- (1, 1, '9781434474234', 1),
-- (2, 1, '9781449474212', 1);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `order_item`
--
-- ALTER TABLE `order_item`
--   ADD CONSTRAINT `FK_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE;
-- COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
