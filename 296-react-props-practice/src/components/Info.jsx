import React from "react";

export default function Info(props) {
  return (
    <div>
      <p className="info">{props.tel}</p>
      <p className="info">{props.email}</p>
    </div>
  );
}
