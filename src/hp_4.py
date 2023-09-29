# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    old_format = "%Y-%m-%d"
    new_format = "%d %b %Y"
    new_dates = [datetime.strptime(date,old_format).strftime(new_format) for date in old_dates]
    return new_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    new_dates = []
    date_obj = datetime.strptime(start,'%Y-%m-%d')
    for val in range(0,n):
        new_dates.append(date_obj + timedelta(days=val))
    return new_dates


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    new_dates = []
    date_obj = datetime.strptime(start_date,'%Y-%m-%d')
    for index,val in enumerate(values):
        new_date = date_obj + timedelta(days=index)
        new_dates.append((new_date,val))
    return new_dates
        


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile,'r') as file:
        patrons_list = []
        dr_obj = DictReader(file)
        for item in dr_obj:
            patron_dict = dict()
            no_of_days = datetime.strptime(item['date_returned'],'%m/%d/%Y') - datetime.strptime(item['date_due'],'%m/%d/%Y')
            if no_of_days == 0:
                patron_dict['patron_id'] = item['patron_id']
                patron_dict['late_fees'] = float(0)
                patrons_list.append(patron_dict)
            else:
                patron_dict['patron_id'] = item['patron_id']
                patron_dict['late_fees'] = round(no_of_days.days*0.25,2)
                patrons_list.append(patron_dict)
        aggregated_data = dict()
        for patron in patrons_list:
            aggregated_data[patron['patron_id']] = aggregated_data.get(patron['patron_id'],0) + patron['late_fees']
        patrons_late_fee_list = [{'patron_id':k, 'late_fees':v} for k,v in aggregated_data.items()]
        for p in patrons_late_fee_list:
            for k,v in p.items():
                if k == 'late_fees':
                    if len(str(v).split('.')[-1]) != 2:
                        p[k] = str(v) + '0'
        with open(outfile,'w',newline='') as file:
            col = ['patron_id','late_fees']
            writer = DictWriter(file,fieldnames=col)
            writer.writeheader()
            writer.writerows(tax)
                
    


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
