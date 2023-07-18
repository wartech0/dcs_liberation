import { ControlPoint } from "../../api/_liberationApi";
import backend from "../../api/backend";


function OpenInfoDialog(controlPoint: ControlPoint) {
}

function OpenNewPackageDialog(controlPoint: ControlPoint) {
  backend.get(`/control-points/${controlPoint.id}`);
}

export const makeLocationMarkerEventHandlers = (controlPoint: ControlPoint) => {
  return {
    click: () => {
      OpenInfoDialog(controlPoint);
    },

    contextmenu: () => {
      OpenNewPackageDialog(controlPoint);
    },
  };
};
