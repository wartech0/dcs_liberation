import { useAppSelector } from "../../../app/hooks";

export default function ContextPane() {
  const selectedCP = useAppSelector(
    (state) => state.webInterface.selectedControlPoint
  );
  const selectedTgo = useAppSelector((state) => state.webInterface.selectedTgo);
  const CP = useAppSelector((state) => state.webInterface.ControlPoint);
  const Tgo = useAppSelector((state) => state.webInterface.Tgo);

  if (selectedTgo && Tgo) {
    return (
      <div className="container">
        <h1 className="display-6">
          <strong>{selectedTgo.name}</strong>
        </h1>
        <strong>{selectedTgo.category.toUpperCase()}</strong>
        <h3>
          {selectedTgo.blue ? (
            <p className="text-primary">OWNFOR</p>
          ) : (
            <p className="text-danger">OPFOR</p>
          )}
        </h3>
        <>
          {selectedTgo.units.map((unit) => (
            <p>{unit}</p>
          ))}
        </>
      </div>
    );
  }

  if (selectedCP && CP) {
    return (
      <div className="container">
        <h1 className="display-6">
          <strong>{selectedCP.name.toUpperCase()}</strong>
        </h1>
        <h3>
          {selectedCP.blue ? (
            <p className="text-primary">OWNFOR</p>
          ) : (
            <p className="text-danger">OPFOR</p>
          )}
        </h3>
        <h3>Ammo Depot: {selectedCP.active_ammo_depot}</h3>
        <h3>Fuel Depot: {selectedCP.active_fuel_depot}</h3>
      </div>
    );
  }

  return <></>;
}
