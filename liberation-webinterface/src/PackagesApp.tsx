import { getPackages } from "./api/packagesSlice";
import { useAppSelector } from "./app/hooks";
import Header from "./components/ui/header/Header";
import Login from "./components/ui/login/Login";
import Package from "./components/ui/package";
import useEventStream from "./hooks/useEventSteam";
import useInitialGameState from "./hooks/useInitialGameState";
import "./index.css";

function IsLoggedIn() {
  return true;
}

function PackagesApp() {
  useInitialGameState();
  //useEventStream();
  const packages = useAppSelector(getPackages);

  return (
    <div className="PackagesApp">
      <Header />

      {Object.values(packages).map((pack) => {
        return (
          <Package
            key={pack.id}
            desc={pack.desc}
            target_name={pack.target_name}
          />
        );
      })}
    </div>
  );
}

export default PackagesApp;
