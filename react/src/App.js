import React from 'react';
import { Switch, Route } from 'react-router-dom';

import Display from './display/Display';

const App = () => {
  return (
      <Switch>
        <Route exact path='/' component={Display}></Route>
      </Switch>
  );
}

export default App;