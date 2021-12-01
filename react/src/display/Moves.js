import React from "react";

class Moves extends React.Component {

  render() {
    let items = []
    const align = {
      textAlign: 'right'
    }
    if (this.props.moves != null) {
      for (const [key, value] of Array.from(this.props.moves.entries()).reverse()) {
        let sp = value.split(' ')
        if (sp.length === 4) {
          items.push(<tr>
            <td>{key + 1}</td>
            <td>{sp[0]}</td>
            <td>{sp[1]}</td>
            <td></td>
            <td style={align}>{sp[2]}</td>
            <td style={align}>{sp[3]}</td>
          </tr>)
        } else {
          items.push(<tr>
            <td>{key + 1}</td>
            <td>{sp[0]}</td>
            <td>{sp[1]}</td>
            <td>{sp[2]}</td>
            <td style={align}>{sp[3]}</td>
            <td style={align}>{sp[4]}</td>
          </tr>)
        }
        // items.push(<li key={key}>{value}</li>)
      }
    }
    return (
      <div className="card moves">
        <div className="card-header">Züge</div>
        <div className="card-body">
          <table className={"moves"}>
            {items}
          </table>
        </div>
      </div>
    );
  }

}

export default Moves;
