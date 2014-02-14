CREATE TABLE `trend_top_list_trends` (
    `trend_top_list_id` int(10) unsigned NOT NULL,
    `name` varchar(45) NOT NULL,
    `events` varchar(45) NOT NULL DEFAULT '',
    `promoted_content` varchar(45) NOT NULL DEFAULT '',
    PRIMARY KEY (`trend_top_list_id`,`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
