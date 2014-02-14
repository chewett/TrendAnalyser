CREATE TABLE `woeid_data` (
    `woeid` int(11) NOT NULL,
    `country` varchar(50) DEFAULT NULL,
    `countryCode` varchar(5) DEFAULT NULL,
    `name` varchar(50) DEFAULT NULL,
    `parentWoeid` int(11) DEFAULT NULL,
    `placeCode` int(11) DEFAULT NULL,
    `placeName` varchar(50) DEFAULT NULL,
    `url` varchar(254) DEFAULT NULL,
    PRIMARY KEY (`woeid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
