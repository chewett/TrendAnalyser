CREATE TABLE `tweet_hashtags` (
    `tweetId` bigint(20) NOT NULL,
    `hashtag` varchar(180) NOT NULL,
    PRIMARY KEY (`tweetId`,`hashtag`),
    CONSTRAINT `tweet_id` FOREIGN KEY (`tweetId`) REFERENCES `tweet_details` (`tweetId`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
