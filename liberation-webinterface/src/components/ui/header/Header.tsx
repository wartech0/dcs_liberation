import { useAppSelector } from "../../../app/hooks";

function Header() {
  const budget = useAppSelector((state) => state.gameState.current_income);
  return (
    <nav
      className="navbar bg-dark border-bottom border-bottom-dark navbar-expand-lg"
      data-bs-theme="dark"
    >
      <div className="container-fluid">
        <a className="navbar-brand text-white" href="/">
          Liberation War Room
        </a>
        <div className="navbar-nav">
          <a className="nav-item nav-link" href="/packages">
            Packages
          </a>
          <a className="nav-item nav-link" href="/squadrons">
            Squadrons
          </a>

          <span className="navbar-text">{budget}M USD</span>
        </div>
      </div>
    </nav>
  );
}

export default Header;
