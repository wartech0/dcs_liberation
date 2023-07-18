interface ControlPointModalProps {
  show: boolean;
}

export default function ControlPointModal(props: ControlPointModalProps) {
  if (props.show) {
    return <h1>Hello World</h1>;
  } else {
    return null;
  }
}
