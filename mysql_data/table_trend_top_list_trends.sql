CREATE TABLE `trend_top_list_trends` (
    `trend_top_list_id` int(10) unsigned NOT NULL,
    `name` varchar(45) NOT NULL,
    `events` varchar(45) NOT NULL DEFAULT '',
    `promoted_content` varchar(45) NOT NULL DEFAULT '',
    PRIMARY KEY (`trend_top_list_id`,`name`),
    CONSTRAINT `trend_top_list_id` FOREIGN KEY (`trend_top_list_id`) REFERENCES `trend_top_list` (`trend_top_list_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
