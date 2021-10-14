import os
import json
from rethinkdb import r
import prpubsub as ps
from crawler import *
import base64

if __name__ == '__main__':
    dbname = os.environ['RETHINKDB_DATABASE'].strip()
    dbhost = os.environ.get('RETHINKDB_HOST').strip()
    #     dbpass=os.environ.get('RETHINKDB_PASS').strip()
    exchange = ps.Exchange('pupsub', db=dbname, host=dbhost)
    topic_bpa = exchange.topic('crawler.bpa')
    topic_response = exchange.topic('crawler.callback')
    #
    # # escuchar una cola
    filter_func = lambda topic: topic.match(r'crawler\.bpa')
    queue = exchange.queue(filter_func)

    for topic_bpa, payload in queue.subscription():
        data = dict(payload)
        token = data['token'].strip()
        action = data['action'].strip()
        cid = data['cid'].strip()
        params = json.loads(str(base64.b64decode(token), "utf-8").replace('_NH_', 'Ñ'))
        #     proxies={
        #          'http': 'socks5://localhost:1040',
        #          'https': 'socks5://localhost:1040',
        #     }

        crw = crawbpa(params, None)

        if action == 'healthcheck' or action == 'health_check' or action == 'ping':
            payload = crw.health_check()
            print(payload)
            topic_response.publish({
                "cid": cid,
                "data": payload
            })
        if action == 'lockup':
            payload = crw.holder_lockup(data['account'].strip())
            print(payload)
            topic_response.publish({
                "cid": cid,
                "data": payload
            })
        if action == 'sync':
            payload = crw.get_accounts()
            print(payload)
            topic_response.publish({
                "cid": cid,
                "data": payload
            })
        if action == 'upgrade_limits':
            amount = data['account'].strip()
            payload = json.dumps(crw.update_limits(amount))
            print(payload)
            topic_response.publish({
                "cid": cid,
                "data": payload
            })
