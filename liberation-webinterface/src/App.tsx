import LiberationMap from "./components/LiberationMap";
import ContextPane from "./components/contextpane/ContextPane";
import Header from "./components/header/Header";
import Login from "./components/login/Login";
import useEventStream from "./hooks/useEventSteam";
import useInitialGameState from "./hooks/useInitialGameState";
import "./index.css";

function IsLoggedIn() {
  return true;
}

function App() {
  useInitialGameState();
  useEventStream();
  return (
    <div className="App">
      <Header />
      <div className="row g-0">
        <div className="col-3">
          <div className="container">
            <ContextPane />
          </div>
        </div>
        <div className="col-9">
          <LiberationMap />
        </div>
      </div>
    </div>
  );
}

export default App;
