import { selectIadsNetwork } from "../../../api/iadsNetworkSlice";
import { useAppSelector } from "../../../app/hooks";
import IadsConnection from "../iadsnetwork/IadsNetwork";
import { LayerGroup } from "react-leaflet";

interface IadsNetworkLayerProps {
  blue: boolean;
}

export const IadsNetworkLayer = (props: IadsNetworkLayerProps) => {
  const connections = Object.values(
    useAppSelector(selectIadsNetwork).connections
  );
  var iadsConnectionsForSide = connections.filter(
    (connection) => connection.blue === props.blue
  );

  return (
    <LayerGroup>
      {iadsConnectionsForSide.map((connection) => {
        return (
          <IadsConnection key={connection.id} iads_connection={connection} />
        );
      })}
    </LayerGroup>
  );
};

export default IadsNetworkLayer;
