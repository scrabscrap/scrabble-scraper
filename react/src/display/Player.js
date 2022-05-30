import React from "react";

class Player extends React.Component {

  render() {
    var headerclass = "card-header"
    if (this.props.name === this.props.current) {
      headerclass = headerclass + " text-white bg-success"
    }
//    var _tmp = 1800 - this.props.time
    var _tmp = this.props.time
    var vz = ''
    if (_tmp < 0) {
      _tmp = -_tmp
      vz = '-'
    }
    var _m = Math.trunc(_tmp / 60)
    var _s = _tmp % 60
    // data = [int((_m // 10) % 10), int(_m % 10), int(_s // 10), int(_s % 10)]

    return (
        <div className="card player">
          <div className={headerclass}>
            {this.props.name}: {this.props.score} (Restzeit: {vz}{Math.trunc(_m / 10) % 10}{(_m % 10)}:{Math.trunc(_s / 10)}{(_s % 10)})
          </div>
        </div>
    );
  }

}

export default Player;
