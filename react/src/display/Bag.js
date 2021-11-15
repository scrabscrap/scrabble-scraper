import React from "react";

class Bag extends React.Component {

  render() {
    var items = []

    if (this.props.bag != null) {
      for (const [key, value] of this.props.bag.entries()) {
        items.push(<span key={key} className="tile">{value}</span>)
      }
    }
    return (
        <div className="card bag">
          <div className="card-header">nicht gespielt</div>
          <div className="card-body">
            {items}
          </div>
        </div>
    );
  }

}

export default Bag;
