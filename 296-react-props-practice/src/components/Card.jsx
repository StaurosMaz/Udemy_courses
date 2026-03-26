import React from "react";
import Avatar from "./Avatar";
import Info from "./Info";

export default function Card(props) {
  return (
    <div>
      <div className="card">
        <div className="top">
          <h2 className="name">{props.name}</h2>
          <Avatar img={props.img} />
        </div>
        <div className="bottom ">
          <Info tel={props.tel} email={props.email} />
        </div>
      </div>
    </div>
  );
}
