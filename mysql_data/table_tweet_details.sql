CREATE TABLE `tweet_details` (
    `tweetId` bigint(20) NOT NULL,
    `negative` tinyint(3) unsigned DEFAULT '0',
    `positive` tinyint(3) unsigned DEFAULT '0',
    `created_at` int(11) DEFAULT NULL,
    PRIMARY KEY (`tweetId`),
    KEY `positive` (`positive` DESC),
    KEY `negative` (`negative` DESC)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
