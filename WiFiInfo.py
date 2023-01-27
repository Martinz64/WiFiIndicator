import os
import re

def get_wlan_standard(rate):
    if "HE" in rate:
        return "AX"
    if "VHT" in rate:
        return "AC"
    if "HT" in rate:
        return "N"
    return "G"


#print(iwlink)
def get_info_from_iwlink(iwlink):
    if not "Not connected." in iwlink:
        ssid_pat = re.compile("SSID: (.*?) \t")
        ssid = ssid_pat.search(iwlink).group(1)

        freq_pat = re.compile("freq: (.*?) \t")
        freq = float(freq_pat.search(iwlink).group(1))

        signal_pat = re.compile("signal: (.*?) dBm \t")
        signal = float(signal_pat.search(iwlink).group(1))

        tx_rate_pat = re.compile("tx bitrate: (.*?) \t")
        tx_rate = tx_rate_pat.search(iwlink).group(1)

        speed_pat = re.compile("(.*?) MBit/s")
        tx_speed = float(speed_pat.search(tx_rate).group(1))

        bw_pat = re.compile(" (\d*?)MHz")
        tx_bw = float(bw_pat.search(tx_rate).group(1))

        standard = get_wlan_standard(tx_rate)

        d = dict()
        d['ssid'] = ssid
        d['freq'] = freq
        d['signal'] = signal
        d['tx_speed'] = tx_speed
        d['tx_bw'] = tx_bw
        d['standard'] = standard
        d['connected'] = True
        return d
    else:
        d = dict()
        d['connected'] = False
        return d

#iwlink = os.popen("iw %s link" % "wlp2s0").read().replace('\n',' ')
#wl = get_info_from_iwlink(iwlink)

'''print('%s %s %d dBm %d Mb/s (%s GHz)' % (
    wl['standard'],
    wl['ssid'],
    wl['signal'],
    wl['tx_speed'],
    ('%f' % (wl['freq']/1000)).rstrip('0')
))'''

#print(standard,ssid,freq,signal)
