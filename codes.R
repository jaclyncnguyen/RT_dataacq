top5 <- read.csv('top5.csv', header = TRUE)
head(top5)
library(ggplot2)

top5$'earndate' <- as.character(top5$earndate)
top5$earndate <- as.Date(as.character(top5$earndate), '%m/%d/%Y')
ggplot(top5, aes(x = earndate, y = earnings, colour = movie_title)) + geom_point() + geom_line() + labs(x = 'Date', y = 'Weekend Earnings', title = 'Weekend Earning Trends of Top 5 Movie')

