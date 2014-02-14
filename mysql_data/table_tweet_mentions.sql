CREATE TABLE `tweet_mentions` (
    `tweetId` bigint(20) NOT NULL,
    `user_id` int(11) unsigned NOT NULL,
    `name` varchar(150) NOT NULL,
    `screen_name` varchar(150) NOT NULL,
    PRIMARY KEY (`tweetId`,`user_id`),
    KEY `fk_tweet_mentions_1` (`tweetId`),
    CONSTRAINT `fk_tweet_mentions_1` FOREIGN KEY (`tweetId`) REFERENCES `tweet_details` (`tweetId`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
