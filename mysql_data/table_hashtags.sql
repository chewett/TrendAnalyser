CREATE  TABLE `trendanalyser`.`hashtags` (
    `hid` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
    `hashtag` VARCHAR(255) NOT NULL ,
    PRIMARY KEY (`hid`) ,
    UNIQUE INDEX `hashtag_UNIQUE` (`hashtag` ASC) )
ENGINE = MyISAM
DEFAULT CHARACTER SET = utf8;
