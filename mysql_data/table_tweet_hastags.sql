CREATE TABLE `tweet_hashtags` (
    `tweetId` bigint(20) NOT NULL,
    `hid` int(11) NOT NULL,
    PRIMARY KEY (`tweetId`,`hid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
