-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
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
-- Database: `clothes`
--
CREATE DATABASE IF NOT EXISTS `clothes` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `clothes`;

-- --------------------------------------------------------

--
-- Table structure for table `clothes`
--

DROP TABLE IF EXISTS `clothes`;
CREATE TABLE IF NOT EXISTS `clothes` (
  `clothesID` INT NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `cost` decimal(10,2) NOT NULL,
  `size` varchar(13) NOT NULL,
  `description` varchar(300) NOT NULL,
  `color` varchar(80) NOT NULL,
  `image` varchar(4000) NOT NULL,
  `isOnPromotion` BOOLEAN NOT NULL,
  PRIMARY KEY (`clothesID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

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

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
