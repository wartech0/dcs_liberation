import { renderWithProviders } from "../../../testutils";
import ControlPointsLayer from "./ControlPointsLayer";
import { LatLng } from "leaflet";
import { PropsWithChildren } from "react";

const mockMarker = jest.fn();
const mockLayerGroup = jest.fn();
jest.mock("react-leaflet", () => ({
  LayerGroup: (props: PropsWithChildren<any>) => {
    mockLayerGroup(props);
    return <>{props.children}</>;
  },
  Marker: (props: any) => {
    mockMarker(props);
  },
}));

describe("ControlPointsLayer", () => {
  it("renders each control point", () => {
    renderWithProviders(<ControlPointsLayer />, {
      preloadedState: {
        controlPoints: {
          controlPoints: {
            foo: {
              id: "foo",
              name: "Foo",
              blue: true,
              position: new LatLng(0, 0),
              mobile: false,
              sidc: "",
              active_ammo_depot: 0,
              active_fuel_depot: 0,
            },
            bar: {
              id: "bar",
              name: "Bar",
              blue: false,
              position: new LatLng(1, 0),
              mobile: false,
              sidc: "",
              active_ammo_depot: 0,
              active_fuel_depot: 0,
            },
          },
        },
      },
    });
    expect(mockMarker).toBeCalledTimes(2);
  });

  it("renders LayerGroup but no contents if no combat", () => {
    renderWithProviders(<ControlPointsLayer />);
    expect(mockLayerGroup).toBeCalledTimes(1);
    expect(mockMarker).not.toHaveBeenCalled();
  });
});
