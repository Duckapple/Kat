from datetime import datetime, timedelta
import re

def toDatetime(time: str) -> datetime:
    # Trim off the time zone ending of the string
    justTime = time.split()[:-1]
    return datetime.fromisoformat(' '.join(justTime))


def toTimeDelta(time: str):
    """
    Format of `time` is `[-][D day[s]] [H]H:[M]M:[S]S`,
    where `D`, `H`, `M` and `S` are captured digits.
    """
    capture = re.match('(-)?(?:(\d+) days?, )?(\d{1,2}):(\d{1,2}):(\d{1,2})', time)
    if capture == None: return None
    captureGroups = [capture.group(i) for i in range(1, 6)]
    days, hours, minutes, seconds = map(lambda x: int(x) if x != None else None, captureGroups[1:])
    delta = timedelta(
        days=days if days else 0,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )
    sign = captureGroups[0]
    return -delta if sign else delta
