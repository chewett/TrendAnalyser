CREATE TABLE `trend_top_list` (
    `trend_top_list_id` int(10) unsigned NOT NULL,
    `woeid` int(11) NOT NULL DEFAULT '0',
    `as_of` varchar(45) NOT NULL DEFAULT '',
    `created_at` varchar(45) NOT NULL DEFAULT '',
    PRIMARY KEY (`trend_top_list_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

