Various things I've written in Python.


*poloLendingBot*

A simple bot that autolends ETH out for margin traders on Poloniex at the next best rate.
Poloniex's autorenew loan feature renews your loan at whatever rate you offered it at previously,
which isn't optimal when the current rate is higher than your rate. This bot autorenews your loan
but adjusts your interest rate so that it gets you the best rate whilst ensuring your loan offer
has the best chance of getting accepted by a margin trader.

Makes use of this wrapper for the Poloniex API: https://pastebin.com/8fBVpjaj

*tradingbot*

An initial attempt at writing a bitcoin swing trading bot. But then I bought ETH and decided to hodl,
and ETH price skyrocketed, so this bot just kinda didn't go anywhere....

*gradeChecker*

A Math Prof I had uploaded grades as a static html page which was manually updated at sporadic times.
I wrote this script to run as a cron job on a raspberry pi to regularly check if the grades were updated.
The html page was hashed and the hash saved, and if it changed an email is sent out.
