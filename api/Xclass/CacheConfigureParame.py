


def verifyCacheCfgParame(parame,value):
    return_data = {}
    if parame == 'port':
        return_data['msg'] = '1024-65535'
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if 1024 <= value <= 65535:
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1
    if parame in ['appendonly','activerehashing','no-appendfsync-on-rewrite']:
        return_data['msg'] = 'yes,no'
        if value in ["yes","no"]:
            return_data['code'] = 0
        else:
            return_data['code'] = 1

    if parame == 'appendfsync':
        return_data['msg'] = 'everysec,always,no'
        if value in ["everysec","always","no"]:
            return_data['code'] = 0
        else:
            return_data['code'] = 1

    if parame == 'maxmemory-policy':
        return_data['msg'] = 'volatile-lru,allkeys-lru,volatile-random,allkeys-random,volatile-ttl,noeviction'
        if value in ["volatile-lru","allkeys-lru","volatile-random","allkeys-random","volatile-ttl","noeviction"]:
            return_data['code'] = 0
        else:
            return_data['code'] = 1
                
    if parame == 'disable-commands':
        return_data['msg'] = 'FLUSHDB,FLUSHALL'
        if value in ["FLUSHDB","FLUSHALL"]:
            return_data['code'] = 0
        else:
            return_data['code'] = 1
                
    if parame == ['hash-max-ziplist-entries','list-max-ziplist-entries']:
        return_data['msg'] = '0-512'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if 0 <= value <= 512:
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1
    if parame == ['hash-max-ziplist-value','list-max-ziplist-value']:
        return_data['msg'] = '0-64'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if 0 <= value <= 64:
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1
    if parame == 'latency-monitor-threshold':
        return_data['msg'] = '0-600000'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if 0 <= value <= 600000:
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1
    if parame == 'maxclients':
        return_data['msg'] = '0-65000'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if 0 <= value <= 65000:
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1
    if parame == 'repl-backlog-size':
        return_data['msg'] = '16384-'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if 16384 <= value:
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1
    if parame in ['maxmemory-samples','min-slaves-max-lag','min-slaves-to-write',\
                        'repl-backlog-ttl','set-max-intset-entries','set-max-intset-entries',\
                        'zset-max-ziplist-entries','zset-max-ziplist-value']:
        return_data['msg'] = '0-'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if 0 <= value:
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1
    if parame == 'slowlog-log-slower-than':
        return_data['msg'] = '-1-60000'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if -1 <= value <= 60000:
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1
    if parame == 'slowlog-max-len':
        return_data['msg'] = '0-1000'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if 0 <= value <= 1000:
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1
    if parame == 'tcp-keepalive':
        return_data['msg'] = '0-2147483647'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if 0 <= value <= 2147483647:
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1
    if parame == 'timeout':
        return_data['msg'] = '0,20-'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if (value ==0) or (20 <= value):
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1
    if parame == 'udp_port':
        return_data['msg'] = '0,1024-65535'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if (value ==0) or (1024 <= value<=65535):
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1
    if parame in ['cas_disabled','error_on_memory_exhausted']:
        return_data['msg'] = '0-1'
        if value in ["0","1"]:
            return_data['code'] = 0
        else:
            return_data['code'] = 1
    if parame == 'chunk_size':
        return_data['msg'] = '1-1024'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if 1 <= value<=1024:
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1

    if parame == 'max_simultaneous_connections':
        return_data['msg'] = '1-65000'
        valueList = value.split('.')
        try:
            if valueList[1]:
                return_data['code'] = 1
        except:
            try:
                value = int(value)
                if 1 <= value <= 65000:
                    return_data['code'] = 0
                else:
                    return_data['code'] = 1
            except:
                return_data['code'] = 1

    return return_data
