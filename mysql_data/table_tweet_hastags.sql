CREATE TABLE `tweet_hashtags` (
    `tweetId` bigint(20) NOT NULL,
    `hid` int(11) NOT NULL,
    PRIMARY KEY (`tweetId`,`hashtag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
