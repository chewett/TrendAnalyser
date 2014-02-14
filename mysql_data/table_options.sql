CREATE TABLE `options` (
    `key` varchar(255) NOT NULL,
    `value` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `options` (`key`,`value`) VALUES ('debug','false');
INSERT INTO `options` (`key`,`value`) VALUES ('offline','false');
INSERT INTO `options` (`key`,`value`) VALUES ('save_data_location','/home/user/tweet_data/');
INSERT INTO `options` (`key`,`value`) VALUES ('twitter_key_location','/home/user/twitter.json');
