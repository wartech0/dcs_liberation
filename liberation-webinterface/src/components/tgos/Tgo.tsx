import { Tgo as TgoModel } from "../../api/liberationApi";
import { selectInterfaceTgo } from "../../api/webInterfaceSlice";
import { useAppDispatch } from "../../app/hooks";
import SplitLines from "../splitlines/SplitLines";
import { Icon, Point } from "leaflet";
import { Symbol as MilSymbol } from "milsymbol";
import { Marker, Tooltip } from "react-leaflet";

function iconForTgo(cp: TgoModel) {
  const symbol = new MilSymbol(cp.sidc, {
    size: 24,
  });

  return new Icon({
    iconUrl: symbol.toDataURL(),
    iconAnchor: new Point(symbol.getAnchor().x, symbol.getAnchor().y),
  });
}

interface TgoProps {
  tgo: TgoModel;
}

export default function Tgo(props: TgoProps) {
  const Dispatch = useAppDispatch();
  return (
    <Marker
      position={props.tgo.position}
      icon={iconForTgo(props.tgo)}
      eventHandlers={{
        click: () => {
          Dispatch(selectInterfaceTgo(props.tgo));
        },
      }}
    >
      <Tooltip>
        {`${props.tgo.name} (${props.tgo.control_point_name})`}
        <br />
        <SplitLines items={props.tgo.units} />
      </Tooltip>
    </Marker>
  );
}
