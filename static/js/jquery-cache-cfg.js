/**
 * Created by shengyuan on 2016/4/1.
 */
    function CacheDefaultCfg(cacheType){
        if (cacheType==0||cacheType==1){
            var cfgcont = '<tr class="editable editing"><td class="key"><span class="id">port</span></td><td class="master_value">6379</td><td style="border-right:1px solid #e4eaec;"><span class="tips">1024-65535</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id"><span class="id">appendonly</span></td><td class="master_value">yes</td><td style="border-right:1px solid #e4eaec;"><span class="tips">yes,no</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id"><span class="id">appendfsync</span></td><td class="master_value">everysec</td><td style="border-right:1px solid #e4eaec;"><span class="tips">everysec,always,no</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">maxmemory-policy</span></td><td class="master_value">volatile-lru</td><td style="border-right:1px solid #e4eaec;"><span class="tips">volatile-lru,allkeys-lru,volatile-random,allkeys-random,volatile-ttl,noeviction</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">activerehashing</span></td><td class="master_value">yes</td><td style="border-right:1px solid #e4eaec;"><span class="tips">yes,no</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">disable-commands</span></td><td class="master_value"></td><td style="border-right:1px solid #e4eaec;"><span class="tips">FLUSHDB,FLUSHALL</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">hash-max-ziplist-entries</span></td><td class="master_value">512</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-512</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">hash-max-ziplist-value</span></td><td class="master_value">64</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-64</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">latency-monitor-threshold</span></td><td class="master_value">0</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-600000</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">list-max-ziplist-entries</span></td><td class="master_value">512</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-512</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">list-max-ziplist-value</span></td><td class="master_value">64</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-64</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">maxclients</span></td><td class="master_value">65000</td><td style="border-right:1px solid #e4eaec;"><span class="tips">1-65000</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">maxmemory-samples</span></td><td class="master_value">3</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">min-slaves-max-lag</span></td><td class="master_value">10</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">min-slaves-to-write</span></td><td class="master_value">0</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">no-appendfsync-on-rewrite</span></td><td class="master_value">yes</td><td style="border-right:1px solid #e4eaec;"><span class="tips">yes,no</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">notify-keyspace-events</span></td><td class="master_value"></td><td style="border-right:1px solid #e4eaec;"><span class="tips"></span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">repl-backlog-size</span></td><td class="master_value">1048576</td><td style="border-right:1px solid #e4eaec;"><span class="tips">16384-</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">repl-backlog-ttl</span></td><td class="master_value">3600</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">repl-timeout</span></td><td class="master_value">60</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">requirepass</span> <span class="none">* 不支持集群服务</span></td><td class="master_value"></td><td style="border-right:1px solid #e4eaec;"><span class="tips"></span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">set-max-intset-entries</span></td><td class="master_value">512</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">slaveof-host</span> <span class="none">* 不支持集群服务</span></td><td class="master_value"></td><td style="border-right:1px solid #e4eaec;"><span class="tips"></span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">slowlog-log-slower-than</span></td><td class="master_value">-1</td><td style="border-right:1px solid #e4eaec;"><span class="tips">-1-60000</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">slowlog-max-len</span></td><td class="master_value">128</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-1000</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">tcp-keepalive</span></td><td class="master_value">0</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-2147483647</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">timeout</span></td><td class="master_value">0</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0,20-</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">zset-max-ziplist-entries</span></td><td class="master_value">128</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">zset-max-ziplist-value</span></td><td class="master_value">64</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-</span></td></tr>';
            }
            if(cacheType==2){
            var cfgcont = '<tr class="editable editing"><td class="key"><span class="id">port</span></td><td class="master_value">11211</td><td style="border-right:1px solid #e4eaec;"><span class="tips">1024-65535</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">udp_port</span></td><td class="master_value">11211</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0,1024-65535</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">cas_disabled</span></td><td class="master_value">0</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-1</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">chunk_size</span></td><td class="master_value">48</td><td style="border-right:1px solid #e4eaec;"><span class="tips">1-1024</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">chunk_size_growth_factor</span></td><td class="master_value">1.25</td><td style="border-right:1px solid #e4eaec;"><span class="tips">1.01-100.00</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">error_on_memory_exhausted</span></td><td class="master_value">0</td><td style="border-right:1px solid #e4eaec;"><span class="tips">0-1</span></td></tr>';
            cfgcont += '<tr class="editable editing"><td class="key"><span class="id">max_simultaneous_connections</span></td><td class="master_value">65000</td><td style="border-right:1px solid #e4eaec;"><span class="tips">1-65000</span></td></tr>';
            }
    return cfgcont;
}
