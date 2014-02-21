CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `tweet_mentions_full` AS select `d`.`tweetId` AS `tweetId`,`d`.`negative` AS `negative`,`d`.`positive` AS `positive`,`d`.`created_at` AS `created_at`,`men`.`mid` AS `mid`,`men`.`user_id` AS `user_id`,`men`.`name` AS `name`,`men`.`screen_name` AS `screen_name` from ((`tweet_mentions` `m` left join `tweet_details` `d` on((`m`.`tweetId` = `d`.`tweetId`))) left join `mentions` `men` on((`men`.`mid` = `m`.`mid`)))
