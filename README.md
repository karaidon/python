Various things I've written in Python.


*poloLendingBot*

A simple bot that autolends ETH out for margin traders on Poloniex at the next best rate.
Poloniex's autorenew loan feature renews your loan at whatever rate you offered it at previously,
which isn't optimal when the current rate is higher than your rate. This bot autorenews your loan
but adjusts your interest rate so that it gets you the best rate whilst ensuring your loan offer
has the best chance of getting accepted by a margin trader.

Makes use of this wrapper for the Poloniex API: https://pastebin.com/8fBVpjaj

*tradingbot*

An initial attempt at writing a bitcoin trading bot. But then I bought ETH and decided to hodl,
and ETH price skyrocketed, so this bot just kinda didn't go anywhere....
