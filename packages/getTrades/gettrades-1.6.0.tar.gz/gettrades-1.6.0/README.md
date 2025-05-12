**getTrades v1.6**

Read trades and calculate overall profit/loss

 

usage: *python getTrades.py [option]*

where [option] can be:

| \-d      | delete a config section (asks for config number)                                                                                                |
|----------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| \-a      | add a config section                                                                                                                            |
| \-l      | list all config section and their numbers                                                                                                       |
| \-u [\#] | use a specific config section (by number found by -l option)                                                                                    |
| \-k      | (advanced) use saved resultset, don't query Bitvavo again                                                                                       |
|          | When no option is provided, a standard run will be executed, when more than one config excist, a config number is asked to run the program with |

 

Initial run will ask for API and Secret to api.bitvavo.com and store this
information encrypted in a config.ini file.

 

This will be the default and does not need to be specified further until there
are more than 1 configs
