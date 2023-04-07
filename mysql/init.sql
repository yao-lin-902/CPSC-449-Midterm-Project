CREATE DATABASE web;

use web;

CREATE TABLE IF NOT EXISTS `user` (
`id` int NOT NULL AUTO_INCREMENT,
`name` varchar(50) NOT NULL,
`username` varchar(50) NOT NULL,
`password` varchar(255) NOT NULL, PRIMARY KEY (`id`)
) ENGINE=InnODB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
