
from flask import Blueprint, jsonify
from pricing_app.model.index import EquityIndex

# Define the blueprint and set its url prefix
mod = Blueprint('index_pricing', __name__, url_prefix='/idx')


@mod.route('/px/<idx>')
def index_data(idx):
    """Called by the DataTable when the page is first opened

    [The data collected here might as well be sent direct to the page]
    """
    this = EquityIndex(idx)

    # collect data from first file
    ts = '0810'
    price_data = this.components_last_px(ts)

    # reformat timestamp for inclusion in the table
    ts = ts[:2] + ':' + ts[2:]

    # passing each row as an object (and notice that we're also
    # explicitly passing DT_RowId) makes it easier to isolate the
    # DataTable row 'by ticker' in the websocket javascript function(s)
    data = []
    for ticker, _data in price_data.iteritems():

        rw = {'DT_RowId': ticker,
              'ticker': ticker,
              'px': 'n/a',
              'ccy': 'n/a',
              'ts': ts
              }
        # effectively what we're doing here is treating each row as
        # having no data. Only if _data!=None do we insert px and ccy
        if _data:
            rw['px'] = _data['px']
            rw['ccy'] = _data['ccy']

        data.append(rw)

    return jsonify(data=data)
