CREATE TABLE `mentions` (
    `mid` int(11) NOT NULL,
    `user_id` bigint(20) NOT NULL,
    `name` varchar(255) NOT NULL,
    `screen_name` varchar(255) NOT NULL,
    PRIMARY KEY (`mid`),
    KEY `index2` (`user_id`),
    KEY `index3` (`name`),
    KEY `index4` (`screen_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
