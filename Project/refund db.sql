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
-- Database: `refund`
--
CREATE DATABASE IF NOT EXISTS `refund` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `refund`;

DROP TABLE IF EXISTS `refund`;
CREATE TABLE IF NOT EXISTS `refund` (
  `refundPaymentID` INT NOT NULL AUTO_INCREMENT,
  `customerEmail` varchar(32) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `refundAmt` DECIMAL(10,2) NOT NULL,
  `phoneNum` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`refundPaymentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

Insert INTO `Refund` (`customerEmail`,`description`,`refundAmt`, `phoneNum`) VALUES
('jane.smith@example.com',"ClothesName", 193.97, '97986025');
COMMIT;