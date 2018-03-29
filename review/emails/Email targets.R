library(readr)
setwd("~/Desktop/Momentum/email_targets/")

# read the target export from NationBuilder
targets <- read_csv("membersopenedemailsorvrecent.csv")

# keep the email addresses
emails <- na.omit(targets[,c('email')])

# trim commas from emails to avoid breaking the CSV
emails$email <- trimws(gsub(",", "", emails$email))

# output the CSV
write_csv(emails, "targets.csv", col_names = F)
