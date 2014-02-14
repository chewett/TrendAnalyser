CREATE TABLE `tweet_mentions` (
    `tweetId` bigint(20) NOT NULL,
    `mid` int(11) unsigned NOT NULL,
    PRIMARY KEY (`tweetId`,`mid`),
    KEY `fk_tweet_mentions_1` (`tweetId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
