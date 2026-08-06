export default function DeparturePill({ state, departure, minutesUntil, following }) {
  if (state === "CLOSED") {
    return <div>Campus stop closed — first bus {departure?.time}</div>;
  }
  return (
    <div>
      <div>{departure?.route} to {departure?.headsign}</div>
      <div>{departure?.time} <span>scheduled</span></div>
      <div>{minutesUntil} min</div>
      {state === "LAST_BUS" && <div>last bus today</div>}
      {following && <div>then {following.time}</div>}
    </div>
  );
}
