import React from "react";

class Picture extends React.Component {

  render() {
    var img = 'web/image-' + this.props.move + '.jpg'
    return(
        <div className="card moves">
          <div className="card-header">Spielfeld</div>
          <div className="card-body">
            <center><img src={img} width={'95%'} alt=" " /></center>
          </div>
        </div>
    );
  }

}

export default Picture;
