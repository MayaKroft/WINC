# Imports
import argparse
import csv
from datetime import date, datetime
from sys import stderr
import getdate
import textwrap
import doc_handler
from rich.console import Console
# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    getdate.run_date_check()

    #----------------GLOBAL VARIABLES----------------#
    SYSTEM_TIME= getdate.retrieve()
    YESTERDAY = getdate.yesterday()
    TOMORROW = getdate.tomorrow()



    #-----------------------------CUSTOM CHECKERS------------------------------#
    def all_dates(i):
        try:
            return datetime.strptime(i, '%Y-%m-%d').date()   
        except ValueError:
            raise Exception('One or more of the given dates is not in a YYYY-MM-DD format')
    
    def valid_id(id, date):
        id = int(id) if not isinstance(id, int) else id
        try: 
            valid = doc_handler.is_valid_id(id, date)
            return valid
        except ValueError:
            raise Exception('This item does not yet exist')
    #RAISES FALSE NEGATIVE
    
    def valid_item(item, date):
        try: 
            valid = doc_handler.is_valid_item(item, date)
            return valid
        except ValueError:
            stderr('This item does not yet exist')
    
   

    #-----------------------------PARSER DECLARATION---------------------------#
    super_parser = argparse.ArgumentParser(prog='SuperPy', formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            SuperPy will optimize the inventory and 
            profits management of your store!
            --------------------------------
                It's features include:
                    Date setting and andvancement
                    Profit reports based on date or item
                    Bulk item registration under one id or multiple
                    Expiration date management
                    Detailed inventory reports
            '''))
    subparser = super_parser.add_subparsers(dest = "command")


    #-----------ARGUMENTS NEEDED--------------
    # SHOW TIME
    # ADVANCE TIME
    # RETROCEDE TIME
    # BUY
    # SELL
    # SET PRICE
    # REPORT
    # ---INVENTORY
    # ---EXPIRED
    # ---NOT EXPIRED
    # ---EARNINGS 
    # ---EFECTIVITY
    # ---ITEMS NAMED
    # IMPORT FILE
    # EXPORT FILE
    #
    #my_group = super_parser.add_mutually_exclusive_group(required=False)


    #--------------------------TIME COMMANDS SECTION --------------------------#
    super_parser.add_argument(
        '-at', '--advance-time',
        type=int,
        help="advance the system date by x days or retrocede by -x days")
    super_parser.add_argument(
        '-st', '--system-time',
        action='store_true',
        help="show the current date the system has been set to")
    super_parser.add_argument(
        '-today', '--set-time-to-current',
        action='store_true',
        help="It will reset the date to the current date")

    #--------------------------- DOCUMENT ACTIONS --------------------------#   
    file_subparser = subparser.add_parser('file', help= 'Manage your program files here')
    file_subparser.add_argument(
        '-fa', '--file_action',
        choices=['wipe', 'backup', 'export', 'import'],
        help= 'Which action should be fullfilled')
    file_subparser.add_argument(
        '-fn', '--csv_name',
        choices=['purchased.csv', 'sold.csv', 'prices.csv'],
        help= 'Which data file should be handled')
    file_subparser.add_argument(
        '-et', '--export_type',
        choices=['xlsx','json','csv'],
        help= 'The file type the export will happen to')
    file_subparser.add_argument(
        '-en', '--file_name',
        help= 'The file name for the exported or imported file')
    file_subparser.add_argument(
        '-ia', '--import_action',
        choices=['append', 'overwrite'],
        help= 'wether the information will be added to the existing files or replacing it')


    #--------------------------BUY COMMANDS SECTION----------------------------#
    buy_subparser = subparser.add_parser('buy', help= 'add a new item to the bought inventory')
    buy_subparser.add_argument(
        '-n', '--product-name',
        help = 'the name of the product eg. orange',
        required= True)
    buy_subparser.add_argument(
        '-a', '--amount',
        help = 'number of units purchased',
        nargs= '*',
        type= int,
        default= 1)
    buy_subparser.add_argument(
        '-bp', '--buy-price',
        help= 'the price the item was bought for',
        type= float,
        required= True)
    buy_subparser.add_argument(
        '-bd', '--buy-date',
        help= 'the date the item was bought on',
        type= all_dates,
        default= SYSTEM_TIME)
    buy_subparser.add_argument(
        '-e', '--expiration-date',
        help= 'the expiration date of the bought item',
        type= all_dates,
        nargs= '*',
        default= '0000-00-00')
    buy_subparser.add_argument(
        '-sp', '--sell-price',
        type= float,
        help= 'the price the item will be sold for')

    #--------------------------SELL COMMANDS SECTION---------------------------#
    sell_subparser = subparser.add_parser('sell', help= 'register a new sale')
    sell_group = sell_subparser.add_mutually_exclusive_group(required=True)
    sell_group.add_argument(
        '-i', '--item',
        help = 'the name of the product')
    sell_group.add_argument(
        '-id', '--item_id',
        help = 'the id of the product',
        type= int)
    sell_subparser.add_argument(
        '-d', '--date',
        help = 'will set the date the sale should be assigned to',
        type= all_dates,
        default= SYSTEM_TIME)
    sell_subparser.add_argument(
        '-a', '--amount',
        help = 'number of units sold',
        type= int,
        default= 1)
    sell_subparser.add_argument(
        '-p', '--price',
        help = 'will set the price of the product of that id or retrieve the latest price',
        type= float)

    #-----------------------SET PRICE COMMANDS SECTION-------------------------#
    price_subparser = subparser.add_parser('price', help= 'Set or modify the price of an item')
    price_group = price_subparser.add_mutually_exclusive_group(required=True)
    price_group.add_argument(
        '-i', '--item',
        help = 'the name of the product')
    price_group.add_argument(
        '-id', '--item_id',
        help = 'the id of the product',
        type= int)
    price_subparser.add_argument(
        '-p', '--price',
        help = 'will set the price of the product of that id or name',
        type = float,
        required= True)
    price_subparser.add_argument(
        '-d', '--date',
        help = 'will set the date the price should be assigned to',
        type= all_dates,
        required= False,
        default= SYSTEM_TIME)


    #-----------------REPORT COMMANDS SECTION----------------#
    report_subparser = subparser.add_parser('report', help= 'will create reports on inventory, expired items, profit and revenue')
    # report_subparser.set_defaults(command = 'report')
    report_subparser.add_argument(
        'type',
        help = 'Generates a report of the selected type',
        choices=['inventory', 'i', 'expired', 'e', 'profit', 'p', 'revenue', 'r', 'item', 'id'])
    report_date_group = report_subparser.add_mutually_exclusive_group(required=False)
    report_date_group.add_argument(
        '-y', '--yesterday',
        help = 'Will generate the report of the day previous to the system time',
        action='store_true',)
    report_date_group.add_argument(
        '-t', '--today',
        help = 'Will generate the report of the current systen time day',
        action='store_true',)
    report_date_group.add_argument(
        '-tw', '--tomorrow',
        help = 'Will generate the report of the day that follows the system time',
        action='store_true',)
    report_date_group.add_argument(
        '-d', '--date',
        help = 'Generates a report for the given time, wether it be a single date, month, year or a range between two dates',
        nargs= '*',)
    report_subparser.add_argument(
        '-v', '--verbosity',
        help= '0 will simplify the report, 1 is the default, 2 will make the report more complex',
        choices=[0, 1, 2],
        type= int,
        default= 1)
    report_subparser.add_argument(
        '-pn', '--product_name',
        help= 'Name of the item of which the history is to be retrieved')
    report_subparser.add_argument(
        '-pi', '--product_id',
        help= 'ID of the item of which the history is to be retrieved',
        type= int)
    report_subparser.add_argument(
        '--save',
        help= 'to what format do you with to save the file',
        choices=['xlsx','json','csv'])




    #-----------------------------ARGUMENT HANDLING----------------------------#
    args = super_parser.parse_args()

    #make it so when running systemtime is always tooday, make command to go to last modified date
    if args.system_time:
        print ('The system is currently at {}'.format(SYSTEM_TIME))
    elif args.advance_time:
        current_date = getdate.makedate(SYSTEM_TIME, args.advance_time)
        print ('The new date is:  {}'.format(current_date))
    elif args.set_time_to_current:
        current_date = getdate.makedate(datetime.today(), 0)
        print ('The system is currently at {}'.format(SYSTEM_TIME))
        

    if args.command == 'buy':
        if len(args.amount) == len(args.expiration_date):
            doc_handler.buy(product_name= args.product_name, amount= args.amount, buy_date= args.buy_date, buy_price= args.buy_price, expiration_date= args.expiration_date, sell_price= args.sell_price)
        else: 
            print('If there are multiple amounts you need to supply the same amout of dates and vice-versa')

    elif args.command == 'sell':
        if args.item:
            if valid_item(args.item,args.date):
                doc_handler.sell(args.date, args.amount, args.price, item= args.item)
            elif valid_item(args.item, date.today()):
                print('This item did not exist in the given sell date')
            else:
                print('This item does not exist')
        elif args.item_id:
            if valid_id(args.item_id, args.date):
                doc_handler.sell(args.date, args.amount, args.price, id= args.item_id)
            elif valid_id(args.item_id, date.today()):
                print('This item did not exist in the given sell date')
            else:
                print('This item doe snot exist')

    elif args.command == 'price':
        #add checking that the date is a valid format, and that the price consists of numbers
        doc_handler.set_price(args.item, args.price, args.date)

    elif args.command == 'report':
        console = Console()
        if args.today:
            report_date = SYSTEM_TIME
            report_end = SYSTEM_TIME
        elif args.yesterday:
            report_date = YESTERDAY
            report_end = YESTERDAY
        elif args.tomorrow:
            report_date = TOMORROW
            report_end = TOMORROW
        elif args.date:
            report_dates = getdate.get_date_range(args.date)
            report_date = report_dates[0]
            report_end = report_dates[1]
        else:
            report_date = 0
            report_end = SYSTEM_TIME
        
        if args.type == 'inventory' or args.type == 'i':
            r_table = doc_handler.report_inventory(report_date, report_end, args.verbosity)
            console.print(r_table)
        
        elif args.type == 'expired' or  args.type == 'e':
            r_table = doc_handler.report_expired(report_date, report_end, args.verbosity)
            console.print(r_table)

        elif args.type == ('profit' or 'p'):
            r_table = doc_handler.report_profit(report_date, report_end, args.verbosity)
            console.print(r_table)
        elif args.type == ('revenue' or 'r'):
            r_table = doc_handler.report_revenue(report_date, report_end, args.verbosity)
            console.print(r_table)
        elif args.type == 'item':
            if valid_item(args.product_name, report_end):
                r_table = doc_handler.report_item(report_date, report_end, args.verbosity, item = args.product_name)
                console.print(r_table)
            else:
                raise Exception('Please select a valid item within the date range')
        elif args.type == 'id':
            if valid_id(args.product_id, report_end):
                r_table = doc_handler.report_item(report_date, report_end, args.verbosity, id = args.product_id)
                console.print(r_table)
            else:
                raise Exception('Please select a valid ID within the date range')
        if args.save:
            saved_doc = doc_handler.save(args.save, r_table, SYSTEM_TIME)
            console.print(f'Your report was saved as {saved_doc}')

    elif args.command == 'file':
        if args.file_action == 'wipe':
            doc_handler.wipe_csv_(args.csv_name)  
        elif args.file_action == 'backup':
            doc_handler.backup(args.csv_name)
        elif args.file_action == 'export':
            if args.export_name:
                doc_handler.export(args.csv_name, SYSTEM_TIME, args.export_type, args.file_name)
            else:
                doc_handler.export(args.csv_name, SYSTEM_TIME, args.export_type)
        elif args.file_action == 'import':
            if args.import_action == 'append':
                doc_handler.import_data(args.file_name, args.csv_name, append= True)
            elif args.import_action == 'overwrite':
                doc_handler.import_data(args.file_name, args.csv_name, overwrite= True)

            

if __name__ == "__main__":
    main()
