# Imports
import argparse
import os
import csv
from datetime import date, datetime
from sys import stderr
import getdate
import textwrap
import doc_handler
from rich.console import Console
from rich.text import Text
from to_from_ymd import to_ymd

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    getdate.run_date_check() #This will check if the previous date the program was run the last date used was a fictional one, if so, it will give the option to remain in in or change to the current date

    #----------------GLOBAL VARIABLES----------------#
    SYSTEM_TIME= getdate.retrieve()
    YESTERDAY = getdate.yesterday()
    TOMORROW = getdate.tomorrow()
    FILE_EXTS = ['xlsx','json','csv']
    CSV_CHOICES = ['bought.csv', 'sold.csv', 'prices.csv']
    CONSOLE = Console()


    #-----------------------------CUSTOM CHECKERS------------------------------#
    def all_dates(i):
        if isinstance(i, list):
            for d in i:
                try:
                    return datetime.strptime(d, '%Y-%m-%d').date()   
                except ValueError:
                    raise Exception('One or more of the given dates is not in a YYYY-MM-DD format')

        else:
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

    def file_path(string):
        if os.path.isfile(string):
            return string
        else:
            raise NotADirectoryError(string)

    #-----------------------------PARSER DECLARATION---------------------------#
    super_parser = argparse.ArgumentParser(prog='SuperPy', formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
                   'Welcome to Superpy!'
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


    #--------------------------TIME COMMANDS SECTION --------------------------#
    super_parser.add_argument(
        '-at', '--advance-time',
        type=int,
        metavar= '',
        help="Advance the system date by x days or retrocede by -x days")
    super_parser.add_argument(
        '-st', '--system-time',
        action='store_true',
        help="Show the current date the system has been set to")
    super_parser.add_argument(
        '-reset', '--set-time-to-current',
        action='store_true',
        help="Reset the date to the current date")


    #--------------------------- DOCUMENT ACTIONS --------------------------# 
    export_subparser = subparser.add_parser('export', help= 'Exports a program file to the given file format and name with the date of creation', formatter_class=argparse.RawTextHelpFormatter)  
    export_subparser.add_argument(
        '-csv', '--csv-name',
        choices=CSV_CHOICES,
        required= True,
        metavar= '',
        help= textwrap.dedent(f"""\
            The csv file that should be handled
            Choose from: {CSV_CHOICES}"""))
    export_subparser.add_argument(
        '-et', '--export-type',
        choices= FILE_EXTS,
        required= True,
        metavar= ' ',
        help= textwrap.dedent(f"""\
        The file type the export will happen to;
        choose from: {FILE_EXTS}"""))
    export_subparser.add_argument(
        '-fn', '--file-name',
        metavar = ' ',
        help= 'The file name for the exported file, optional')

    import_subparser = subparser.add_parser('import', help= 'Imports a given file to the program files', formatter_class=argparse.RawTextHelpFormatter)
    import_subparser.add_argument(
        '-csv', '--csv-name',
        choices= CSV_CHOICES,
        required= True,
        metavar= '',
        help= textwrap.dedent(f"""\
            The csv file that should be handled
            Choose from {CSV_CHOICES}"""))
    import_subparser.add_argument(
        '-fn', '--file-name',
        required = True,
        type= file_path,
        metavar= '',
        help= 'The file path to the imported file')
    import_subparser.add_argument(
        '-ia', '--import-action',
        choices=['append', 'overwrite'],
        metavar= '',
        help= textwrap.dedent("""\
            Wether the information will be added to the existing files or replacing it
            choose from ['append', 'overwrite']"""))

    file_subparser = subparser.add_parser('file', help= 'Manage your program files here', formatter_class=argparse.RawTextHelpFormatter)
    file_subparser.add_argument(
        '-fa', '--file-action',
        choices=['wipe', 'backup'],
        metavar= '',
        help= textwrap.dedent("""\
            Which action should be fullfilled;
            choose from: ['wipe', 'backup']"""))
    file_subparser.add_argument(
        '-csv', '--csv-name',
        choices=CSV_CHOICES,
        metavar= '',
        help= textwrap.dedent(f"""\
            Which data file should be handled;
            choose from: {CSV_CHOICES}"""))


    #--------------------------BUY COMMANDS SECTION----------------------------#
    buy_subparser = subparser.add_parser('buy', help= 'Add a new item to the bought inventory', formatter_class=argparse.RawTextHelpFormatter)
    buy_subparser.add_argument(
        '-n', '--product-name',
        help = 'The name of the product eg. orange',
        metavar= '',
        required= True)
    buy_subparser.add_argument(
        '-a', '--amount',
        help = 'Number of units bought',
        nargs= '*',
        type= int,
        metavar= '',
        default= [1])
    buy_subparser.add_argument(
        '-bp', '--buy-price',
        help= 'The price the item was bought for',
        type= float,
        metavar= '',
        required= True)
    buy_subparser.add_argument(
        '-bd', '--buy-date',
        help= 'The date the item was bought on',
        type= all_dates,
        metavar= '',
        default= SYSTEM_TIME)
    buy_subparser.add_argument(
        '-e', '--expiration-date',
        help= 'The expiration date of the bought item',
        type= all_dates,
        nargs= '*',
        metavar= '',
        default= [to_ymd('3000-01-01')])
    buy_subparser.add_argument(
        '-sp', '--sell-price',
        type= float,
        metavar= '',
        help= 'The price the item will be sold for')

    #--------------------------SELL COMMANDS SECTION---------------------------#
    sell_subparser = subparser.add_parser('sell', help= 'register a new sale', formatter_class=argparse.RawTextHelpFormatter)
    sell_group = sell_subparser.add_mutually_exclusive_group(required=True)
    sell_group.add_argument(
        '-n', '--product-name',
        metavar= '',
        help = 'The name of the product')
    sell_group.add_argument(
        '-id', '--item-id',
        metavar= '',
        help = 'The id of the product',
        type= int)
    sell_subparser.add_argument(
        '-d', '--date',
        help = 'Will set the date the sale should be assigned to',
        type= all_dates,
        metavar= '',
        default= SYSTEM_TIME)
    sell_subparser.add_argument(
        '-a', '--amount',
        help = 'Wumber of units sold',
        type= int,
        metavar= '',
        default= 1)
    sell_subparser.add_argument(
        '-p', '--price',
        metavar= '',
        help = 'Will set the price of the product of that id or retrieve the latest price',
        type= float)

    #-----------------------SET PRICE COMMANDS SECTION-------------------------#
    price_subparser = subparser.add_parser('price', help= 'Set or modify the price of an item', formatter_class=argparse.RawTextHelpFormatter)
    price_group = price_subparser.add_mutually_exclusive_group(required=True)
    price_group.add_argument(
        '-n', '--product-name',
        metavar= '',
        help = 'The name of the product')
    price_group.add_argument(
        '-id', '--item-id',
        metavar= '',
        help = 'The id of the product',
        type= int)
    price_subparser.add_argument(
        '-p', '--price',
        metavar= '',
        help = 'Will set the price of the product of that id or name',
        type = float,
        required= True)
    price_subparser.add_argument(
        '-d', '--date',
        metavar= '',
        help = 'Will set the date the price should be assigned to',
        type= all_dates,
        required= False,
        default= SYSTEM_TIME)


    #-----------------REPORT COMMANDS SECTION----------------#
    report_subparser = subparser.add_parser('report', help= 'will create reports on inventory, expired items, profit and revenue', formatter_class=argparse.RawTextHelpFormatter)
    # report_subparser.set_defaults(command = 'report')
    report_subparser.add_argument(
        'type',
        help = 'Generates a report of the selected type',
        choices=['inventory', 'i', 'expired', 'e', 'profit', 'p', 'revenue', 'r', 'name', 'id'])
    report_start_group = report_subparser.add_mutually_exclusive_group(required=False)
    report_start_group.add_argument(
        '-y', '--yesterday',
        help = 'Will generate the report of the day previous to the system time',
        action='store_true',)
    report_start_group.add_argument(
        '-t', '--today',
        help = 'Will generate the report of the current systen time day',
        action='store_true',)
    report_start_group.add_argument(
        '-tw', '--tomorrow',
        help = 'Will generate the report of the day that follows the system time',
        action='store_true',)
    report_start_group.add_argument(
        '-d', '--date',
        metavar= '',
        help = 'Generates a report for the given time, wether it be a single date, month, year or a range between two dates',
        nargs= '*',)
    report_subparser.add_argument(
        '-v', '--verbosity',
        metavar= '',
        help= '0 will simplify the report, 1 is the default, 2 will make the report more complex',
        choices=[0, 1, 2],
        type= int,
        default= 1)
    report_subparser.add_argument(
        '-n', '--product-name',
        metavar= '',
        help= 'Name of the item of which the history is to be retrieved')
    report_subparser.add_argument(
        '-id', '--product-id',
        metavar= '',
        help= 'ID of the item of which the history is to be retrieved',
        type= int)
    report_subparser.add_argument(
        '--save',
        metavar= '',
        help= textwrap.dedent(f"""\
        Format to which you wish to save the file;
        choose from: {FILE_EXTS}"""),
        choices=FILE_EXTS)


    #-----------------------------ARGUMENT HANDLING----------------------------#
    args = super_parser.parse_args()

    if args.system_time:
        CONSOLE.print ('The system is currently at {}'.format(SYSTEM_TIME))
    elif args.advance_time:
        current_date = getdate.makedate(SYSTEM_TIME, args.advance_time)
        SYSTEM_TIME = current_date
        CONSOLE.print ('The new date is:  {}'.format(current_date))
    elif args.set_time_to_current:
        current_date = getdate.makedate(datetime.today(), 0)
        SYSTEM_TIME = current_date
        CONSOLE.print ('The system is currently at {}'.format(SYSTEM_TIME))
        
    if args.command == 'buy':
        if len(args.amount) == len(args.expiration_date):
            for x,i in enumerate(args.amount):
                doc_handler.buy(product_name= args.product_name, amount= i, buy_date= args.buy_date, buy_price= args.buy_price, expiration_date= args.expiration_date[x], sell_price= args.sell_price)
            CONSOLE.print('Action completed')
        else: 
            CONSOLE.print('If there are multiple amounts you need to supply the same amout of dates and vice-versa')
        

    elif args.command == 'sell':
        if args.product_name:
            if valid_item(args.product_name,args.date):
                doc_handler.sell(args.date, args.amount, args.price, item= args.product_name)
            elif valid_item(args.product_name, date.today()):
                CONSOLE.print('This item did not exist in the given sell date')
            else:
                CONSOLE.print('This item does not exist')
        elif args.item_id:
            if valid_id(args.item_id, args.date):
                doc_handler.sell(args.date, args.amount, args.price, id= args.item_id)
            elif valid_id(args.item_id, date.today()):
                CONSOLE.print('This item did not exist in the given sell date')
            else:
                CONSOLE.print('This item does not exist')
        

    elif args.command == 'price':
        id = args.item_id if args.item_id else False
        item = args.product_name if args.product_name else False
        doc_handler.set_price(args.price, args.date, id= id, item= item)

    elif args.command == 'report':
        
        if args.today:
            report_start = SYSTEM_TIME
            report_end = SYSTEM_TIME
        elif args.yesterday:
            report_start = YESTERDAY
            report_end = YESTERDAY
        elif args.tomorrow:
            report_start = TOMORROW
            report_end = TOMORROW
        elif args.date:
            report_dates = getdate.get_date_range(args.date)
            report_start = report_dates[0]
            report_end = report_dates[1]
        else:
            report_start = 0
            report_end = SYSTEM_TIME
        
        if args.type == 'inventory' or args.type == 'i':
            r_table = doc_handler.report_inventory(report_start, report_end, args.verbosity)
            CONSOLE.print(r_table)
        
        elif args.type == 'expired' or  args.type == 'e':
            r_table = doc_handler.report_expired(report_start, report_end, args.verbosity)
            CONSOLE.print(r_table)

        elif args.type == 'profit' or args.type == 'p':

            r_table = doc_handler.report_profit(report_start, report_end, args.verbosity)
            CONSOLE.print(r_table)
        elif args.type == 'revenue' or args.type == 'r':
            r_table = doc_handler.report_revenue(report_start, report_end, args.verbosity)
            CONSOLE.print(r_table)
        elif args.type == 'name':
            if valid_item(args.product_name, report_end):
                r_table = doc_handler.report_item(report_start, report_end, args.verbosity, item = args.product_name)
                CONSOLE.print(r_table)
            else:
                raise Exception('Please select a valid item within the date range')
        elif args.type == 'id':
            if valid_id(args.product_id, report_end):
                r_table = doc_handler.report_item(report_start, report_end, args.verbosity, id = args.product_id)
                CONSOLE.print(r_table)
            else:
                raise Exception('Please select a valid ID within the date range')
        if args.save:
            saved_doc = doc_handler.save(args.save, r_table, SYSTEM_TIME)
            CONSOLE.print(f'Your report was saved as {saved_doc}')

    
    #------------------FILE ACTION HANDLING-------------------#
    elif args.command == 'export':
        if args.file_name:
            e_file = doc_handler.export(args.csv_name, SYSTEM_TIME, args.export_type, args.file_name)
        else:
            e_file =doc_handler.export(args.csv_name, SYSTEM_TIME, args.export_type)
        if e_file:
            CONSOLE.print(f'Exported file has been saved as {e_file}')
        
        
    
    elif args.command == 'import':
        if args.import_action == 'append':
            doc_handler.import_data(args.file_name, args.csv_name, SYSTEM_TIME, append= True)
        elif args.import_action == 'overwrite':
            doc_handler.import_data(args.file_name, args.csv_name, SYSTEM_TIME, overwrite= True)
    
    elif args.command == 'file':
        if args.file_action == 'wipe':
            doc_handler.wipe_csv(args.csv_name,SYSTEM_TIME)  
        elif args.file_action == 'backup':
            doc_handler.backup_csv(args.csv_name, SYSTEM_TIME)
        

if __name__ == "__main__":
    main()
