import sqlite3, sys
from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Chicago")
DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

def to_secs(hms):
    h, m, s = (int(x) for x in hms.split(":"))
    return h*3600 + m*60 + s

def active_services(con, now):
    ymd = now.strftime("%Y%m%d")
    day = DAYS[now.weekday()]
    base = {r[0] for r in con.execute(
        f"SELECT service_id FROM calendar WHERE {day}='1' "
        "AND start_date<=? AND end_date>=?", (ymd, ymd))}
    for sid, ex in con.execute(
        "SELECT service_id, exception_type FROM calendar_dates WHERE date=?", (ymd,)):
        base.add(sid) if ex == "1" else base.discard(sid)
    return base

def next_departures(con, stop_id, n=5):
    now = datetime.now(TZ)
    now_s = now.hour*3600 + now.minute*60 + now.second
    svc = active_services(con, now)
    if not svc:
        return now, []
    q = ("SELECT r.route_short_name, r.route_long_name, t.direction_text, st.departure_time "
         "FROM stop_times st JOIN trips t ON t.trip_id=st.trip_id "
         "JOIN routes r ON r.route_id=t.route_id "
         f"WHERE st.stop_id=? AND t.service_id IN ({','.join('?'*len(svc))})")
    out = []
    for rt, ln, dirtxt, dep in con.execute(q, (stop_id, *svc)):
        if not dep:
            continue
        d = to_secs(dep)
        if d >= now_s:
            out.append((d - now_s, rt or ln, dirtxt, dep))
    out.sort()
    return now, out[:n]

if __name__ == "__main__":
    stop = sys.argv[1] if len(sys.argv) > 1 else "220s0345"
    con = sqlite3.connect("data/pace.db")
    now, deps = next_departures(con, stop)
    print(f"stop {stop} | {now:%a %b %d %I:%M %p} | SCHEDULED, not live\n")
    if not deps:
        print("no more buses today")
    for mins, rt, dirtxt, dep in deps:
        print(f"  {dep}  ({mins//60:>3} min)  Rt {rt:<5} {dirtxt}")
