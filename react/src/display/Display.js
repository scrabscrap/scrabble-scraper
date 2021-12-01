import React from 'react';
import '../bootstrap.min.css';
import '../App.css';

import Player from './Player';
import Picture from './Picture';
import Moves from './Moves';
import Board from './Board';
import Bag from './Bag';

export default class Display extends React.Component {
  intervalID;

  constructor(props) {
    super(props);

    this.state = {
      time: null,
      move: null,
      name1: null,
      name2: null,
      score1: 0,
      score2: 0,
      time1: 0,
      time2: 0,
      current: null,
      bag: null,
      board: null,
      moves: null,
      countdown: 5,
      reloadError: 0,
      timeout_counter: 0
    };
  }

  componentDidMount() {
    this.getData();
    // den ersten Timer erzwingen
    this.intervalID = setTimeout(this.counter.bind(this), 1000);
  }

  componentWillUnmount() {
    clearTimeout(this.intervalID);
  }

  getData = () => {
    fetch('web/status.json')
      .then(response => {
        if (response.ok) {
          let data = response;
          // if the type is json return, interpret it as json
          if (response.headers.get('Content-Type').indexOf('application/json')
            > -1) {
            data = response.json();
          }
          this.setState({ errorCount: 0 })
          this.errorCount = 0
          return data;
        }
      })
      .then(data => {
        this.setState({
          time: data.time,
          move: data.move,
          name1: data.name1,
          name2: data.name2,
          score1: data.score1,
          score2: data.score2,
          time1: data.time1,
          time2: data.time2,
          current: data.onmove,
          bag: data.bag,
          board: data.board,
          moves: data.moves
        });
      }).catch(error => {
        var errorCnt = this.state.reloadError + 1
        if (errorCnt > 15) {
          this.setState({ countdown: -1 })
          clearTimeout(this.intervalID);
          errorCnt = 0;
        }
        this.setState({ reloadError: errorCnt })
      });
  }

  counter = () => {
    var next = this.state.countdown - 1
    var cnt_moves = 0
    if (this.state.moves != null) {
      cnt_moves = this.state.moves.length
    }
    if (next <= 0) {
      next = 5
      this.getData()
    }
    if (this.state.moves == null || this.state.moves.length === cnt_moves) {
      this.setState({ timeout_counter: this.state.timeout_counter + 1 })
    }
    /* wenn sich nichts ändert -> nach 30min kein automatischer reload mehr */
    if (this.state.timeout_counter > 1800) {
      this.setState({ countdown: -1 })
      this.setState({ timeout_counter: 0 })
      clearTimeout(this.intervalID);
    } else {
      this.setState({ countdown: next })
      this.intervalID = setTimeout(this.counter.bind(this), 1000);
    }
  }

  render() {
    const fontStyle = {
      fontSize: 18
    }
    return (
      <div>
        <h1 className="title">ScrabScrap<br />
          <div style={fontStyle}>Scrabble-Scraper</div>
        </h1>
        <span
          className="counter">{'\u27F3'} {this.state.countdown}s {(this.state.reloadError
            > 0) ? "(" + this.state.reloadError + " Refresh-Fehler)"
            : ""}</span>
        <div className="container">
          <div className="row">
            <div className="col">
              <Player name={this.state.name1} score={this.state.score1}
                time={this.state.time1} current={this.state.current} />
              <Player name={this.state.name2} score={this.state.score2}
                time={this.state.time2} current={this.state.current} />
              <Board board={this.state.board} />
              <Picture move={this.state.move} />
            </div>
            <div className="col">
              <Bag bag={this.state.bag} />
              <Moves moves={this.state.moves} />
            </div>
          </div>
        </div>
      </div>
    );
  }
}
