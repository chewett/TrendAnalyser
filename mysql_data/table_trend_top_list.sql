CREATE TABLE `trend_top_list` (
    `trend_top_list_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `woeid` int(11) NOT NULL,
    `as_of` int(11) NOT NULL,
    `created_at` int(11) NOT NULL,
    PRIMARY KEY (`trend_top_list_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
