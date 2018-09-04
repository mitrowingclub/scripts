set -x

source /home/orm/anaconda3/bin/activate sheets
cd /home/orm/read_sheet/

# for renewing credential add flag --noauth_local_webserver, and remove argparse
# send non-LTR reminder
python quickstart.py

# send LTR reminder
python quickstart.py --LTR=True
