# SuperPy

### For this project I wish to assert the following.

#### Regarding the commands section:
Many abbreviations for the commands were implemented, which can greatly ease the operation speed of an experienced user.
The purchase section was implemented in such a way that several amounts could be added, with several expiry dates in the same purchase, such as to make the purchase of big bulks of the same item easier.
The sell and price functions were implemented with the possibility of giving only a name and afterwards selecting the ids as it is possible that a customer purchases the same item with different id's, due to the time of purchase or expiry date and so all instances of an item can be easily repriced. An amount check with the ability to offer alternatives of the same name has also been implemented to allow a sale even if only one id is remembered or simple human mistakes such as typing the wrong number of items are made.

#### Regarding the information handling
Despite having made a list that compiles a lot of information about the items and passes them onto a class, this list is mainly used for inventory as other date limitation considerations were taken for other types of report and to practice classes.
Simple functions were made to get valuable bits of information from a certain id or item. Also the ability to import files with different column names, and even diferent date formats supported which will be converted to the format used in the program.

#### Date wise, the date check and date range selection have been improved
The date check allows for the user to retrieve the last fictional date used if it was one other than the natural date at the last runtime, solving the problem of from one day to the other jumping to the current factual date and having to manually remember the last fictitious one.
Selecting a date range by only typing in a year, set of years or year-month, makes a report such as “all profit form xxxx year” much easier to request and includes the ability to have one date be a full date while another is only a year or year-month.
