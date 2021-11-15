import React from "react";

class Board extends React.Component {

  cell(board, coord) {
    if (board != null) {
      var e = board[coord]
      if (e != null) {
        return (<div id={coord} className="tile">{e}</div>);
      } else {
        return (<div id={coord}></div>);
      }
    } else {
      return null;
    }
  }

  render() {
    return (
        <div className="card board">
          <div className="card-body"><center>
          <table id="board" className="tableboard">
            <thead>
            <tr>
              <td className="tableborder"></td>
              <td className="tableborder">1</td>
              <td className="tableborder">2</td>
              <td className="tableborder">3</td>
              <td className="tableborder">4</td>
              <td className="tableborder">5</td>
              <td className="tableborder">6</td>
              <td className="tableborder">7</td>
              <td className="tableborder">8</td>
              <td className="tableborder">9</td>
              <td className="tableborder">10</td>
              <td className="tableborder">11</td>
              <td className="tableborder">12</td>
              <td className="tableborder">13</td>
              <td className="tableborder">14</td>
              <td className="tableborder">15</td>
            </tr>
            </thead>
            <tbody>
            <tr>
              <td className="tableborder">A</td>
              <td className="tablered">{this.cell(this.props.board, "a1")}</td>
              <td>{this.cell(this.props.board, "a2")}</td>
              <td>{this.cell(this.props.board, "a3")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "a4")}</td>
              <td>{this.cell(this.props.board, "a5")}</td>
              <td>{this.cell(this.props.board, "a6")}</td>
              <td>{this.cell(this.props.board, "a7")}</td>
              <td className="tablered">{this.cell(this.props.board, "a8")}</td>
              <td>{this.cell(this.props.board, "a9")}</td>
              <td>{this.cell(this.props.board, "a10")}</td>
              <td>{this.cell(this.props.board, "a11")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "a12")}</td>
              <td>{this.cell(this.props.board, "a13")}</td>
              <td>{this.cell(this.props.board, "a14")}</td>
              <td className="tablered">{this.cell(this.props.board, "a15")}</td>
            </tr>
            <tr>
              <td className="tableborder">B</td>
              <td>{this.cell(this.props.board, "b1")}</td>
              <td className="tableorange">{this.cell(this.props.board, "b2")}</td>
              <td>{this.cell(this.props.board, "b3")}</td>
              <td>{this.cell(this.props.board, "b4")}</td>
              <td>{this.cell(this.props.board, "b5")}</td>
              <td className="tableblue">{this.cell(this.props.board, "b6")}</td>
              <td>{this.cell(this.props.board, "b7")}</td>
              <td>{this.cell(this.props.board, "b8")}</td>
              <td>{this.cell(this.props.board, "b9")}</td>
              <td className="tableblue">{this.cell(this.props.board, "b10")}</td>
              <td>{this.cell(this.props.board, "b11")}</td>
              <td>{this.cell(this.props.board, "b12")}</td>
              <td>{this.cell(this.props.board, "b13")}</td>
              <td className="tableorange">{this.cell(this.props.board, "b14")}</td>
              <td>{this.cell(this.props.board, "b15")}</td>
            </tr>
            <tr>
              <td className="tableborder">C</td>
              <td>{this.cell(this.props.board, "c1")}</td>
              <td>{this.cell(this.props.board, "c2")}</td>
              <td className="tableorange">{this.cell(this.props.board, "c3")}</td>
              <td>{this.cell(this.props.board, "c4")}</td>
              <td>{this.cell(this.props.board, "c5")}</td>
              <td>{this.cell(this.props.board, "c6")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "c7")}</td>
              <td>{this.cell(this.props.board, "c8")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "c9")}</td>
              <td>{this.cell(this.props.board, "c10")}</td>
              <td>{this.cell(this.props.board, "c11")}</td>
              <td>{this.cell(this.props.board, "c12")}</td>
              <td className="tableorange">{this.cell(this.props.board, "c13")}</td>
              <td>{this.cell(this.props.board, "c14")}</td>
              <td>{this.cell(this.props.board, "c15")}</td>
            </tr>
            <tr>
              <td className="tableborder">D</td>
              <td className="tablelightblue">{this.cell(this.props.board, "d1")}</td>
              <td>{this.cell(this.props.board, "d2")}</td>
              <td>{this.cell(this.props.board, "d3")}</td>
              <td className="tableorange">{this.cell(this.props.board, "d4")}</td>
              <td>{this.cell(this.props.board, "d5")}</td>
              <td>{this.cell(this.props.board, "d6")}</td>
              <td>{this.cell(this.props.board, "d7")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "d8")}</td>
              <td>{this.cell(this.props.board, "d9")}</td>
              <td>{this.cell(this.props.board, "d10")}</td>
              <td>{this.cell(this.props.board, "d11")}</td>
              <td className="tableorange">{this.cell(this.props.board, "d12")}</td>
              <td>{this.cell(this.props.board, "d13")}</td>
              <td>{this.cell(this.props.board, "d14")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "d15")}</td>
            </tr>
            <tr>
              <td className="tableborder">E</td>
              <td>{this.cell(this.props.board, "e1")}</td>
              <td>{this.cell(this.props.board, "e2")}</td>
              <td>{this.cell(this.props.board, "e3")}</td>
              <td>{this.cell(this.props.board, "e4")}</td>
              <td className="tableorange">{this.cell(this.props.board, "e5")}</td>
              <td>{this.cell(this.props.board, "e6")}</td>
              <td>{this.cell(this.props.board, "e7")}</td>
              <td>{this.cell(this.props.board, "e8")}</td>
              <td>{this.cell(this.props.board, "e9")}</td>
              <td>{this.cell(this.props.board, "e10")}</td>
              <td className="tableorange">{this.cell(this.props.board, "e11")}</td>
              <td>{this.cell(this.props.board, "e12")}</td>
              <td>{this.cell(this.props.board, "e13")}</td>
              <td>{this.cell(this.props.board, "e14")}</td>
              <td>{this.cell(this.props.board, "e15")}</td>
            </tr>
            <tr>
              <td className="tableborder">F</td>
              <td>{this.cell(this.props.board, "f1")}</td>
              <td className="tableblue">{this.cell(this.props.board, "f2")}</td>
              <td>{this.cell(this.props.board, "f3")}</td>
              <td>{this.cell(this.props.board, "f4")}</td>
              <td>{this.cell(this.props.board, "f5")}</td>
              <td className="tableblue">{this.cell(this.props.board, "f6")}</td>
              <td>{this.cell(this.props.board, "f7")}</td>
              <td>{this.cell(this.props.board, "f8")}</td>
              <td>{this.cell(this.props.board, "f9")}</td>
              <td className="tableblue">{this.cell(this.props.board, "f10")}</td>
              <td>{this.cell(this.props.board, "f11")}</td>
              <td>{this.cell(this.props.board, "f12")}</td>
              <td>{this.cell(this.props.board, "f13")}</td>
              <td className="tableblue">{this.cell(this.props.board, "f14")}</td>
              <td>{this.cell(this.props.board, "f15")}</td>
            </tr>
            <tr>
              <td className="tableborder">G</td>
              <td>{this.cell(this.props.board, "g1")}</td>
              <td>{this.cell(this.props.board, "g2")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "g3")}</td>
              <td>{this.cell(this.props.board, "g4")}</td>
              <td>{this.cell(this.props.board, "g5")}</td>
              <td>{this.cell(this.props.board, "g6")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "g7")}</td>
              <td>{this.cell(this.props.board, "g8")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "g9")}</td>
              <td>{this.cell(this.props.board, "g10")}</td>
              <td>{this.cell(this.props.board, "g11")}</td>
              <td>{this.cell(this.props.board, "g12")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "g13")}</td>
              <td>{this.cell(this.props.board, "g14")}</td>
              <td>{this.cell(this.props.board, "g15")}</td>
            </tr>
            <tr>
              <td className="tableborder">H</td>
              <td className="tablered">{this.cell(this.props.board, "h1")}</td>
              <td>{this.cell(this.props.board, "h2")}</td>
              <td>{this.cell(this.props.board, "h3")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "h4")}</td>
              <td>{this.cell(this.props.board, "h5")}</td>
              <td>{this.cell(this.props.board, "h6")}</td>
              <td>{this.cell(this.props.board, "h7")}</td>
              <td className="tableorange">{this.cell(this.props.board, "h8")}</td>
              <td>{this.cell(this.props.board, "h9")}</td>
              <td>{this.cell(this.props.board, "h10")}</td>
              <td>{this.cell(this.props.board, "h11")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "h12")}</td>
              <td>{this.cell(this.props.board, "h13")}</td>
              <td>{this.cell(this.props.board, "h14")}</td>
              <td className="tablered">{this.cell(this.props.board, "h15")}</td>
            </tr>
            <tr>
              <td className="tableborder">I</td>
              <td>{this.cell(this.props.board, "i1")}</td>
              <td>{this.cell(this.props.board, "i2")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "i3")}</td>
              <td>{this.cell(this.props.board, "i4")}</td>
              <td>{this.cell(this.props.board, "i5")}</td>
              <td>{this.cell(this.props.board, "i6")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "i7")}</td>
              <td>{this.cell(this.props.board, "i8")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "i9")}</td>
              <td>{this.cell(this.props.board, "i10")}</td>
              <td>{this.cell(this.props.board, "i11")}</td>
              <td>{this.cell(this.props.board, "i12")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "i13")}</td>
              <td>{this.cell(this.props.board, "i14")}</td>
              <td>{this.cell(this.props.board, "i15")}</td>
            </tr>
            <tr>
              <td className="tableborder">J</td>
              <td>{this.cell(this.props.board, "j1")}</td>
              <td className="tableblue">{this.cell(this.props.board, "j2")}</td>
              <td>{this.cell(this.props.board, "j3")}</td>
              <td>{this.cell(this.props.board, "j4")}</td>
              <td>{this.cell(this.props.board, "j5")}</td>
              <td className="tableblue">{this.cell(this.props.board, "j6")}</td>
              <td>{this.cell(this.props.board, "j7")}</td>
              <td>{this.cell(this.props.board, "j8")}</td>
              <td>{this.cell(this.props.board, "j9")}</td>
              <td className="tableblue">{this.cell(this.props.board, "j10")}</td>
              <td>{this.cell(this.props.board, "j11")}</td>
              <td>{this.cell(this.props.board, "j12")}</td>
              <td>{this.cell(this.props.board, "j13")}</td>
              <td className="tableblue">{this.cell(this.props.board, "j14")}</td>
              <td>{this.cell(this.props.board, "j15")}</td>
            </tr>
            <tr>
              <td className="tableborder">K</td>
              <td>{this.cell(this.props.board, "k1")}</td>
              <td>{this.cell(this.props.board, "k2")}</td>
              <td>{this.cell(this.props.board, "k3")}</td>
              <td>{this.cell(this.props.board, "k4")}</td>
              <td className="tableorange">{this.cell(this.props.board, "k5")}</td>
              <td>{this.cell(this.props.board, "k6")}</td>
              <td>{this.cell(this.props.board, "k7")}</td>
              <td>{this.cell(this.props.board, "k8")}</td>
              <td>{this.cell(this.props.board, "k9")}</td>
              <td>{this.cell(this.props.board, "k10")}</td>
              <td className="tableorange">{this.cell(this.props.board, "k11")}</td>
              <td>{this.cell(this.props.board, "k12")}</td>
              <td>{this.cell(this.props.board, "k13")}</td>
              <td>{this.cell(this.props.board, "k14")}</td>
              <td>{this.cell(this.props.board, "k15")}</td>
            </tr>
            <tr>
              <td className="tableborder">L</td>
              <td className="tablelightblue">{this.cell(this.props.board, "l1")}</td>
              <td>{this.cell(this.props.board, "l2")}</td>
              <td>{this.cell(this.props.board, "l3")}</td>
              <td className="tableorange">{this.cell(this.props.board, "l4")}</td>
              <td>{this.cell(this.props.board, "l5")}</td>
              <td>{this.cell(this.props.board, "l6")}</td>
              <td>{this.cell(this.props.board, "l7")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "l8")}</td>
              <td>{this.cell(this.props.board, "l9")}</td>
              <td>{this.cell(this.props.board, "l10")}</td>
              <td>{this.cell(this.props.board, "l11")}</td>
              <td className="tableorange">{this.cell(this.props.board, "l12")}</td>
              <td>{this.cell(this.props.board, "l13")}</td>
              <td>{this.cell(this.props.board, "l14")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "l15")}</td>
            </tr>
            <tr>
              <td className="tableborder">M</td>
              <td>{this.cell(this.props.board, "m1")}</td>
              <td>{this.cell(this.props.board, "m2")}</td>
              <td className="tableorange">{this.cell(this.props.board, "m3")}</td>
              <td>{this.cell(this.props.board, "m4")}</td>
              <td>{this.cell(this.props.board, "m5")}</td>
              <td>{this.cell(this.props.board, "m6")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "m7")}</td>
              <td>{this.cell(this.props.board, "m8")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "m9")}</td>
              <td>{this.cell(this.props.board, "m10")}</td>
              <td>{this.cell(this.props.board, "m11")}</td>
              <td>{this.cell(this.props.board, "m12")}</td>
              <td className="tableorange">{this.cell(this.props.board, "m13")}</td>
              <td>{this.cell(this.props.board, "m14")}</td>
              <td>{this.cell(this.props.board, "m15")}</td>
            </tr>
            <tr>
              <td className="tableborder">N</td>
              <td>{this.cell(this.props.board, "n1")}</td>
              <td className="tableorange">{this.cell(this.props.board, "n2")}</td>
              <td>{this.cell(this.props.board, "n3")}</td>
              <td>{this.cell(this.props.board, "n4")}</td>
              <td>{this.cell(this.props.board, "n5")}</td>
              <td className="tableblue">{this.cell(this.props.board, "n6")}</td>
              <td>{this.cell(this.props.board, "n7")}</td>
              <td>{this.cell(this.props.board, "n8")}</td>
              <td>{this.cell(this.props.board, "n9")}</td>
              <td className="tableblue">{this.cell(this.props.board, "n10")}</td>
              <td>{this.cell(this.props.board, "n11")}</td>
              <td>{this.cell(this.props.board, "n12")}</td>
              <td>{this.cell(this.props.board, "n13")}</td>
              <td className="tableorange">{this.cell(this.props.board, "n14")}</td>
              <td>{this.cell(this.props.board, "n15")}</td>
            </tr>
            <tr>
              <td className="tableborder">O</td>
              <td className="tablered">{this.cell(this.props.board, "o1")}</td>
              <td>{this.cell(this.props.board, "o2")}</td>
              <td>{this.cell(this.props.board, "o3")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "o4")}</td>
              <td>{this.cell(this.props.board, "o5")}</td>
              <td>{this.cell(this.props.board, "o6")}</td>
              <td>{this.cell(this.props.board, "o7")}</td>
              <td className="tablered">{this.cell(this.props.board, "o8")}</td>
              <td>{this.cell(this.props.board, "o9")}</td>
              <td>{this.cell(this.props.board, "o10")}</td>
              <td>{this.cell(this.props.board, "o11")}</td>
              <td className="tablelightblue">{this.cell(this.props.board, "o12")}</td>
              <td>{this.cell(this.props.board, "o13")}</td>
              <td>{this.cell(this.props.board, "o14")}</td>
              <td className="tablered">{this.cell(this.props.board, "o15")}</td>
            </tr>
            </tbody>
          </table>
          </center>
        </div>
        </div>
    );
  }

}

export default Board;
