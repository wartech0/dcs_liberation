import { ControlPoint } from "../../api/_liberationApi";
import { selectInterfaceCP } from "../../api/webInterfaceSlice";
import { useAppDispatch } from "../../app/hooks";
import { iconForControlPoint } from "./Icons";
import LocationTooltipText from "./LocationTooltipText";
import { Marker, Tooltip } from "react-leaflet";

interface StaticControlPointProps {
  controlPoint: ControlPoint;
}

export const StaticControlPoint = (props: StaticControlPointProps) => {
  const Dispatch = useAppDispatch();

  return (
    <Marker
      position={props.controlPoint.position}
      icon={iconForControlPoint(props.controlPoint)}
      // We might draw other markers on top of the CP. The tooltips from the
      // other markers are helpful so we want to keep them, but make sure the CP
      // is always the clickable thing.
      zIndexOffset={1000}
      eventHandlers={{
        click: () => {
          Dispatch(selectInterfaceCP(props.controlPoint));
        },
      }}
    >
      <Tooltip>
        <LocationTooltipText name={props.controlPoint.name} />
      </Tooltip>
    </Marker>
  );
};
