import { useAppSelector } from "../../../app/hooks";

interface PackageProps {
  desc: string;
  target_name: string;
}

function Package(props: PackageProps) {
  return (
    <div className="container">
      <div className="card" style={{ width: "18rem" }}>
        <div className="card-body">
          <h5 className="card-title">
            {props.desc} {props.target_name}
          </h5>
        </div>
      </div>
    </div>
  );
}

export default Package;
